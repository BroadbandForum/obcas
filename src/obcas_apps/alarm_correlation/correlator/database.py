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

import json
from mylogging import get_logger

logger = get_logger()


class Database:

    ACTIVE_ALARMS_INDEX = 'obcas-active-alarms'
    HISTORY_ALARMS_INDEX = 'obcas-history-alarms'
    OLT_TOPOLOGY_INDEX = 'obcas-olt-topology'
    ONU_TOPOLOGY_INDEX = 'obcas-onu-topology'

    def create_index(index, index_body):
        pass

    def add_data_to_index(index, json_data):
        pass

    def delete_document_from_index(index, document_id):
        pass

    def search_document(index, query):
        pass

    def search(index, query):
        pass


class MockDatabase(Database):

    mock_data_path = {Database.ACTIVE_ALARMS_INDEX: '../data/testcases/input_alarms.json',
                      Database.HISTORY_ALARMS_INDEX: '../data/testcases/input_alarms.json',
                      Database.OLT_TOPOLOGY_INDEX: '../data/testcases/input_olts_topology.json',
                      Database.ONU_TOPOLOGY_INDEX: '../data/testcases/input_olts_topology.json',
                      'ACTIVE_CORRELATIONS_INDEX': '../data/testcases/reported_correlations.json'}

    stored_correlations = []

    def create_index(index, index_body):
        logger.debug("Creating index %s with body \n%s", index, index_body)

    def add_data_to_index(index, json_data):
        logger.debug("Storing in index %s\n%s", index, json_data)
        
    def delete_document_from_index(index, document_id):
        logger.debug("Removing ID %s Removed from index %s", document_id, index)

    def search_document(index, query):
        logger.debug("Searching document query in index %s\n%s", index, query)
        return []

    def search(index, query):
        logger.debug("Searching query in index %s\n%s", index, query)
        if MockDatabase.__is_correlation_query(index, query):
            return MockDatabase.__read_json_file(MockDatabase.mock_data_path['ACTIVE_CORRELATIONS_INDEX'])
        return MockDatabase.__read_json_file(MockDatabase.mock_data_path[index])

    def __is_correlation_query(index, query):
        if index != Database.ACTIVE_ALARMS_INDEX:
            return False
        query_json = json.loads(query)
        if 'query' in query_json:
            if 'match_phrase' in query_json['query']:
                if 'alarmTypeId' in query_json['query']['match_phrase']:
                    return query_json['query']['match_phrase']['alarmTypeId'] == 'obcas:alarm-correlation'
        return False
        

    def __read_json_file(path):
        with open(path) as json_file:
            alarms = json.load(json_file)
        return alarms

gDatabase = None

def get_database(database=None):
    global gDatabase
    if gDatabase is None:
        if database is None:
            logger.warning('No database is specified')
            database = MockDatabase
        gDatabase = database
    return gDatabase



