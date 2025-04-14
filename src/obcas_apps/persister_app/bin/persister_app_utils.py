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

import json
import logging

import ncclient
from nc_client.netconf_api import NetconfConstants
from ncclient import manager
from opensearch_handler.opensearch_client_api import OpensearchClient

import persister_app_constants as pa_const

logger = logging.getLogger('persister_app_utils')


def create_opensearch_indexes():
    indexes = [pa_const.ACTIVE_ALARMS_INDEX, pa_const.ALARMS_HISTORY_INDEX, pa_const.ONU_TOPOLOGY_INDEX,
               pa_const.OLT_TOPOLOGY_INDEX, pa_const.ACTIVE_DEFECT_NOTIFICATIONS_INDEX, pa_const.HISTORY_DEFECT_NOTIFICATIONS_INDEX]
    osc = OpensearchClient()
    for index in indexes:
        __check_and_create_index_if_not_present(osc, index)
    osc.close_connection()


def __check_and_create_index_if_not_present(osc, index):
    index_body = __read_json_file_as_string(index)
    try:
        index_details = osc.get_indexes(index)
        logger.debug("Index (%s) already present with details [%s]", index, index_details)
    except Exception:
        result = osc.add_index(os_index=index, index_body=index_body)
        logger.debug("Created index: %s with result %s", index, result)


def get_nc_client_connection():
    baa_manager = ncclient.manager.connect_ssh(host=NetconfConstants.BAA_SERVER_IP,
                                               port=NetconfConstants.BAA_NBI_PORT,
                                               username=NetconfConstants.BAA_USERNAME,
                                               password=NetconfConstants.BAA_PASSWORD,
                                               hostkey_verify=False,
                                               timeout=120)
    return baa_manager


def __read_json_file_as_string(index):
    index_mapping_file_dict = {pa_const.ACTIVE_ALARMS_INDEX: pa_const.ACTIVE_ALARMS_INDEX_MAPPING_FILE,
                               pa_const.ALARMS_HISTORY_INDEX: pa_const.ALARMS_HISTORY_INDEX_MAPPING_FILE,
                               pa_const.ONU_TOPOLOGY_INDEX: pa_const.ONU_TOPOLOGY_INDEX_MAPPING_FILE,
                               pa_const.OLT_TOPOLOGY_INDEX: pa_const.OLT_TOPOLOGY_INDEX_MAPPING_FILE,
                               pa_const.ACTIVE_DEFECT_NOTIFICATIONS_INDEX: pa_const.ACTIVE_NOTIFICATIONS_INDEX_MAPPING_FILE,
                               pa_const.HISTORY_DEFECT_NOTIFICATIONS_INDEX: pa_const.HISTORY_NOTIFICATIONS_INDEX_MAPPING_FILE}

    if index in index_mapping_file_dict:
        file = index_mapping_file_dict.get(index)
        with open(file) as index_mapping:
            index_mapping_dict = json.load(index_mapping)
            index_mapping_str = json.dumps(index_mapping_dict)
            return index_mapping_str
