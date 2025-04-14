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
from database import Database, get_database

logger = get_logger()

ACTIVE_CORRELATIONS_INDEX = Database.ACTIVE_ALARMS_INDEX
HISTORY_CORRELATIONS_INDEX = Database.HISTORY_ALARMS_INDEX

class Reporter:

    def report(correlation):
        # logger.info('Reporting correlation %s' % (json.dumps(correlation, indent=4)))
        Reporter.__persist_correlation(correlation)

    def __persist_correlation(correlation):
        if correlation['alarmStatus'].__eq__("raised"):
            logger.debug('Persisting Raised correlation in index %s\n%s' % (ACTIVE_CORRELATIONS_INDEX, json.dumps(correlation, indent=4)))
            get_database().add_data_to_index(ACTIVE_CORRELATIONS_INDEX, correlation)
        else:
            logger.debug('Removing Cleared correlation from index %s and persisting it in index %s\n%s' % (ACTIVE_CORRELATIONS_INDEX, HISTORY_CORRELATIONS_INDEX, json.dumps(correlation, indent=4)))
            alarmResource = correlation['alarmResource']
            correlations_documents = Reporter.__search_correlations(ACTIVE_CORRELATIONS_INDEX, alarmResource)
            logger.debug('Removing %s number of correlations from index %s' % (len(correlations_documents), ACTIVE_CORRELATIONS_INDEX))
            if len(correlations_documents) > 0:
                correlation['raisedTime'] = correlations_documents[-1]['_source']['time']
                Reporter.__delete_correlations(ACTIVE_CORRELATIONS_INDEX, correlations_documents)
            get_database().add_data_to_index(HISTORY_CORRELATIONS_INDEX, correlation)

    def __search_correlations(index, alarmResource):
        with open('../data/indexes/search_correlations_tmp.json') as query_file:
            query_tmp = json.load(query_file)
        query_str = json.dumps(query_tmp)
        query = query_str.replace("$alarmResource$", alarmResource)
        return get_database().search_document(index, query)

    def __delete_correlations(index, correlations_documents):
        for document in correlations_documents:
            if '_id' in document:
                logger.debug('Removing document with id %s from index %s' % (document['_id'], index))
                get_database().delete_document_from_index(index=index, document_id=document['_id'])

    def __read_index_file(index_path):
        with open('../data/indexes/' + index_path + '.json') as index_file:
            index = json.load(index_file)
        return index