import json
import logging
import xml.etree.ElementTree as ET

from opensearch_handler.opensearch_client_api import OpensearchClient

import persister_app_constants as pa_const
import persister_app_utils as pa_utils

logger = logging.getLogger('defect_notification_logger')


def fetch_and_persist_defect_notification():
    baa_manager = pa_utils.get_nc_client_connection()
    baa_manager.create_subscription(stream_name=pa_const.NETCONF_STREAM)
    osc = OpensearchClient()
    while True:
        if baa_manager.connected is False:
            logger.debug("Manager is not connected, create new manager instance for defect notification")
            baa_manager = pa_utils.get_nc_client_connection()
            baa_manager.create_subscription(stream_name=pa_const.NETCONF_STREAM)
        # This will block until a notification is received because
        # we didn't pass a timeout or block=False
        logger.info("Waiting for next defect-notification:")
        notification = baa_manager.take_notification(block=True, timeout=60)
        if notification is not None:
            notification_xml = notification.notification_xml
            if notification_xml.strip().__contains__(
                    pa_const.INTERFACE_STATE) and notification_xml.strip().__contains__(
                pa_const.DEFECT_STATE_CHANGE):
                logger.debug("Received defect change notification: %s", notification_xml)
                defect_notification_dict = __parse_defect_notification(notification_xml)
                __parse_and_persist_defect_notification_document(defect_notification_dict, osc)


def __parse_defect_notification(notification_xml):
    notification_tree = ET.ElementTree(ET.fromstring(notification_xml.strip()))
    root = notification_tree.getroot()
    defect_notif_dict = {}
    olt_name = None
    for nManager in root:
        if nManager.tag.__eq__(pa_const.NETWORK_MANAGER_URI):
            for managedDevices in nManager:
                for devices in managedDevices:
                    if devices.tag.__eq__(pa_const.DEVICE_URI):
                        for device in devices:
                            if device.tag.__eq__(pa_const.NETWORK_MANAGER_NAME_URI):
                                olt_name = device.text
                            if device.tag.__eq__(pa_const.NETWORK_MANAGER_ROOT_URI):
                                for interfaces_state in device:
                                    if interfaces_state.tag.__eq__(pa_const.INTERFACE_STATE_URI):
                                        for interface in interfaces_state:
                                            if interface.tag.__eq__(pa_const.INTERFACE_URI):
                                                for interface_details in interface:
                                                    if interface_details.tag.__eq__(pa_const.INTERFACE_NAME_URI):
                                                        v_ani_name = interface_details.text
                                                        defect_notif_dict[pa_const.DEVICE_REF_ID] = v_ani_name.split("vAni_")[1]
                                                        defect_notif_dict[pa_const.vANI_REF_ID] = v_ani_name
                                                        alarm_resource = pa_const.ALARM_RESOURCE_DEVICE_NAME + olt_name + pa_const.ALARM_RESOURCE_INTERFACE_NAME + v_ani_name + pa_const.ALARM_RESOURCE_SUFFIX
                                                        defect_notif_dict[pa_const.ALARM_RESOURCE] = alarm_resource
                                                    if interface_details.tag.__eq__(pa_const.VANI_URI):
                                                        for vani_details in interface_details:
                                                            if vani_details.tag.__eq__(pa_const.DEFECT_STATE_CHANGE_URI):
                                                                for defect in vani_details:
                                                                    if defect.tag.__eq__(pa_const.DEFECT_URI):
                                                                        for defect_details in defect:
                                                                            if defect_details.tag.__eq__(pa_const.DEFECT_TYPE_URI):
                                                                                defect_notif_dict[pa_const.ALARM_TYPE_ID] = defect_details.text                                                                                
                                                                            if defect_details.tag.__eq__(pa_const.DEFECT_STATE_URI):
                                                                                defect_notif_dict[pa_const.ALARM_STATUS] = defect_details.text
                                                                            if defect_details.tag.__eq__(pa_const.DEFECT_LAST_CHANGE_URI):
                                                                                if defect_notif_dict[pa_const.ALARM_STATUS].__eq__(pa_const.RAISED):
                                                                                    defect_notif_dict[pa_const.RAISED_TIME] = defect_details.text
                                                                                if defect_notif_dict[pa_const.ALARM_STATUS].__eq__(
                                                                                        pa_const.CLEARED):
                                                                                    defect_notif_dict[
                                                                                        pa_const.ALARM_CLEARED_TIME] = defect_details.text

    return defect_notif_dict

def __fetch_olt_and_ont_ref_id_from_onu_topology_index(osc, defect_notification_dict):
    ani_ref_id = defect_notification_dict[pa_const.vANI_REF_ID]
    with open(pa_const.TOPOLOGY_SEARCH_QUERY_SEARCH_BY_ANI_REF_ID_JSON) as search_query:
        search_query_dict = json.load(search_query)
        search_query_str = json.dumps(search_query_dict)
        final_query_str = search_query_str.replace("%aniRefId%", ani_ref_id)
    hits_list = osc.search(os_index=pa_const.ONU_TOPOLOGY_INDEX, search_body=final_query_str).get(
        pa_const.HITS).get(pa_const.HITS)
    for i in range(len(hits_list)):
        if hits_list[i][pa_const._INDEX].__eq__(pa_const.ONU_TOPOLOGY_INDEX):
            defect_notification_dict[pa_const.DEVICE_REF_ID] = hits_list[i][pa_const._SOURCE].get(
                pa_const.DEVICE_REF_ID)
            olt = hits_list[i][pa_const._SOURCE].get(pa_const.OLT.lower())
            alarm_resource = "baa-network-manager:network-manager/baa-network-manager:managed-devices/baa-network-manager:device[baa-network-manager:name='" + olt + "']/baa-network-manager:root/if:interfaces-state/if:interface[if:name='" + ani_ref_id + "']"
            defect_notification_dict[pa_const.ALARM_RESOURCE] = alarm_resource
    return defect_notification_dict

def __parse_and_persist_defect_notification_document(defect_notification_dict, osc):
    if defect_notification_dict[pa_const.ALARM_STATUS].__eq__(pa_const.RAISED):
        raise_defect_notification_document = json.dumps(defect_notification_dict, indent=4)
        osc.add_data_to_index(os_index=pa_const.ACTIVE_DEFECT_NOTIFICATIONS_INDEX, message=raise_defect_notification_document,
                              id=None)
        logger.info("Persisted %s to index %s", raise_defect_notification_document, pa_const.ACTIVE_DEFECT_NOTIFICATIONS_INDEX)
    elif defect_notification_dict[pa_const.ALARM_STATUS].__eq__(pa_const.CLEARED):
        clear_defect_notif = __delete_cleared_notification_from_active_notifications_index(osc,
                                                                                           defect_notification_dict)
        clear_defect_notif_document = json.dumps(clear_defect_notif, indent=4)
        osc.add_data_to_index(os_index=pa_const.HISTORY_DEFECT_NOTIFICATIONS_INDEX, message=clear_defect_notif_document,
                              id=None)
        logger.info("Persisted %s to index %s", clear_defect_notif_document, pa_const.HISTORY_DEFECT_NOTIFICATIONS_INDEX)


def __delete_cleared_notification_from_active_notifications_index(osc, defect_notification_dict):

    search_query = __get_notification_search_query(defect_notification_dict[pa_const.DEVICE_REF_ID],
                                                   defect_notification_dict[pa_const.ALARM_TYPE_ID],
                                                   defect_notification_dict[pa_const.vANI_REF_ID],
                                                   defect_notification_dict[pa_const.ALARM_RESOURCE])
    hits_list = osc.search(os_index=pa_const.ACTIVE_DEFECT_NOTIFICATIONS_INDEX, search_body=search_query).get(
        pa_const.HITS).get(pa_const.HITS)
    for i in range(len(hits_list)):
        doc_id = hits_list[i][pa_const._ID]
        defect_notification_dict[pa_const.RAISED_TIME] = hits_list[i][pa_const._SOURCE].get(
            pa_const.RAISED_TIME)
        if osc.check_if_document_exists_in_index(index=pa_const.ACTIVE_DEFECT_NOTIFICATIONS_INDEX, document_id=doc_id):
            try:
                delete_result = osc.delete_document_from_index(index=pa_const.ACTIVE_DEFECT_NOTIFICATIONS_INDEX, document_id=doc_id)
                logger.debug("Delete Response: %s", delete_result)
            except Exception as error:
                logger.info("\n ########### Exception Occurred ##########")
                logger.error(error)
    return defect_notification_dict


def __get_notification_search_query(device_ref_id, alarm_type_id, vani_ref_id, alarm_resource):
    with open(pa_const.DEFECT_NOTIFICATION_SEARCH_QUERY_JSON) as search_query:
        search_query_dict = json.load(search_query)
        search_query_str = json.dumps(search_query_dict)
        final_query_str = search_query_str.replace("%deviceRefId%", device_ref_id).replace("%alarmTypeId%",
                                                                                           alarm_type_id).replace(
            "%vAniRefId%", vani_ref_id).replace("%alarmResource%", alarm_resource)
        return final_query_str
