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
# Created by Jafar Hamin (Nokia) in September 2024

import copy
import threading
import os
import json
from mylogging import get_logger
from correlator import get_correlators
from reporter import Reporter
from datetime import datetime
from retriever import Retriever

REPORT_INTERVAL_SEC = int(os.environ.get('REPORT_INTERVAL_SEC', 10))

logger = get_logger()

suppressReporter = None


class SuppressReport:

    common_element_hierarchy = None
    root_causes = None

    def periodically_report_correlations():
        logger.info('\n\n\n##################### Suppressing and reporting correlations ...')
        SuppressReport.retrieve_and_report()
        threading.Timer(REPORT_INTERVAL_SEC, SuppressReport.periodically_report_correlations).start()

    def retrieve_and_report():
        reported_correlations = Retriever.retrieve_correlations()
        logger.debug('\n\nAlready reported correlations')
        for correlation in reported_correlations:
            logger.debug(correlation)
        identified_correlations_json = get_correlators().get_correlation()
        identified_correlations = SuppressReport.list_of_correlations(identified_correlations_json)
        logger.debug('\n\nCurrently identifed correlations')
        for correlation in identified_correlations:
            logger.debug(correlation)
        SuppressReport.report(identified_correlations, reported_correlations)

    def report(identified_correlations, reported_correlations):
        hierarchies, root_causes = SuppressReport.get_hierarchy_rootcauses()
        SuppressReport.identify_root_causes(identified_correlations, root_causes)
        remained_correlations1 = SuppressReport.removed_proper_subsets(identified_correlations)
        remained_correlations = SuppressReport.removed_equal_sets(remained_correlations1, hierarchies, root_causes)
        logger.debug('Remaining correlations')
        for correlation in remained_correlations:
            logger.debug(correlation)
        SuppressReport.clear_reported_correlations(reported_correlations, remained_correlations)
        SuppressReport.raise_identifed_correlations(identified_correlations, remained_correlations)
        return remained_correlations
        
    def clear_reported_correlations(reported_correlations, remained_correlations):
        for correlation in reported_correlations:
            if not correlation in remained_correlations:
                SuppressReport.report_clear_correlation(correlation)

    def raise_identifed_correlations(identified_correlations, remained_correlations):
        for correlation in identified_correlations:
            if correlation in remained_correlations:
                SuppressReport.report_raise_correlation(correlation)

    def removed_proper_subsets(correlations):
        remove_correlations_indexes = []
        for i in range(len(correlations)):
            for j in range(len(correlations)):
                if i == j:
                    continue
                if set(correlations[i]['correlatedDevices']) < set(correlations[j]['correlatedDevices']):
                    remove_correlations_indexes.append(i)
                    break
        remained_correlatins = []
        for i in range(len(correlations)):
            if i not in remove_correlations_indexes:
                remained_correlatins.append(correlations[i])
        return remained_correlatins

    def removed_equal_sets(correlations, hierarchies, root_causes):
        equal_sets, reamined_correlations = SuppressReport.equal_set_correlations(correlations)
        for equal_set in equal_sets:
            one_set = SuppressReport.keep_one_correlation(equal_set, hierarchies, root_causes)
            reamined_correlations.append(one_set)
        return reamined_correlations
    
    def equal_set_correlations(correlations):
        equal_sets = []
        for correlation in correlations:
            found_set = SuppressReport.find_in_equal_sets(equal_sets, correlation)
            if found_set is None:
                equal_sets.append([correlation])
            else:
                found_set.append(correlation)
        result_equal_sets = []
        reamined_correlations = []
        for equal_set in equal_sets:
            if len(equal_set) == 1:
                reamined_correlations.append(equal_set[0])
            else:
                result_equal_sets.append(equal_set)
        return result_equal_sets, reamined_correlations

    def keep_one_correlation(correlations, hierarchies, root_causes):
        removed_indexes = []
        for i in range(len(correlations) - 1):
            for j in range(i+1, len(correlations)):
                if SuppressReport.common_element_is_higher_than(correlations[i], correlations[j], hierarchies):
                    removed_indexes.append(i)
                    break
        remained_correlatins = []
        for i in range(len(correlations)):
            if i not in removed_indexes:
                remained_correlatins.append(correlations[i])

        removed_indexes = []
        for i in range(len(remained_correlatins) - 1):
            for j in range(i+1, len(remained_correlatins)):
                if SuppressReport.common_element_is_less_related_to_root_cause(remained_correlatins[i], remained_correlatins[j], root_causes):
                    removed_indexes.append(i)
                    break             
        remained_correlatins2 = []
        for i in range(len(remained_correlatins)):
            if i not in removed_indexes:
                remained_correlatins2.append(remained_correlatins[i])

        return remained_correlatins2[0]

    def find_in_equal_sets(equal_sets, correlation):
        c = set(correlation['correlatedDevices'])
        for equal_set in equal_sets:
            if c == set(equal_set[0]['correlatedDevices']):
                return equal_set
        return None

    def identify_root_causes(correlations, root_causes):
        for correlation in correlations:
            SuppressReport.identify_root_cause(correlation, root_causes)

    def identify_root_cause(correlation, root_causes):
        for root_cause in root_causes:
            if set(root_cause['alarmTypeIds']) <= set(correlation['commonAlarmTypeIds']):
                correlation['rootCause'] = root_cause['name']
                return
        correlation['rootCause'] = ''

    def common_element_is_less_related_to_root_cause(correlation1, correlation2, root_causes):
        correlation1_is_related = SuppressReport.common_element_is_related_to_root_cause(correlation1, root_causes)
        correlation2_is_related = SuppressReport.common_element_is_related_to_root_cause(correlation2, root_causes)
        if not correlation1_is_related and correlation2_is_related:
            return True
        if correlation1_is_related and not correlation2_is_related:
            return False
        if correlation1['rootCause'] == "" and correlation1['rootCause'] != "":
            return True
        if correlation1['rootCause'] != "" and correlation1['rootCause'] == "":
            return False
        return correlation1['alarmResource'] < correlation2['alarmResource']

    def common_element_is_related_to_root_cause(correlation, root_causes):
        common_element = correlation['alarmResource'].split(":")[0]
        for root_cause in root_causes:
            if correlation['rootCause'] == root_cause['name']:
                return common_element in root_cause['preferred_common_elements']
        return False

    def common_element_is_higher_than(correlation1, correlation2, hierarchies):
        common_element1 = correlation1['alarmResource'].split(":")[0]
        common_element2 = correlation2['alarmResource'].split(":")[0]
        for _, hierarchy in hierarchies.items():
            if common_element1 in hierarchy and common_element2 in hierarchy:
                return hierarchy.index(common_element1) < hierarchy.index(common_element2)
        return False

    def get_hierarchy_rootcauses():
        if SuppressReport.common_element_hierarchy is None or SuppressReport.root_causes is None:
            with open('../data/settings.json') as json_file:
                content = json.load(json_file)
                SuppressReport.common_element_hierarchy = content['common_element_hierarchy']
                SuppressReport.root_causes = content['root_causes']
        return SuppressReport.common_element_hierarchy, SuppressReport.root_causes

    def list_of_correlations(correlations_json):
        result = []
        correlations = copy.deepcopy(correlations_json)
        for label in correlations:
            for value in correlations[label]:
                correlations[label][value]['alarmResource'] = label + ':' + value
                result.append(correlations[label][value])
        return result

    def report_raise_correlation(correlation):
        correlation['alarmStatus'] = 'raised'
        if 'correlatedDevices' in correlation:
            correlation['correlatedDevices'].sort()
        SuppressReport.report_correlation(correlation)

    def report_clear_correlation(correlation):
        correlation['alarmStatus'] = 'cleared'
        SuppressReport.report_correlation(correlation)

    def report_correlation(correlation):
        correlation['alarmTypeId'] = 'obcas:alarm-correlation'
        correlation['time'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        Reporter.report(correlation)
