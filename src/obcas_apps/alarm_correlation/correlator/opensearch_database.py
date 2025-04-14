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
from opensearch_handler.opensearch_client_api import OpensearchClient
from mylogging import get_logger

logger = get_logger()

class OsDatabase:
    osc = None

    def create_index(index, index_body):
        try:
            body = json.dumps(index_body)
            return OsDatabase.__get_osc().add_index(os_index=index, index_body=body)
        except Exception as error:
            logger.error(error)

    def add_data_to_index(index, json_data):
        document = json.dumps(json_data, indent=4)
        try:
            return OsDatabase.__get_osc().add_data_to_index(os_index=index, message=document)
        except Exception as error:
            logger.error(error)
            return []

    def delete_document_from_index(index, document_id):
        try:
            return OsDatabase.__get_osc().delete_document_from_index(index=index, document_id=document_id)
        except Exception as error:
            logger.error(error)
            return []

    def search_document(index, query):
        try:
            return OsDatabase.__get_osc().search(os_index=index, search_body=query).get("hits").get("hits")
        except Exception as error:
            logger.error(error)
            return []

    def search(index, query):
        result = OsDatabase.search_document(index, query)
        return OsDatabase._filter(result, '_source')

    def _filter(list_of_dic, key):
        result = []
        for dic in list_of_dic:
            result.append(dic[key])
        return result
    
    def __get_osc():
        if OsDatabase.osc is None:
            OsDatabase.osc = OpensearchClient()
        return OsDatabase.osc


