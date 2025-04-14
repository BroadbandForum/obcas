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
import os
import re
import time
import xml.etree.ElementTree as ET

from nc_client.netconf_api import NcClient as ncc
from opensearch_handler.opensearch_client_api import OpensearchClient

import persister_app_constants as pa_constants
import persister_app_utils as pa_utils

logger = logging.getLogger('topology_utils')

def fetch_and_persist_topology():
    logger.info("fetching topology info")
    osc = OpensearchClient()
    while True:
        olt_topology_dict_list = get_olt_topology()
        if not olt_topology_dict_list:
            logger.info("OLT device list is empty")
        else:
            __parse_and_persist_topology_document(pa_constants.OLT.lower(), olt_topology_dict_list, osc)

        vonu_topology_dict_list = get_vonu_topology()
        onu_topology_dict_list = get_eonu_and_vonu_vani_details(olt_topology_dict_list, vonu_topology_dict_list)
        if not onu_topology_dict_list:
            logger.info("ONU device list is empty")
        else:
            __parse_and_persist_topology_document(pa_constants.ONU.lower(), onu_topology_dict_list, osc)

        time.sleep(86400)

def start_rest_server():
    os.system('python3 external_topology.py')


def get_olt_topology():
    logger.info("fetching OLT topology info")
    nc_get_response = __execute_nc_client_request(pa_constants.GET_ALL_OLT_DEVICES_XML, pa_constants.GET)
    tree = ET.ElementTree(ET.fromstring(nc_get_response.strip()))
    return __get_olt_topology(tree)


def get_vonu_topology():
    logger.info("fetching ONU topology info")
    nc_get_response = __execute_nc_client_request(pa_constants.GET_ALL_ONU_DEVICES_XML, pa_constants.GET)
    tree = ET.ElementTree(ET.fromstring(nc_get_response.strip()))
    return __get_vonu_topology(tree)

def get_eonu_and_vonu_vani_details(olt_topology_dict_list, onu_topology_dict_list):
    onu_device_dict_list = []
    if olt_topology_dict_list is None:
        for onu_topology_dict in onu_topology_dict_list:
            vani_dict_list = __get_v_ani_from_olt(
                {pa_constants.DEVICE_NAME: onu_topology_dict[pa_constants.OLT.lower()]})
            if vani_dict_list:
                onu_device_dict_list += __get_onu_device_dict_list(onu_topology_dict_list, vani_dict_list)
    else:
        for olt_topology_dict in olt_topology_dict_list:
            vani_dict_list = __get_v_ani_from_olt(
                {pa_constants.DEVICE_NAME: olt_topology_dict[pa_constants.DEVICE_REF_ID]})
            if vani_dict_list:
                onu_device_dict_list += __get_onu_device_dict_list(onu_topology_dict_list, vani_dict_list)
    return onu_device_dict_list


def get_eonu_details(eonu_vani_dict_list):
    eonu_device_dict_list = []
    for eonu_vani_dict in eonu_vani_dict_list:
        eonu_device_dict = {}
        eonu_device_dict[pa_constants.DEVICE_REF_ID] = eonu_vani_dict[pa_constants.DEVICE_REF_ID]
        eonu_device_dict[pa_constants.SERIAL_NUMBER] = eonu_vani_dict[pa_constants.SERIAL_NUMBER]
        eonu_device_dict[pa_constants.VENDOR] = eonu_vani_dict[pa_constants.SERIAL_NUMBER][:4]
        eonu_device_dict[pa_constants.V_ANI_REF_ID] = eonu_vani_dict["v_ani_name"]
        eonu_device_dict[pa_constants.OLT.lower()] = eonu_vani_dict["olt_name"]
        eonu_device_dict[pa_constants.VOMCI] = "Not Applicable"

        if "preferred_channel_pair" not in eonu_vani_dict:
            eonu_vani_dict["preferred_channel_pair"] = __get_preferred_channel_pair_from_vani(
                eonu_vani_dict["olt_name"], eonu_vani_dict["v_ani_name"])
        channel_termination = get_ct_using_channel_pair(eonu_vani_dict["olt_name"],
                                                        eonu_vani_dict["preferred_channel_pair"])
        eonu_device_dict[pa_constants.CHANNEL_TERMINATION] = eonu_device_dict[
                                                                 pa_constants.OLT.lower()] + '.' + channel_termination
        eonu_device_dict_list.append(eonu_device_dict)
    return eonu_device_dict_list

def get_vonu_details(vonu_vani_dict_list, onu_topology_dict_list):
    for vonu_vani_dict in vonu_vani_dict_list:
        for onu_topology_dict in onu_topology_dict_list:
            if onu_topology_dict[pa_constants.DEVICE_REF_ID].__eq__(vonu_vani_dict[pa_constants.DEVICE_REF_ID]):
                onu_topology_dict[pa_constants.V_ANI_REF_ID] = vonu_vani_dict["v_ani_name"]
                if "preferred_channel_pair" not in vonu_vani_dict:
                    vonu_vani_dict["preferred_channel_pair"] = __get_preferred_channel_pair_from_vani(
                        onu_topology_dict[pa_constants.OLT.lower()], vonu_vani_dict["v_ani_name"])
                channel_termination = get_ct_using_channel_pair(onu_topology_dict[pa_constants.OLT.lower()],
                                                                vonu_vani_dict["preferred_channel_pair"])
                onu_topology_dict[pa_constants.CHANNEL_TERMINATION] = onu_topology_dict[
                                                                          pa_constants.OLT.lower()] + '.' + channel_termination
    return onu_topology_dict_list

def __get_vonu_and_eonu_device_list(onu_topology_dict_list, vani_dict_list):
    vonu_dict_list = []
    eonu_dict_list = []
    for vani_dict in vani_dict_list:
        is_vonu = False
        for onu_topology_dict in onu_topology_dict_list:
            if onu_topology_dict[pa_constants.DEVICE_REF_ID].__eq__(vani_dict[pa_constants.DEVICE_REF_ID]):
                is_vonu = True
                vonu_dict_list.append(vani_dict)
                break
        if not is_vonu:
            eonu_dict_list.append(vani_dict)
    return vonu_dict_list, eonu_dict_list

def __get_onu_device_dict_list(onu_topology_dict_list, vani_dict_list):
    vonu_vani_dict_list, eonu_vani_dict_list = __get_vonu_and_eonu_device_list(onu_topology_dict_list, vani_dict_list)
    eonu_device_dict_list = get_eonu_details(eonu_vani_dict_list)
    vonu_device_dict_list = get_vonu_details(vonu_vani_dict_list, onu_topology_dict_list)
    return eonu_device_dict_list + vonu_device_dict_list


def fetch_topology_based_on_notification():
    baa_manager = pa_utils.get_nc_client_connection()
    baa_manager.create_subscription(stream_name=pa_constants.NETCONF_STREAM)
    osc = OpensearchClient()
    while True:
        if baa_manager.connected is False:
            logger.debug("Manager is not connected, create new manager instance for topology")
            baa_manager = pa_utils.get_nc_client_connection()
            baa_manager.create_subscription(stream_name=pa_constants.NETCONF_STREAM)
        # This will block until a notification is received because
        # we didn't pass a timeout or block=False
        logger.info("Waiting for next notification:")
        notification = baa_manager.take_notification(block=True, timeout=60)
        if notification is not None:
            notification_xml = notification.notification_xml
            if notification_xml.strip().__contains__(
                    pa_constants.INTERFACE_STATE) and notification_xml.strip().__contains__(
                pa_constants.ONU_PRESENCE_STATE_CHANGE):
                logger.debug("Received ONU presence state change notification: %s", notification_xml)
                notification_dict = __get_ct_from_notification(notification_xml)
                if notification_dict[pa_constants.ONU_STATE].__eq__(
                        pa_constants.ONU_PRESENT_AND_ON_INTENDED_CHANNEL_TERMINATION):
                    logger.info("ONU connected, update device topology for the ONU")
                    __persist_ct_in_topology_document(notification_dict, osc)
            elif notification_xml.strip().__contains__(pa_constants.NETCONF_CONFIG_CHANGE):
                device_ref_id = None
                target_operation_dict_list = __get_device_ref_id_from_config_change_notification(notification_xml)
                for target_operation in target_operation_dict_list:
                    target = target_operation.get(pa_constants.TARGET)
                    operation = target_operation.get(pa_constants.OPERATION)
                    if target is not None:
                        target_split_value = target.split("[baa-network-manager:name=")
                        if target_split_value is not None:
                            device_value = target_split_value[1].split("']")
                            if device_value is not None:
                                device_ref_id = device_value[0].replace("'", "")
                    if device_ref_id is not None:
                        if operation.__eq__(pa_constants.CREATE) or operation.__eq__(
                                pa_constants.MERGE) or operation.__eq__(pa_constants.REPLACE):
                            __fetch_and_persist_device_topology(osc, device_ref_id)
                        elif operation.__eq__(pa_constants.REMOVE) or operation.__eq__(pa_constants.DELETE):
                            __delete_document(target, device_ref_id, osc)


def __get_ct_from_notification(notification_xml):
    notification_tree = ET.ElementTree(ET.fromstring(notification_xml.strip()))
    root = notification_tree.getroot()
    notif_dict = {}
    device_ref_id = None
    for nManager in root:
        if nManager.tag.__eq__(pa_constants.NETWORK_MANAGER_URI):
            for managedDevices in nManager:
                for devices in managedDevices:
                    if devices.tag.__eq__(pa_constants.DEVICE_URI):
                        for device in devices:
                            if device.tag.__eq__(pa_constants.NETWORK_MANAGER_NAME_URI):
                                device_ref_id = device.text
                            if device.tag.__eq__(pa_constants.NETWORK_MANAGER_ROOT_URI):
                                for interfaces_state in device:
                                    if interfaces_state.tag.__eq__(pa_constants.INTERFACE_STATE_URI):
                                        for interface in interfaces_state:
                                            if interface.tag.__eq__(pa_constants.INTERFACE_URI):
                                                for interface_details in interface:
                                                    if interface_details.tag.__eq__(pa_constants.INTERFACE_NAME_URI):
                                                        notif_dict[
                                                            pa_constants.CHANNEL_TERMINATION] = device_ref_id + "." + interface_details.text
                                                    if interface_details.tag.__eq__(
                                                            pa_constants.CHANNEL_TERMINATION_URI):
                                                        for channel_term_details in interface_details:
                                                            if channel_term_details.tag.__eq__(
                                                                    pa_constants.ONU_PRESENCE_STATE_CHANGE_URI):
                                                                for onu_presence_state_change_details in channel_term_details:
                                                                    if onu_presence_state_change_details.tag.__eq__(
                                                                            pa_constants.DETECTED_SERIAL_NUMBER_URI):
                                                                        notif_dict[
                                                                            pa_constants.SERIAL_NUMBER] = onu_presence_state_change_details.text
                                                                    elif onu_presence_state_change_details.tag.__eq__(
                                                                            pa_constants.ONU_PRESENCE_STATE_URI):
                                                                        notif_dict[
                                                                            pa_constants.ONU_STATE] = onu_presence_state_change_details.text
    return notif_dict


def __persist_ct_in_topology_document(notification_dict, osc):
    device_ref_id = fetch_device_ref_id(osc, notification_dict[pa_constants.SERIAL_NUMBER])
    doc_id = pa_constants.ONU_TOPOLOGY_INDEX + "_" + device_ref_id
    del notification_dict[pa_constants.SERIAL_NUMBER]
    del notification_dict[pa_constants.ONU_STATE]
    query_body = {pa_constants.DOC: notification_dict}
    topology_document = json.dumps(query_body, indent=4)
    osc.update_data_to_index(pa_constants.ONU_TOPOLOGY_INDEX, topology_document, doc_id)
    logger.info("Persisted Channel termination in topology document: %s", topology_document)

def persist_splitter_and_location_in_topology_document(external_topology_dict_list, topology_index):
    osc = OpensearchClient()
    for external_topology_dict in external_topology_dict_list:
        device_ref_id = external_topology_dict[pa_constants.DEVICE_REF_ID]
        doc_id = topology_index + "_" + device_ref_id
        olt_hits_value = __get_hits_point_from_search_query(osc, pa_constants.TOPOLOGY_SEARCH_BY_DEVICE_REF_ID_JSON, device_ref_id, topology_index)
        if int(olt_hits_value) > 0:
            query_body = {pa_constants.DOC: external_topology_dict}
            topology_document = json.dumps(query_body, indent=4)
            osc.update_data_to_index(topology_index, topology_document, doc_id)
        else:
            topology_document = json.dumps(external_topology_dict, indent=4)
            osc.add_data_to_index(topology_index, topology_document, doc_id)
        logger.info("Persisted location and splitter details in topology document: %s", topology_document)


def fetch_device_ref_id(osc, serial_number):
    search_query = __get_topology_search_query(serial_number)
    hits_list = osc.search(os_index=pa_constants.ONU_TOPOLOGY_INDEX, search_body=search_query).get(
        pa_constants.HITS).get(pa_constants.HITS)
    for i in range(len(hits_list)):
        if hits_list[i][pa_constants._INDEX].__eq__(pa_constants.ONU_TOPOLOGY_INDEX):
            return hits_list[i][pa_constants._SOURCE].get(pa_constants.DEVICE_REF_ID)


def __get_topology_search_query(serial_number):
    with open(pa_constants.TOPOLOGY_SEARCH_QUERY_JSON) as search_query:
        search_query_dict = json.load(search_query)
        search_query_str = json.dumps(search_query_dict)
        final_query_str = search_query_str.replace("%serialNumber%", serial_number)
        return final_query_str


def __delete_document(target, device_ref_id, osc):
    derived_target = "/baa-network-manager:network-manager/baa-network-manager:managed-devices/baa-network-manager:device[baa-network-manager:name='" + device_ref_id + "']"
    if derived_target.__eq__(target):
        olt_hits_value = __get_hits_point_from_search_query(osc, pa_constants.TOPOLOGY_SEARCH_BY_DEVICE_REF_ID_JSON, device_ref_id, pa_constants.OLT_TOPOLOGY_INDEX)
        onu_hits_value = __get_hits_point_from_search_query(osc, pa_constants.TOPOLOGY_SEARCH_BY_DEVICE_REF_ID_JSON, device_ref_id, pa_constants.ONU_TOPOLOGY_INDEX)

        if int(olt_hits_value) > 0:
            olt_doc_id = pa_constants.OLT_TOPOLOGY_INDEX + "_" + device_ref_id
            osc.delete_document_from_index(pa_constants.OLT_TOPOLOGY_INDEX, olt_doc_id)
            logger.info("Deleted OLT(%s) document from %s", device_ref_id, pa_constants.OLT_TOPOLOGY_INDEX)

            # Delete ONU's which are assoiated with this OLT
            device_ref_id_list = __get_device_from_search_query(osc, pa_constants.TOPOLOGY_GET_ONU_BY_OLT_JSON, device_ref_id, pa_constants.ONU_TOPOLOGY_INDEX)
            for device_ref_id in device_ref_id_list:
                onu_doc_id = pa_constants.ONU_TOPOLOGY_INDEX + "_" + device_ref_id
                osc.delete_document_from_index(pa_constants.ONU_TOPOLOGY_INDEX, onu_doc_id)
                logger.info("Deleted ONU(%s) document from %s", device_ref_id, pa_constants.ONU_TOPOLOGY_INDEX)

        elif int(onu_hits_value) > 0:
            onu_doc_id = pa_constants.ONU_TOPOLOGY_INDEX + "_" + device_ref_id
            osc.delete_document_from_index(pa_constants.ONU_TOPOLOGY_INDEX, onu_doc_id)
            logger.info("Deleted ONU(%s) document from %s", device_ref_id, pa_constants.ONU_TOPOLOGY_INDEX)


def __get_device_ref_id_from_config_change_notification(notification_xml):
    notification_tree = ET.ElementTree(ET.fromstring(notification_xml.strip()))
    root = notification_tree.getroot()
    target_operation_dict_list = []
    for netconf_config_change in root:
        if netconf_config_change.tag.__eq__(pa_constants.NETCONF_CONFIG_CHANGE_IRI):
            for edit in netconf_config_change:
                if edit.tag.__eq__(pa_constants.NETCONF_NOTIFICATION_EDIT):
                    operation = None
                    target = None
                    for edit_details in edit:
                        if edit_details.tag.__eq__(pa_constants.NETCONF_NOTIFICATION_TARGET):
                            if edit_details.text.__contains__(pa_constants.NETCONF_NOTIFICATION_TARGET_PREFIX):
                                if re.search(pa_constants.REGEX_NETWORK_MANAGER, edit_details.text):
                                    target = edit_details.text
                        elif edit_details.tag.__eq__(pa_constants.NETCONF_NOTIFICATION_OPERATION):
                            operation = edit_details.text
                        if operation != None and target != None:
                            target_operation_dict_list.append(
                                {pa_constants.TARGET: target, pa_constants.OPERATION: operation})
    return target_operation_dict_list


def __fetch_and_persist_device_topology(osc, device_ref_id):
    device_type = __get_device_type(device_ref_id)
    device_topology_dict_list, onu_topology_dict_list = __get_device_topology(device_ref_id, device_type)
    __parse_and_persist_topology_document(device_type.lower(), device_topology_dict_list, osc)
    if device_type.__eq__(pa_constants.OLT):
        if onu_topology_dict_list:
            __parse_and_persist_topology_document(pa_constants.ONU.lower(), onu_topology_dict_list, osc)


def __parse_and_persist_topology_document(device_type, topology_dict_list, osc):
    topology_os_index = pa_constants.OBCAS + device_type + pa_constants._TOPOLOGY
    for topology_dict in topology_dict_list:
        olt_hits_value = __get_hits_point_from_search_query(osc, pa_constants.TOPOLOGY_SEARCH_BY_DEVICE_REF_ID_JSON, topology_dict[pa_constants.DEVICE_REF_ID], topology_os_index)
        doc_id = topology_os_index + "_" + topology_dict[pa_constants.DEVICE_REF_ID]
        if int(olt_hits_value) > 0:
            query_body = {pa_constants.DOC: topology_dict}
            topology_document = json.dumps(query_body, indent=4)
            osc.update_data_to_index(topology_os_index, topology_document, doc_id)
            logger.info("Persisted topology document: %s", topology_document)
        else:
            topology_document = json.dumps(topology_dict, indent=4)
            osc.add_data_to_index(topology_os_index, topology_document, doc_id)
            logger.info("Persisted topology document: %s", topology_document)

def __get_hits_point_from_search_query(osc, json_file, device_ref_id, topology_index):
    with open(json_file) as search_query:
        search_query_dict = json.load(search_query)
        search_query_str = json.dumps(search_query_dict)
        final_query_str = search_query_str.replace("%deviceRefId%", device_ref_id)
        return osc.search(topology_index, search_body=final_query_str).get(
            pa_constants.HITS).get(
            pa_constants.TOTAL).get(pa_constants.VALUE)

def __get_device_from_search_query(osc, json_file, device_ref_id, topology_index):
    with open(json_file) as search_query:
        search_query_dict = json.load(search_query)
        search_query_str = json.dumps(search_query_dict)
        final_query_str = search_query_str.replace("%deviceRefId%", device_ref_id)
        hits_list = osc.search(os_index=topology_index, search_body=final_query_str).get(
            pa_constants.HITS).get(pa_constants.HITS)

        device_ref_id_list = []
        for i in range(len(hits_list)):
            if hits_list[i][pa_constants._INDEX].__eq__(topology_index):
                device_ref_id_list.append(hits_list[i][pa_constants._SOURCE].get(pa_constants.DEVICE_REF_ID))
        return device_ref_id_list

def __get_device_type(device_ref_id):
    device_dict = {pa_constants.DEVICE_NAME: device_ref_id}
    nc_get_response = ncc.send_nc_request(pa_constants.GET, pa_constants.GET_DEVICE_TYPE_XML, device_dict)
    tree = ET.ElementTree(ET.fromstring(nc_get_response.strip()))
    root = tree.getroot()
    for data in root:
        if data.tag.__eq__(pa_constants.DATA_URI):
            for nManager in data:
                if nManager.tag.__eq__(pa_constants.NETWORK_MANAGER_URI):
                    for managedDevices in nManager:
                        for devices in managedDevices:
                            if devices.tag.__eq__(pa_constants.DEVICE_URI):
                                for device in devices:
                                    if device.tag.__eq__(pa_constants.DEVICE_MANAGEMENT_URI):
                                        for deviceManagement in device:
                                            if deviceManagement.tag.__eq__(pa_constants.NETWORK_MANAGER_TYPE_URI):
                                                return deviceManagement.text


def __get_device_topology(device_ref_id, device_type):
    device_dict = {pa_constants.DEVICE_NAME: device_ref_id}
    nc_get_response = ncc.send_nc_request(pa_constants.GET, pa_constants.GET_DEVICE_DETAILS_XML, device_dict)
    tree = ET.ElementTree(ET.fromstring(nc_get_response.strip()))
    if device_type is not None:
        if device_type.__eq__(pa_constants.OLT):
            return __get_olt_topology(tree), __get_eonu_details(device_ref_id)
        elif device_type.__eq__(pa_constants.ONU):
            vonu_topology_dict_list = __get_vonu_topology(tree)
            vonu_topology_dict_with_vani_list = get_eonu_and_vonu_vani_details(None, vonu_topology_dict_list)
            if vonu_topology_dict_with_vani_list:
                return vonu_topology_dict_with_vani_list, None
            else:
                return vonu_topology_dict_list, None
        else:
            logger.info("DeviceType is not OLT or ONU")

def __get_eonu_details(device_ref_id):
    vani_dict_list = __get_v_ani_from_olt({pa_constants.DEVICE_NAME: device_ref_id})
    if vani_dict_list:
        return get_eonu_details(vani_dict_list)
    else:
        return None

def __get_olt_topology(tree):
    device_details_dict_list = []
    root = tree.getroot()
    for data in root:
        if data.tag.__eq__(pa_constants.DATA_URI):
            for nManager in data:
                if nManager.tag.__eq__(pa_constants.NETWORK_MANAGER_URI):
                    for managedDevices in nManager:
                        for devices in managedDevices:
                            if devices.tag.__eq__(pa_constants.DEVICE_URI):
                                device_details_dict = {}
                                for device in devices:
                                    if device.tag.__eq__(pa_constants.NETWORK_MANAGER_NAME_URI):
                                        device_details_dict[pa_constants.DEVICE_REF_ID] = device.text
                                    elif device.tag.__eq__(pa_constants.DEVICE_MANAGEMENT_URI):
                                        for deviceManagement in device:
                                            if deviceManagement.tag.__eq__(pa_constants.NETWORK_MANAGER_VENDOR_URI):
                                                device_details_dict[pa_constants.VENDOR] = deviceManagement.text
                                device_details_dict_list.append(device_details_dict)
    return device_details_dict_list


def __get_vonu_topology(tree):
    device_details_dict_list = []
    root = tree.getroot()
    for data in root:
        if data.tag.__eq__(pa_constants.DATA_URI):
            for nManager in data:
                if nManager.tag.__eq__(pa_constants.NETWORK_MANAGER_URI):
                    for managedDevices in nManager:
                        for devices in managedDevices:
                            if devices.tag.__eq__(pa_constants.DEVICE_URI):
                                device_details_dict = {}
                                for device in devices:
                                    if device.tag.__eq__(pa_constants.NETWORK_MANAGER_NAME_URI):
                                        device_details_dict[pa_constants.DEVICE_REF_ID] = device.text
                                    if device.tag.__eq__(pa_constants.DEVICE_MANAGEMENT_URI):
                                        for deviceManagement in device:
                                            if deviceManagement.tag.__eq__(pa_constants.NETWORK_MANAGER_VENDOR_URI):
                                                device_details_dict[pa_constants.VENDOR] = deviceManagement.text
                                            elif deviceManagement.tag.__eq__(pa_constants.ONU_CONFIG_INFO_URI):
                                                for onu_config_info in deviceManagement:
                                                    if onu_config_info.tag.__eq__(
                                                            pa_constants.EXPECTED_SERIAL_NUMBER_URI):
                                                        device_details_dict[
                                                            pa_constants.SERIAL_NUMBER] = onu_config_info.text
                                                    elif onu_config_info.tag.__eq__(
                                                            pa_constants.EXPECTED_ATTACHMENT_POINTS_URI):
                                                        for expected_attachment_points in onu_config_info:
                                                            if expected_attachment_points.tag.__eq__(
                                                                    pa_constants.EXPECTED_ATTACHMENT_POINT_URI):
                                                                for expected_attachment_point in expected_attachment_points:
                                                                    if expected_attachment_point.tag.__eq__(
                                                                            pa_constants.OLT_NAME_URI):
                                                                        device_details_dict[
                                                                            pa_constants.OLT.lower()] = expected_attachment_point.text
                                                    elif onu_config_info.tag.__eq__(
                                                            pa_constants.VOMCI_ONU_MANAGEMENT_URI):
                                                        for vomci_onu_mngmt in onu_config_info:
                                                            if vomci_onu_mngmt.tag.__eq__(
                                                                    pa_constants.VOMCI_FUNCTION_URI):
                                                                device_details_dict[
                                                                    pa_constants.VOMCI] = vomci_onu_mngmt.text
                                device_details_dict_list.append(device_details_dict)

    return device_details_dict_list


def __get_ani_from_onu(device_name_dict):
    netconf_response = __execute_nc_client_request_with_args(pa_constants.GET_ANI_XML, pa_constants.GET_CONFIG,
                                                             device_name_dict)
    tree = ET.ElementTree(ET.fromstring(netconf_response.strip()))
    return __fetch_ani_from_response(tree)

def __get_v_ani_from_olt(device_details_dict):
    netconf_response = __execute_nc_client_request_with_args(pa_constants.GET_V_ANI_XML, pa_constants.GET_CONFIG,
                                                             device_details_dict)
    tree = ET.ElementTree(ET.fromstring(netconf_response.strip()))
    return __fetch_v_ani_from_response(tree)


def __fetch_ani_from_response(tree):
    root = tree.getroot()
    for data in root:
        if data.tag.__eq__(pa_constants.DATA_URI):
            for nManager in data:
                if nManager.tag.__eq__(pa_constants.NETWORK_MANAGER_URI):
                    for managedDevices in nManager:
                        for devices in managedDevices:
                            if devices.tag.__eq__(pa_constants.DEVICE_URI):
                                for device in devices:
                                    if device.tag.__eq__(pa_constants.NETWORK_MANAGER_ROOT_URI):
                                        for interfaces in device:
                                            for interface in interfaces:
                                                for ani_details in interface:
                                                    if ani_details.tag.__eq__(pa_constants.INTERFACE_NAME_URI):
                                                        return ani_details.text

def __fetch_v_ani_from_response(tree):
    v_ani_dict_list = []
    root = tree.getroot()
    olt_name = str()
    for data in root:
        if data.tag.__eq__(pa_constants.DATA_URI):
            for nManager in data:
                if nManager.tag.__eq__(pa_constants.NETWORK_MANAGER_URI):
                    for managedDevices in nManager:
                        for devices in managedDevices:
                            if devices.tag.__eq__(pa_constants.DEVICE_URI):
                                for device in devices:
                                    if device.tag.__eq__(pa_constants.NETWORK_MANAGER_NAME_URI):
                                        olt_name = device.text
                                    if device.tag.__eq__(pa_constants.NETWORK_MANAGER_ROOT_URI):
                                        for interfaces in device:
                                            for interface in interfaces:
                                                v_ani_dict = {}
                                                for v_ani_details in interface:
                                                    if v_ani_details.tag.__eq__(pa_constants.INTERFACE_NAME_URI):
                                                        v_ani_dict["olt_name"] = olt_name
                                                        v_ani_dict["v_ani_name"] = v_ani_details.text
                                                        v_ani_dict[pa_constants.DEVICE_REF_ID] = \
                                                        (v_ani_details.text).rsplit("_", 1)[1]
                                                    if v_ani_details.tag.__eq__("{urn:bbf:yang:bbf-xponvani}v-ani"):
                                                        for channel_details in v_ani_details:
                                                            if channel_details.tag.__eq__(
                                                                    "{urn:bbf:yang:bbf-xponvani}channel-partition"):
                                                                v_ani_dict["channel_partition"] = channel_details.text
                                                            elif channel_details.tag.__eq__(
                                                                    "{urn:bbf:yang:bbf-xponvani}expected-serial-number"):
                                                                v_ani_dict[
                                                                    pa_constants.SERIAL_NUMBER] = channel_details.text
                                                            elif channel_details.tag.__eq__(
                                                                    "{urn:bbf:yang:bbf-xponvani}preferred-channel-pair"):
                                                                v_ani_dict[
                                                                    "preferred_channel_pair"] = channel_details.text
                                                v_ani_dict_list.append(v_ani_dict)
    return v_ani_dict_list


def __execute_nc_client_request(file_name, operation):
    return ncc.send_nc_request(operation, file_name)


def __execute_nc_client_request_with_args(file_name, operation, device_name):
    return ncc.send_nc_request(operation, file_name, device_name)


def __get_preferred_channel_pair_from_vani(device_ref_id, vani_name):
    device_dict = {pa_constants.DEVICE_NAME: device_ref_id, pa_constants.VANI_NAME: vani_name}
    netconf_response = __execute_nc_client_request_with_args(pa_constants.GET_CHANNEL_PAIR_FROM_VANI,
                                                             pa_constants.GET_CONFIG, device_dict)
    tree = ET.ElementTree(ET.fromstring(netconf_response.strip()))
    root = tree.getroot()
    for data in root:
        if data.tag.__eq__(pa_constants.DATA_URI):
            for nManager in data:
                if nManager.tag.__eq__(pa_constants.NETWORK_MANAGER_URI):
                    for managedDevices in nManager:
                        for devices in managedDevices:
                            if devices.tag.__eq__(pa_constants.DEVICE_URI):
                                for device in devices:
                                    if device.tag.__eq__(pa_constants.NETWORK_MANAGER_ROOT_URI):
                                        for interfaces in device:
                                            for interface in interfaces:
                                                for interface_details in interface:
                                                    if interface_details.tag.__eq__(pa_constants.V_ANI_URI):
                                                        for vani_details in interface_details:
                                                            if vani_details.tag.__eq__(pa_constants.CHANNEL_PAIR_URI):
                                                                return vani_details.text


def get_ct_using_channel_pair(device_ref_id, channel_pair_ref):
    device_dict = {pa_constants.DEVICE_NAME: device_ref_id, pa_constants.CHANNEL_PAIR_REF: channel_pair_ref}
    netconf_response = __execute_nc_client_request_with_args(pa_constants.GET_CT_FROM_CHANNEL_PAIR_REF,
                                                             pa_constants.GET_CONFIG,
                                                             device_dict)
    tree = ET.ElementTree(ET.fromstring(netconf_response.strip()))
    root = tree.getroot()
    for data in root:
        if data.tag.__eq__(pa_constants.DATA_URI):
            for nManager in data:
                if nManager.tag.__eq__(pa_constants.NETWORK_MANAGER_URI):
                    for managedDevices in nManager:
                        for devices in managedDevices:
                            if devices.tag.__eq__(pa_constants.DEVICE_URI):
                                for device in devices:
                                    if device.tag.__eq__(pa_constants.NETWORK_MANAGER_ROOT_URI):
                                        for interfaces in device:
                                            for interface in interfaces:
                                                for ct_details in interface:
                                                    if ct_details.tag.__eq__(pa_constants.INTERFACE_NAME_URI):
                                                        return ct_details.text
