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
import xml.etree.ElementTree as ET

from opensearch_handler.opensearch_client_api import OpensearchClient

import persister_app_constants as pa_constants
import persister_app_utils as pa_utils

logger = logging.getLogger('alarm_utils')


def fetch_and_persist_alarm():
    baa_manager = pa_utils.get_nc_client_connection()
    baa_manager.create_subscription(stream_name=pa_constants.ALARM_STREAM)
    osc = OpensearchClient()
    while True:
        if baa_manager.connected is False:
            logger.debug("Manager is not connected, create new manager instance for alarm")
            baa_manager = pa_utils.get_nc_client_connection()
            baa_manager.create_subscription(stream_name=pa_constants.ALARM_STREAM)
        # This will block until a notification is received because
        # we didn't pass a timeout or block=False
        logger.info("Waiting for next alarm-notification:")
        notification = baa_manager.take_notification(block=True, timeout=60)
        if notification is not None:
            notification_xml = notification.notification_xml
            if notification_xml.strip().__contains__(
                    pa_constants.ALARM_NOTIFICATION):
                logger.debug("Received alarm notification: %s", notification_xml)
                alarm_notification_dict = __parse_alarm_notification(notification_xml)
                __parse_and_persist_alarm_document(alarm_notification_dict, osc)


def __parse_alarm_notification(notification_xml):
    alarm_map = {pa_constants.RESOURCE_URI: pa_constants.ALARM_RESOURCE,
                 pa_constants.ALARM_TYPE_ID_URI: pa_constants.ALARM_TYPE_ID,
                 pa_constants.ALARM_TYPE_QUALIFIER_URI: pa_constants.ALARM_TYPE_QUALIFIER,
                 pa_constants.ALARM_TIME_URI: pa_constants.TIME,
                 pa_constants.ALARM_PERCEIVED_SEVERITY_URI: pa_constants.ALARM_PERCEIVED_SEVERITY,
                 pa_constants.ALARM_TEXT_URI: pa_constants.ALARM_TEXT}

    notification_tree = ET.ElementTree(ET.fromstring(notification_xml.strip()))
    root = notification_tree.getroot()
    alarm_notif_dict = {}
    for alarm_notification in root:
        if alarm_notification.tag.__eq__(pa_constants.ALARM_NOTIFICATION_URI):
            for alarm_notification_details in alarm_notification:
                if alarm_notification_details.tag in alarm_map:
                    alarm_notif_dict[alarm_map[alarm_notification_details.tag]] = alarm_notification_details.text
    if alarm_notif_dict[pa_constants.ALARM_PERCEIVED_SEVERITY].__eq__(pa_constants.CLEARED):
        alarm_notif_dict[pa_constants.ALARM_STATUS] = pa_constants.CLEARED
        alarm_notif_dict[pa_constants.ALARM_CLEARED_TIME] = alarm_notif_dict[pa_constants.TIME]
        del alarm_notif_dict[pa_constants.TIME]
    else:
        alarm_notif_dict[pa_constants.ALARM_STATUS] = pa_constants.RAISED
        alarm_notif_dict[pa_constants.RAISED_TIME] = alarm_notif_dict[pa_constants.TIME]
        del alarm_notif_dict[pa_constants.TIME]
    alarm_notif_dict[pa_constants.DEVICE_REF_ID] = \
        alarm_notif_dict[pa_constants.ALARM_RESOURCE].split(pa_constants.FORWARD_SLASH)[2].split(pa_constants.EQUAL)[
            1].replace("'",
                       "").replace(
            "]", "")
    return alarm_notif_dict


def __parse_and_persist_alarm_document(alarm_notification_dict, osc):
    if alarm_notification_dict[pa_constants.ALARM_STATUS].__eq__(pa_constants.RAISED):
        raise_alarm_document = json.dumps(alarm_notification_dict, indent=4)
        osc.add_data_to_index(os_index=pa_constants.ACTIVE_ALARMS_INDEX, message=raise_alarm_document, id=None)
        logger.info("Persisted %s to index %s", raise_alarm_document, pa_constants.ACTIVE_ALARMS_INDEX)
    elif alarm_notification_dict[pa_constants.ALARM_STATUS].__eq__(pa_constants.CLEARED):
        clear_alarm_dict = __delete_cleared_alarm_from_active_alarms_index(osc, alarm_notification_dict)
        clear_alarm_document = json.dumps(clear_alarm_dict, indent=4)
        osc.add_data_to_index(os_index=pa_constants.ALARMS_HISTORY_INDEX, message=clear_alarm_document, id=None)
        logger.info("Persisted %s to index %s", clear_alarm_document, pa_constants.ALARMS_HISTORY_INDEX)


def __delete_cleared_alarm_from_active_alarms_index(osc, alarm_notification_dict):
    search_query = __get_alarm_search_query(alarm_notification_dict[pa_constants.DEVICE_REF_ID],
                                            alarm_notification_dict[pa_constants.ALARM_TYPE_ID],
                                            alarm_notification_dict[pa_constants.ALARM_TEXT],
                                            alarm_notification_dict[pa_constants.ALARM_RESOURCE])
    hits_list = osc.search(os_index=pa_constants.ACTIVE_ALARMS_INDEX, search_body=search_query).get(
        pa_constants.HITS).get(pa_constants.HITS)
    for i in range(len(hits_list)):
        doc_id = hits_list[i][pa_constants._ID]
        alarm_notification_dict[pa_constants.RAISED_TIME] = hits_list[i][pa_constants._SOURCE].get(
            pa_constants.RAISED_TIME)
        if osc.check_if_document_exists_in_index(index=pa_constants.ACTIVE_ALARMS_INDEX, document_id=doc_id):
            try:
                delete_result = osc.delete_document_from_index(index=pa_constants.ACTIVE_ALARMS_INDEX, document_id=doc_id)
                logger.debug("Delete Response: %s", delete_result)
            except Exception as error:
                logger.info("\n ########### Exception Occurred ##########")
                logger.error(error)
    return alarm_notification_dict


def __get_alarm_search_query(device_ref_id, alarm_type_id, alarm_text, alarm_resource):
    with open(pa_constants.ALARM_SEARCH_QUERY_JSON) as search_query:
        search_query_dict = json.load(search_query)
        search_query_str = json.dumps(search_query_dict)
        final_query_str = search_query_str.replace("%deviceRefId%", device_ref_id).replace("%alarmTypeId%",
                                                                                           alarm_type_id).replace(
            "%alarmText%", alarm_text).replace("%alarmResource%", alarm_resource)
        return final_query_str
