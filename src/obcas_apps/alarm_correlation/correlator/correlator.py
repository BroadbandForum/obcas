# Copyright 2024 Broadband Forum
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Created by Jafar Hamin (Nokia) in March 2024


import copy
import os
import json
from mylogging import get_logger
import threading
from alarm import AllAlarms, get_alarms



logger = get_logger()

CORRELATOR_CHECK_INTERVAL_SEC = int(os.environ.get('CORRELATOR_CHECK_INTERVAL_SEC', 10))


MIN_CATEGORY_LEN = 2  # Minimum size of a category of devices to be periodically checked for alarm correlations
MIN_NFS_HAVING_ALARM_PER_TOTAL_NFS_PERCENTAGE = 100  
# Minimum percentage of devices raising alarms in a category to be considered as an alarm correlations.
# 100 means all devices in a category must raise alarms to consider that category as an alarm correlation


allCorrelators = None

def get_correlators():
    global allCorrelators
    if allCorrelators is None:
        allCorrelators = Correlators()
    return allCorrelators


class Correlators:
    def __init__(self):
        self.__correlators = {}
        with open('../data/settings.json') as json_file:
            content = json.load(json_file)
            self.__ignore_labels = content['common_element_ignores']

    def add(self, label, value, nf_name):
        if label in self.__ignore_labels:
            return
        if label not in self.__correlators:
            self.__correlators[label] = ValueCorrelators(label)
        self.__correlators[label].add(value, nf_name)

    def remove(self, label, value, nf_name):
        if label not in self.__correlators:
            return
        self.__correlators[label].remove(value, nf_name)
        if self.__correlators[label].len() == 0:
            self.__correlators.pop(label, None)

    def get_correlation(self):
        result = {}
        for label in self.__correlators:
            correlation = self.__correlators[label].get_correlation()
            if correlation:
                result[label] = self.__correlators[label].get_correlation()
        return result

    def get_nfs(self):
        result = {}
        for label in self.__correlators:
            result[label] = self.__correlators[label].get_nfs()
        return result


class ValueCorrelators:
    def __init__(self, label):
        self.label = label
        self.__valueCorrelators = {}
        self.__correlation = None
        self.__worker = None

    def add(self, value, nf_name):
        if value not in self.__valueCorrelators:
            self.__valueCorrelators[value] = NfNameCorrelators(self.label, value)
        self.__valueCorrelators[value].add(nf_name)

    def remove(self, value, nf_name):
        if value not in self.__valueCorrelators:
            return
        self.__valueCorrelators[value].remove(nf_name)
        if self.__valueCorrelators[value].len() == 0:
            self.__valueCorrelators.pop(value, None)
    
    def get_correlation(self):
        result = {}
        for value in self.__valueCorrelators:
            correlation = self.__valueCorrelators[value].get_correlation()
            if correlation:
                result[value] = self.__valueCorrelators[value].get_correlation()
        return result

    def get_nfs(self):
        result = {}
        for value in self.__valueCorrelators:
            result[value] = self.__valueCorrelators[value].get_nfs()
        return result
    
    def len(self):
        result = 0
        for value in self.__valueCorrelators:
            result += self.__valueCorrelators[value].len()
        return result        
                

class NfNameCorrelators:
    def __init__(self, label, value):
        self.label = label
        self.value = value
        self.__nfNameCorrelators = set()
        self.lock = threading.Lock()
        self.correlator = Correlator(self, label, value)

    def add(self, nf_name):
        self.lock.acquire()
        try:
            self.__nfNameCorrelators.add(nf_name)
        finally:
            self.lock.release()
        if len(self.__nfNameCorrelators) >= MIN_CATEGORY_LEN:
            self.correlator.start()
     
    def remove(self, nf_name):
        self.lock.acquire()
        try:
            self.__nfNameCorrelators.remove(nf_name)
        finally:
            self.lock.release()

    def get_nfs(self):
        self.lock.acquire()
        try:
            return list(copy.deepcopy(self.__nfNameCorrelators))
        finally:
            self.lock.release()
    
    def len(self):
        self.lock.acquire()
        try:
            return len(self.__nfNameCorrelators)
        finally:
            self.lock.release()

    def get_correlation(self):
        return self.correlator.get_correlation()

    def __str__(self):
        return self.label + ':' + self.value


class Correlator:

    def __init__(self, category, label, value):
        self.category = category
        self.label = label
        self.value = value
        if label == None or value == None:
            logger.debug('NONE value label = %s value = %s' % (label, value))
        self.category_id = label + ':' + value
        self.__correlation = None
        self.__worker = None
        self.lock = threading.Lock()
    
    def start(self):
        if self.__worker is None:
            logger.debug('Starting correlator %s' % (self.category_id))
            self.__periodically_check_correlation()
    
    def stop(self):
        if self.__worker is not None:
            logger.debug('Stoping correlator %s' % (self.category_id))
            self.__set_correlation(None, self.category.get_nfs())
            self.__worker.cancel()
            self.__worker = None
    
    def __periodically_check_correlation(self):
        nfs = self.category.get_nfs()
        if len(nfs) < MIN_CATEGORY_LEN:
            self.stop()
            return
        logger.debug('Checking correlator %s' % (self.category_id))
        self.__check_correlation(nfs)
        self.__worker = threading.Timer(CORRELATOR_CHECK_INTERVAL_SEC, self.__periodically_check_correlation)
        self.__worker.start()

    def __check_correlation(self, nfs):
        correlation = self.__detect_correlation(nfs)
        if correlation is not None:
            logger.debug('Detected correlation of %s' % (self.category_id))
        self.__set_correlation(correlation, nfs)

    def __detect_correlation(self, nfs):
        nfs_with_alarm_count = Correlator.__number_of_nfs_having_alarm(nfs)
        if (nfs_with_alarm_count / len(nfs) ) < (MIN_NFS_HAVING_ALARM_PER_TOTAL_NFS_PERCENTAGE / 100):
            return None
        all_alarms_ids = Correlator.__all_alarms_ids(nfs)
        common_alarms_ids = Correlator.__common_alarms_ids(nfs)
        return {'allAlarmTypeIds': all_alarms_ids, 'commonAlarmTypeIds': common_alarms_ids, 'correlatedDevices': nfs}

    def __number_of_nfs_having_alarm(nfs):
        result = 0
        for nf_name in nfs:
            alarms = get_alarms().search(nf_name, {})
            if len(alarms) > 0:
                result += 1
        return result

    def __all_alarms_ids(nfs):
        result = set()
        for nf_name in nfs:
            alarms = get_alarms().search(nf_name, {})
            for alarm in alarms:
                result.add(AllAlarms.get_alarm_id(alarm))
        return list(result)

    def __common_alarms_ids(nfs):
        result = set()
        init = True
        for nf_name in nfs:
            alarms = get_alarms().search(nf_name, {})
            alarm_ids = set()
            for alarm in alarms:
                alarm_ids.add(AllAlarms.get_alarm_id(alarm))
            if init:
                result = alarm_ids
                init = False
            else:
                result = result & alarm_ids
            if len(result) == 0:
                return []
        return list(result)

    def __set_correlation(self, correlation, nfs):
        self.lock.acquire()
        try:
            self.__correlation = correlation
        finally:
            self.lock.release()
    
    def get_correlation(self):
        self.lock.acquire()
        try:
            if self.__correlation is None:
                return {}
            return copy.deepcopy(self.__correlation)
        finally:
            self.lock.release()