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


from entity import Entities, ListOfDicEntities


class AllAlarms:

    def __init__(self):
        self.__alarms = Entities(ListOfDicEntities)

    def add(self, nf_name, alarm):
        return self.__alarms.add(nf_name, alarm)

    def remove(self, nf_name, alarm):
        return self.__alarms.remove(nf_name, alarm)

    def search(self, nf_name, alarm):
        return self.__alarms.search(nf_name, alarm)

    def remove_nf(self, nf_name):
        return self.__alarms.remove_nf(nf_name)

    def get_alarm_id(alarm):
        if 'alarmTypeId' in alarm:
            return alarm['alarmTypeId']

    def get(self):
        return self.__alarms.get()

    def set(self, alarms):
        return self.__alarms.set(alarms)


allAlarms = None

def get_alarms():
    global allAlarms
    if allAlarms is None:
        allAlarms = AllAlarms()
    return allAlarms