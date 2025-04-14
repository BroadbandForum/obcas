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
# Created by Jafar Hamin (Nokia) in June 2024

from database import Database, get_database

class Retriever:

    def retrieve_onus_topology():
        QUERY_MATCH_ALL = '{"size": 10000, "query": { "match_all": {}}}'
        return get_database().search(Database.ONU_TOPOLOGY_INDEX, QUERY_MATCH_ALL)

    def retrieve_olts_topology():
        QUERY_MATCH_ALL = '{"size": 10000, "query": { "match_all": {}}}'
        return get_database().search(Database.OLT_TOPOLOGY_INDEX, QUERY_MATCH_ALL)

    def retrieve_alarms():
        QUERY_MATCH_ALARMS = '''{
            "size": 10000,
            "query": {
                "bool" : {
                    "must_not" : {
                        "match_phrase" : {
                            "alarmTypeId": "obcas:alarm-correlation"
                        }
                    }
                }
            }
        }'''
        return get_database().search(Database.ACTIVE_ALARMS_INDEX, QUERY_MATCH_ALARMS)

    def retrieve_correlations():
        QUERY_MATCH_CORRELATIONS = '''{
            "size": 10000,
            "query": {
                "match_phrase": {
                    "alarmTypeId": "obcas:alarm-correlation"
                }
            }
        }'''
        return get_database().search(Database.ACTIVE_ALARMS_INDEX, QUERY_MATCH_CORRELATIONS)