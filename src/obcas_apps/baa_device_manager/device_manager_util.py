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

import logging
import xml.etree.ElementTree as ET

from nc_client.netconf_api import NcClient as ncc

logger = logging.getLogger('device_manager_util')

global devices
global aligned_devices
global connected_devices
global connected_and_aligned
global error_state_devices


def get_devices(xml_tree):
    """
    *getDevices(xmlTree)* - Returns the list of devices present in OB-BAA
    :param xml_tree:
    :return:
    """
    root = xml_tree.getroot()
    for data in root:
        if data.tag == '{urn:ietf:params:xml:ns:netconf:base:1.0}data':
            for network_manager in data:
                if network_manager.tag == '{urn:bbf:yang:obbaa:network-manager}network-manager':
                    for managed_devices in network_manager:
                        return list(managed_devices)


def get_device_details_as_dict(managed_devices):
    """
    *getDevices(managedDevices)* - Returns the dictionary of device details
    :param list managed_devices:
    :return:
    """
    device_details_dict = {"device-name": [], "device-alignment": [], "device-connection": [],
                           "device-interface-version": [], "device-model": [], "device-type": [], "device-vendor": []}
    for device_list in managed_devices:
        if device_list.tag == '{urn:bbf:yang:obbaa:network-manager}device':
            for device in device_list:
                if device.tag == '{urn:bbf:yang:obbaa:network-manager}name':
                    device_details_dict["device-name"].append(device.text)
                if device.tag == '{urn:bbf:yang:obbaa:network-manager}device-management':
                    for device_management in device:
                        if device_management.tag == '{urn:bbf:yang:obbaa:network-manager}device-state':
                            for device_management_details in device_management:
                                if device_management_details.tag == ('{urn:bbf:yang:obbaa:network-manager}'
                                                                     'configuration-alignment-state'):
                                    device_details_dict["device-alignment"].append(device_management_details.text)
                                if device_management_details.tag == ('{urn:bbf:yang:obbaa:network-manager}'
                                                                     'connection-state'):
                                    for connection in device_management_details:
                                        if connection.tag == '{urn:bbf:yang:obbaa:network-manager}connected':
                                            device_details_dict["device-connection"].append(connection.text)
                        if device_management.tag == '{urn:bbf:yang:obbaa:network-manager}interface-version':
                            device_details_dict["device-interface-version"].append(device_management.text)
                        if device_management.tag == '{urn:bbf:yang:obbaa:network-manager}model':
                            device_details_dict["device-model"].append(device_management.text)
                        if device_management.tag == '{urn:bbf:yang:obbaa:network-manager}type':
                            device_details_dict["device-type"].append(device_management.text)
                        if device_management.tag == '{urn:bbf:yang:obbaa:network-manager}vendor':
                            device_details_dict["device-vendor"].append(device_management.text)
    return device_details_dict


def get_device_counters():
    """
    *get_device_counters(managedDevices)* - Returns the device dict
    :return:
    """
    nc_get_response = ncc.send_nc_request('get', 'get_all_devices.xml')
    tree = ET.ElementTree(ET.fromstring(nc_get_response.strip()))
    device_list = get_devices(tree)
    device_dict = get_device_details_as_dict(device_list)
    logger.info("DM: device dictionary is %s:", device_dict)
    return device_dict


def get_all_device_details():
    """
    *get_all_device_details()* - Returns the list of device dict
    :return:
    """
    nc_get_response = ncc.send_nc_request('get', 'get_all_devices.xml')
    tree = ET.ElementTree(ET.fromstring(nc_get_response.strip()))
    device_list = get_devices(tree)
    device_dict_list = get_device_details(device_list)
    return device_dict_list


def get_device_notification():
    """
    *get_device_notification()* - Returns notifications
    :return:
    """
    notification = ncc.create_subscription_and_take_notification(ncc)
    logger.info("Notification: %s", notification)
    return notification


def get_device_details(managed_devices):
    device_dict_list = list()
    for device_list in managed_devices:
        device_dict = {}
        if device_list.tag == '{urn:bbf:yang:obbaa:network-manager}device':
            for device in device_list:
                if device.tag == '{urn:bbf:yang:obbaa:network-manager}name':
                    device_dict["device-name"] = device.text
                if device.tag == '{urn:bbf:yang:obbaa:network-manager}device-management':
                    for device_management in device:
                        if device_management.tag == '{urn:bbf:yang:obbaa:network-manager}device-state':
                            for device_management_details in device_management:
                                if device_management_details.tag == ('{urn:bbf:yang:obbaa:network-manager}'
                                                                     'configuration-alignment-state'):
                                    device_dict["device-alignment"] = device_management_details.text
                                if device_management_details.tag == ('{urn:bbf:yang:obbaa:network-manager}'
                                                                     'connection-state'):
                                    for connection in device_management_details:
                                        if connection.tag == '{urn:bbf:yang:obbaa:network-manager}connected':
                                            device_dict["device-connected"] = connection.text
                                        if connection.tag == ('{urn:bbf:yang:obbaa:network-manager}'
                                                              'connection-creation-time'):
                                            device_dict["device-connection-time"] = connection.text
                        if device_management.tag == '{urn:bbf:yang:obbaa:network-manager}interface-version':
                            device_dict["device-interface-version"] = device_management.text
                        if device_management.tag == '{urn:bbf:yang:obbaa:network-manager}model':
                            device_dict["device-model"] = device_management.text
                        if device_management.tag == '{urn:bbf:yang:obbaa:network-manager}type':
                            device_dict["device-type"] = device_management.text
                        if device_management.tag == '{urn:bbf:yang:obbaa:network-manager}vendor':
                            device_dict["device-vendor"] = device_management.text
                        if device_management.tag == '{urn:bbf:yang:obbaa:network-manager}device-connection':
                            for connection_details in device_management:
                                if connection_details.tag == '{urn:bbf:yang:obbaa:network-manager}connection-model':
                                    print("device-connection-type:", connection_details.text)
                                    device_dict['device-connection-type'] = connection_details.text
                                if connection_details.tag == '{urn:bbf:yang:obbaa:network-manager}duid':
                                    device_dict['duid'] = connection_details.text
                                if connection_details.tag == '{urn:bbf:yang:obbaa:network-manager}mediated-protocol':
                                    device_dict['mediated-protocol'] = connection_details.text
                                if connection_details.tag == '{urn:bbf:yang:obbaa:network-manager}password-auth':
                                    for password_auth in connection_details:
                                        if password_auth.tag == '{urn:bbf:yang:obbaa:network-manager}authentication':
                                            for authentication in password_auth:
                                                if authentication.tag == '{urn:bbf:yang:obbaa:network-manager}address':
                                                    device_dict['address'] = authentication.text
                                                if authentication.tag == ('{urn:bbf:yang:obbaa:network-manager}'
                                                                          'management-port'):
                                                    device_dict['management-port'] = authentication.text
                                                if authentication.tag == '{urn:bbf:yang:obbaa:network-manager}user-name':
                                                    device_dict['user-name'] = authentication.text
                                                if authentication.tag == '{urn:bbf:yang:obbaa:network-manager}password':
                                                    device_dict['password'] = authentication.text
        device_dict_list.append(device_dict)
    return device_dict_list


def get_device_dict(device_name, devices_dict_list):
    device_dict = {}
    if device_name is not None or device_name != '':
        for dev_dict in devices_dict_list:
            if dev_dict.get('device-name') == device_name:
                device_dict = dev_dict
    return device_dict


def get_adapter_dict(adapter_name, adapter_dict_list):
    adapter_dict = {}
    if adapter_name is not None or adapter_name != '':
        for adapt_dict in adapter_dict_list:
            if adapt_dict.get('adapter-name') == adapter_name:
                adapter_dict = adapt_dict
    return adapter_dict


def get_device_connection_dict(device_name, devices_connection_dict_list):
    device_connection_dict = {}
    if device_name is not None or device_name != '':
        for dev_dict in devices_connection_dict_list:
            if dev_dict.get('device-name') == device_name:
                device_connection_dict = dev_dict
    return device_connection_dict


def get_adapters(xml_tree):
    root = xml_tree.getroot()
    for data in root:
        if data.tag == '{urn:ietf:params:xml:ns:netconf:base:1.0}data':
            for network_manager in data:
                if network_manager.tag == '{urn:bbf:yang:obbaa:network-manager}network-manager':
                    for device_adapter in network_manager:
                        return list(device_adapter)


def get_adapter_details(device_adapter):
    adapter_dict_list = list()
    adapter_in_use_counter = 0
    for adapter in device_adapter:
        if adapter.tag == '{urn:bbf:yang:obbaa:network-manager}device-adapter':
            adapter_dict = {}
            for family in adapter:
                if family.tag == '{urn:bbf:yang:obbaa:network-manager}type':
                    adapter_dict["type"] = family.text
                elif family.tag == '{urn:bbf:yang:obbaa:network-manager}interface-version':
                    adapter_dict["interface-version"] = family.text
                elif family.tag == '{urn:bbf:yang:obbaa:network-manager}model':
                    adapter_dict["model"] = family.text
                elif family.tag == '{urn:bbf:yang:obbaa:network-manager}vendor':
                    adapter_dict["vendor"] = family.text
                elif family.tag == '{urn:bbf:yang:obbaa:network-manager}is-netconf':
                    adapter_dict["is-netconf"] = family.text
                elif family.tag == '{urn:bbf:yang:obbaa:network-manager}developer':
                    adapter_dict["developer"] = family.text
                elif family.tag == '{urn:bbf:yang:obbaa:network-manager}revision':
                    adapter_dict["revision"] = family.text
                elif family.tag == '{urn:bbf:yang:obbaa:network-manager}upload-date':
                    adapter_dict["upload-date"] = family.text
                elif family.tag == '{urn:bbf:yang:obbaa:network-manager}in-use':
                    if family.text == "true":
                        adapter_in_use_counter += 1
                    adapter_dict["in-use"] = family.text
            adapter_dict["adapter-name"] = adapter_dict["vendor"] + "-" + adapter_dict["type"] + "-" + adapter_dict[
                "model"] + "-" + adapter_dict["interface-version"]
            adapter_dict_list.append(adapter_dict)
    return adapter_dict_list, adapter_in_use_counter


def get_all_adapter_details():
    """
    *get_all_adapter_details()* - Returns the list of adapter dict
    :return:
    """
    nc_get_response = ncc.send_nc_request('get', 'get_all_adapters.xml')
    tree = ET.ElementTree(ET.fromstring(nc_get_response.strip()))
    adapters = get_adapters(tree)
    adapter_dict_list, adapter_in_use_counter = get_adapter_details(adapters)
    return adapter_dict_list, adapter_in_use_counter


def get_device_configuration(device_name):
    device_dict = {'deviceName': device_name}
    nc_get_response = ncc.send_nc_request('get-config', 'get_device_data.xml', device_dict)
    return nc_get_response


def get_connected_device(device_dict):
    """
    *get_connected_device(device_dict)* - Calculate and return the number of connected devices present in OB-BAA
    :return:
    """
    connection_count = 0
    dict_list = device_dict.get("device-connection")
    for dict_element in dict_list:
        if dict_element == "true":
            connection_count = connection_count + 1

    return connection_count


def get_aligned_device(device_dict):
    """
    *get_aligned_device(device_dict)* - Calculate and return the number of aligned devices present in OB-BAA
    :return:
    """
    alignment_count = 0
    dict_list = device_dict.get("device-alignment")
    for dict_element in dict_list:
        if dict_element == "Aligned":
            alignment_count = alignment_count + 1

    return alignment_count


def get_error_state(device_dict):
    """
    *get_aligned_device(device_dict)* - Calculate and return the number of Error state devices present in OB-BAA
    :return:
    """
    error_count = 0
    dict_list = device_dict.get("device-alignment")
    for dict_element in dict_list:
        if dict_element != "Aligned" and dict_element != "Never Aligned":
            error_count = error_count + 1
    return error_count


def get_connected_and_aligned_device(device_dict):
    """
        *get_connected_and_aligned_device(device_dict)* - Calculate and return the number of Error state devices present
         in OB-BAA
        :return:
        """
    alignment_count = 0
    for counter in range(device_dict.get("device-name").__len__()):
        if (device_dict.get("device-connection")[counter] == "true" and device_dict.get("device-alignment")[counter] ==
                "Aligned"):
            alignment_count += 1

    return alignment_count


def get_device_family(device_dict):
    device_family_list = []
    for index in range(device_dict.get("device-name").__len__()):
        vendor = device_dict.get("device-vendor")[index]
        model = device_dict.get("device-model")[index]
        device_type = device_dict.get("device-type")[index]
        version = device_dict.get("device-interface-version")[index]
        device_family = vendor + "-" + device_type + "-" + model + "-" + version
        device_family_list.append(device_family)
    logger.info("device family list: %s", device_family_list)
    return device_family_list


def get_device_count_per_adapter(device_adapter_list):
    device_family_dict = {}
    adapter_family = list(set(device_adapter_list))  # set is used to remove the duplicates from list
    for adapter in adapter_family:
        device_family_dict[adapter] = 0
    for device_adapter in device_adapter_list:
        for adapter in adapter_family:
            if device_adapter == adapter:
                device_family_dict[adapter] = device_family_dict[adapter] + 1
    return device_family_dict


def get_config_or_filter(xml_tree):
    file = "nc_client_request.xml"
    device_dict = {}
    root = xml_tree.getroot()
    for child in root:
        if child.tag == '{urn:ietf:params:xml:ns:netconf:base:1.0}edit-config':
            for config in child:
                if config.tag == '{urn:ietf:params:xml:ns:netconf:base:1.0}config':
                    return config, "edit-config", file, device_dict
        elif child.tag == '{urn:ietf:params:xml:ns:netconf:base:1.0}get':
            for get_filter in child:
                if get_filter.tag == '{urn:ietf:params:xml:ns:netconf:base:1.0}filter':
                    for network in get_filter:
                        if network.tag == '{urn:bbf:yang:obbaa:network-manager}network-manager':
                            for managed_devices in network:
                                if managed_devices.tag == '{urn:bbf:yang:obbaa:network-manager}managed-devices':
                                    for device in managed_devices:
                                        if device.tag == '{urn:bbf:yang:obbaa:network-manager}device':
                                            for device_details in device:
                                                if device_details.tag == '{urn:bbf:yang:obbaa:network-manager}root':
                                                     file = "get_device_data.xml"
                                                if device_details.tag == '{urn:bbf:yang:obbaa:network-manager}name':
                                                    device_name = device_details.text
                                                    device_dict = {'deviceName': device_name}
                    return get_filter, "get", file,  device_dict
        elif child.tag == '{urn:ietf:params:xml:ns:netconf:base:1.0}get-config':
            for get_config_filter in child:
                if get_config_filter.tag == '{urn:ietf:params:xml:ns:netconf:base:1.0}filter':
                    for network in get_config_filter:
                        if network.tag == '{urn:bbf:yang:obbaa:network-manager}network-manager':
                            for managed_devices in network:
                                if managed_devices.tag == '{urn:bbf:yang:obbaa:network-manager}managed-devices':
                                    for device in managed_devices:
                                        if device.tag == '{urn:bbf:yang:obbaa:network-manager}device':
                                            for device_details in device:
                                                if device_details.tag == '{urn:bbf:yang:obbaa:network-manager}root':
                                                    file = "get_device_data.xml"
                                                if device_details.tag == '{urn:bbf:yang:obbaa:network-manager}name':
                                                    device_name = device_details.text
                                                    device_dict = {'deviceName': device_name}
                    return get_config_filter, "get-config", file, device_dict
        elif child.tag == '{urn:ietf:params:xml:ns:yang:1}action':
            return child, "action", file, device_dict


def execute_nc_client_request(file_name, operation, device_dict):
    if not device_dict:
        return ncc.send_nc_request(operation, file_name)
    else:
        return ncc.send_nc_request(operation, file_name, device_dict)
