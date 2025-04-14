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


import json
import time
import random
import copy
import unittest
from datetime import datetime
from alarm import get_alarms
from topology import get_topologies
from topology_handler import *
from alarm_handler import *
from util import Util
from correlator import get_correlators
from suppress import SuppressReport


class AlarmCorrelationTestCase(unittest.TestCase):


    def test_suppress(self):
        expected_correlations_alarm_resources = ['olt:OLT1']
        AlarmCorrelationTestCase.update_identified_correlations_verify_remained_correlations(self, 'reported_correlations.json', 'identified_correlations4.json', expected_correlations_alarm_resources)
        expected_correlations_alarm_resources = ['olt:OLT2', 'olt:OLT3', 'channelTermination:OLT1.ct2', 'powerDistributionArea:PDA1']
        AlarmCorrelationTestCase.update_identified_correlations_verify_remained_correlations(self, 'reported_correlations.json', 'identified_correlations.json', expected_correlations_alarm_resources)
        expected_correlations_alarm_resources = ['channelTermination:OLT1.ct2']
        AlarmCorrelationTestCase.update_identified_correlations_verify_remained_correlations(self, 'reported_correlations.json', 'identified_correlations2.json', expected_correlations_alarm_resources)
        expected_correlations_alarm_resources = ['olt:OLT1', 'powerDistributionArea:PDA2']
        AlarmCorrelationTestCase.update_identified_correlations_verify_remained_correlations(self, 'reported_correlations.json', 'identified_correlations3.json', expected_correlations_alarm_resources)

    def update_identified_correlations_verify_remained_correlations(self, reported_correlations_file, identified_correlations_file, expected_correlations_alarm_resources):
        reported_correlations = AlarmCorrelationTestCase.read_from_json_file(reported_correlations_file)
        identified_correlations = AlarmCorrelationTestCase.read_from_json_file(identified_correlations_file)
        remained_correlations = SuppressReport.report(identified_correlations, reported_correlations)
        print('\n\n\nremained_correlations\n\n')
        print(remained_correlations)
        self.assertTrue(len(remained_correlations) == len(expected_correlations_alarm_resources))
        self.assertTrue(AlarmCorrelationTestCase.alarmResources_exists(expected_correlations_alarm_resources, remained_correlations))

    def test_correlations(self):
        SuppressReport.periodically_report_correlations()
        AlarmCorrelationTestCase.show_state()
        # onus_topology, olts_topology, alarms = AlarmCorrelationTestCase.read_input_from_files()
        onus_topology, olts_topology, alarms = AlarmCorrelationTestCase.generate_inputs(10, 3, 20, False)
        AlarmCorrelationTestCase.update_topology_alarms_verify_correlations(self, onus_topology, olts_topology, alarms)
        time.sleep(11)
        onus_topology, olts_topology, alarms = AlarmCorrelationTestCase.generate_inputs(100, 20, 60, True)
        alarms.pop(0)
        AlarmCorrelationTestCase.update_topology_alarms_verify_correlations(self, onus_topology, olts_topology, alarms)
        time.sleep(11)
        TopologyHandler.update_onu_olt_topolgoy({}, {})
        AlarmCorrelationTestCase.show_state()

    def update_topology_alarms_verify_correlations(self, onus_topology, olts_topology, alarms):
        TopologyHandler.update_onu_olt_topolgoy(onus_topology, olts_topology)
        AlarmHandler.update_devices_alarms(alarms)
        internal_topology = get_topologies().get()
        internal_alarms = get_alarms().get()
        self.assertTrue(AlarmCorrelationTestCase.verify_inputs_equal_internals(onus_topology, olts_topology, alarms, internal_topology, internal_alarms))
        time.sleep(11)
        AlarmCorrelationTestCase.show_state(print_to_file=True)
        internal_correlations = get_correlators().get_correlation()
        self.assertTrue(AlarmCorrelationTestCase.verify_correlations(internal_correlations, internal_topology, internal_alarms))

    def alarmResources_exists(alarm_resources, correlations):
        for alarm_resource in alarm_resources:
            if not AlarmCorrelationTestCase.alarmResource_exists(alarm_resource, correlations):
                return False
        return True
    
    def alarmResource_exists(alarm_resource, correlations):
        for correlation in correlations:
            if correlation['alarmResource'] == alarm_resource:
                return True
        return False
        
    def show_state(print_to_file=False):
        internal_topology = get_topologies().get()
        internal_alarms = get_alarms().get()
        generated_correlators = get_correlators().get_nfs()
        resulting_correlations = get_correlators().get_correlation()
        print('\n\nInternal Topology:\n', internal_topology)
        print('\n\nInternal Alarms:\n', internal_alarms)
        print('\n\nGenerated Correlators:\n', generated_correlators)
        print('\n\nResulting Correlations:\n', resulting_correlations)
        if print_to_file:
            AlarmCorrelationTestCase.write_to_json_file('internal_topology.json', internal_topology)
            AlarmCorrelationTestCase.write_to_json_file('internal_alarms.json', internal_alarms)
            AlarmCorrelationTestCase.write_to_json_file('generated_correlators.json', generated_correlators)
            AlarmCorrelationTestCase.write_to_json_file('resulting_correlations.json', resulting_correlations)

    def generate_inputs(onu_numbers, olt_numbers, alarm_numbers, is_random=True):
        onus_topology = AlarmCorrelationTestCase.generate_onus_topology(onu_numbers, olt_numbers, is_random)
        alarms = AlarmCorrelationTestCase.generate_alarms(onu_numbers, olt_numbers, alarm_numbers, is_random)
        olts_topology = AlarmCorrelationTestCase.generate_olts_topology(olt_numbers)
        AlarmCorrelationTestCase.write_to_json_file('input_onus_topology.json', onus_topology)
        AlarmCorrelationTestCase.write_to_json_file('input_olts_topology.json', olts_topology)
        AlarmCorrelationTestCase.write_to_json_file('input_alarms.json', alarms)
        return onus_topology, olts_topology, alarms

    def read_input_from_files():
        onus_topology = identified_correlations = AlarmCorrelationTestCase.read_from_json_file('input_onus_topology.json')
        olts_topology = identified_correlations = AlarmCorrelationTestCase.read_from_json_file('input_olts_topology.json')
        alarms = identified_correlations = AlarmCorrelationTestCase.read_from_json_file('input_alarms.json')
        return onus_topology, olts_topology, alarms

    def write_to_json_file(path, content):
        with open('../data/testcases/' + path , 'w') as fout:
            json_dumps_str = json.dumps(content, indent=4)
            print(json_dumps_str, file=fout)

    def read_from_json_file(path):
        with open('../data/testcases/' + path) as fin:
            result = json.load(fin)
            return result

    def generate_onus_topology(onu_numbers, olt_numbers, is_random=True):
        devices = []
        device = {}
        onu_per_olt = onu_numbers // olt_numbers
        for i in range(onu_numbers + 1):
            device['deviceRefId'] = 'onu' + str(i + 1)
            olt = 'olt' + str(i // onu_per_olt)
            device['olt'] = olt
            if is_random:
                ct = olt + '.ct' + str(i % 4)
                splitter = str(i%2)
            else:
                ct = olt + '.ct1'
                splitter = '1'
            device['channelTermination'] = ct
            device['splitter1'] = ct + '.sp' + splitter
            device['vendor'] = random.choice(['VENDOR1', 'VENDOR2', 'VENDOR3', 'VENDOR4'])
            device['vomci'] = 'vomci' + str(random.randint(1, 3))
            device['location'] = 'building' + str(i // 6)
            devices.append(copy.deepcopy(device))
        return devices
    
    def generate_olts_topology(olt_numbers):
        devices = []
        device = {}
        for i in range(olt_numbers + 1):
            device['deviceRefId'] = 'olt' + str(i + 1)
            device['olt_vendor'] = random.choice(['VENDOR1', 'VENDOR2', 'VENDOR3', 'VENDOR4'])
            device['serverRoom'] = 'room' + str(random.randint(1, 3))
            devices.append(copy.deepcopy(device))
        return devices
    
    def generate_alarms(onu_numbers, olt_numbers, alarm_numbers, is_random=True):
        alarms = []
        alarm = {}
        if is_random == False:
            for i in range(5):
                alarm['deviceRefId'] = 'onu' + str(i+1)
                alarm['alarmTypeId'] = 'alarmType' + str(random.randint(1, 10))
                alarm['alarmResource'] = 'alarmResource' + str(random.randint(1, 5))
                alarm['time'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                alarms.append(copy.deepcopy(alarm))
            return alarms
        for i in range(alarm_numbers + 1):
            alarm['deviceRefId'] = 'onu' + str(random.randint(1, onu_numbers))
            alarm['alarmTypeId'] = 'alarmType' + str(random.randint(1, 10))
            alarm['alarmResource'] = 'alarmResource' + str(random.randint(1, 5))
            alarm['time'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            alarms.append(copy.deepcopy(alarm))
        for i in range(5):
            alarm['deviceRefId'] = 'olt' + str(random.randint(1, olt_numbers))
            alarm['alarmTypeId'] = 'alarmType' + str(random.randint(1, 10))
            alarm['alarmResource'] = 'alarmResource' + str(random.randint(1, 5))
            alarm['time'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            alarms.append(copy.deepcopy(alarm))
        alarm = {}
        for i in range(5):
            alarm['alarmTypeId'] = 'obcas:alarm-correlation'
            alarm['alarmResource'] = 'channelTermination:OLT1.CT_' + str(i)
            alarm['time'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            alarms.append(copy.deepcopy(alarm))            
        return alarms

    def generate_correlations(label_count, value_count, device_count, total_device):
        correlatoins = {}
        for l in range(label_count + 1):
            label = 'label' + str(l)
            correlatoins[label] = {}
            for v in range(value_count + 1):
                value = 'value' + str(v)
                correlatoins[label][value] = {}                
                correlatoins[label][value]['allAlarmTypeIds'] = ["alarmType1"]
                correlatoins[label][value]['correlatedDevices'] = []
                for d in range(random.randint(1, device_count)):
                    correlatoins[label][value]['correlatedDevices'].append(str(random.randint(1, total_device)))
        return correlatoins

    def verify_inputs_equal_internals(onus_topology, olts_topology, alarms, internal_topology, internal_alarms):
        if TopologyHandler.format_onu_olt_topolgoy(onus_topology, olts_topology) != internal_topology:
            return False
        return AlarmHandler.format_devices_alarms(alarms) == internal_alarms
    
    def verify_correlations(correlations, internal_topology, internal_alarms):
        for label in correlations:
            for value in correlations[label]:
                devices = []
                for device in internal_topology:
                    if label in internal_topology[device] and internal_topology[device][label] == value:
                        devices.append(device)
                for device in devices:
                    if device not in internal_alarms or len(internal_alarms[device]) == 0:
                        print('\nERROR: wrong correlation for ', device, label, value)
                        return False
        return True


if __name__ == '__main__':
    unittest.main()
