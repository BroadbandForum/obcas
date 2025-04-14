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
# limitations under the Licen


_INDEX = '_index'
_SOURCE = '_source'
_ID = '_id'

ALARM_STREAM = "ALARM"
NETCONF_STREAM = "NETCONF"
ALARM_PERSISTER_THREAD = 'alarm_persister_thread'
ACTIVE_ALARMS_INDEX = "obcas-active-alarms"
ALARMS_HISTORY_INDEX = "obcas-history-alarms"
ONU_TOPOLOGY_INDEX = "obcas-onu-topology"
OLT_TOPOLOGY_INDEX = "obcas-olt-topology"
ACTIVE_ALARMS_INDEX_MAPPING_FILE = "active_alarm_index_mapping.json"
ALARMS_HISTORY_INDEX_MAPPING_FILE = "history_alarm_index_mapping.json"
ONU_TOPOLOGY_INDEX_MAPPING_FILE = "onu_topology_index_mapping.json"
OLT_TOPOLOGY_INDEX_MAPPING_FILE = "olt_topology_index_mapping.json"
ALARM_SEARCH_QUERY_JSON = 'alarm_search_query.json'

RESOURCE_URI = '{urn:ietf:params:xml:ns:yang:ietf-alarms}resource'
ALARM_TYPE_ID_URI = '{urn:ietf:params:xml:ns:yang:ietf-alarms}alarm-type-id'
ALARM_TYPE_QUALIFIER_URI = '{urn:ietf:params:xml:ns:yang:ietf-alarms}alarm-type-qualifier'
ALARM_TIME_URI = '{urn:ietf:params:xml:ns:yang:ietf-alarms}time'
ALARM_PERCEIVED_SEVERITY_URI = '{urn:ietf:params:xml:ns:yang:ietf-alarms}perceived-severity'
ALARM_TEXT_URI = '{urn:ietf:params:xml:ns:yang:ietf-alarms}alarm-text'
ALARM_NOTIFICATION_URI = '{urn:ietf:params:xml:ns:yang:ietf-alarms}alarm-notification'
ALARM_NOTIFICATION = 'alarm-notification'
ALARM_RESOURCE = 'alarmResource'
ALARM_TYPE_ID = 'alarmTypeId'
ALARM_TYPE_QUALIFIER = 'alarmTypeQualifier'
TIME = 'time'
ALARM_PERCEIVED_SEVERITY = 'perceivedSeverity'
ALARM_TEXT = 'alarmText'
CLEARED = 'cleared'
ALARM_STATUS = 'alarmStatus'
ALARM_CLEARED_TIME = 'clearedTime'
RAISED = 'raised'
RAISED_TIME = 'raisedTime'
FORWARD_SLASH = '/'
EQUAL = '='

DEVICE_REF_ID = 'deviceRefId'
OLT = 'OLT'
ONU = 'ONU'
GET = 'get'
GET_CONFIG = 'get-config'
INTERFACE_STATE = 'interfaces-state'
ONU_PRESENCE_STATE_CHANGE = 'onu-presence-state-change'
ONU_STATE = 'onu_state'
ONU_PRESENT_AND_ON_INTENDED_CHANNEL_TERMINATION = 'bbf-xpon-onu-types:onu-present-and-on-intended-channel-termination'
NETCONF_CONFIG_CHANGE = 'netconf-config-change'
CREATE = 'create'
MERGE = 'merge'
REPLACE = 'replace'
REMOVE = 'remove'
DELETE = 'delete'
INTERFACE_STATE_URI = '{urn:ietf:params:xml:ns:yang:ietf-interfaces}interfaces-state'
INTERFACE_URI = '{urn:ietf:params:xml:ns:yang:ietf-interfaces}interface'
INTERFACE_NAME_URI = '{urn:ietf:params:xml:ns:yang:ietf-interfaces}name'
CHANNEL_TERMINATION_URI = '{urn:bbf:yang:bbf-xpon}channel-termination'
ONU_PRESENCE_STATE_CHANGE_URI = '{urn:bbf:yang:bbf-xpon-onu-state}onu-presence-state-change'
DETECTED_SERIAL_NUMBER_URI = '{urn:bbf:yang:bbf-xpon-onu-state}detected-serial-number'
ONU_PRESENCE_STATE_URI = '{urn:bbf:yang:bbf-xpon-onu-state}onu-presence-state'
NETCONF_CONFIG_CHANGE_IRI = '{urn:ietf:params:xml:ns:yang:ietf-netconf-notifications}netconf-config-change'
NETCONF_NOTIFICATION_EDIT = '{urn:ietf:params:xml:ns:yang:ietf-netconf-notifications}edit'
NETCONF_NOTIFICATION_TARGET = '{urn:ietf:params:xml:ns:yang:ietf-netconf-notifications}target'
NETCONF_IETF_INTERFACES_TARGET = '{urn:ietf:params:xml:ns:yang:ietf-interfaces}target'
NETCONF_NOTIFICATION_OPERATION = '{urn:ietf:params:xml:ns:yang:ietf-netconf-notifications}operation'
DATA_URI = '{urn:ietf:params:xml:ns:netconf:base:1.0}data'
NETWORK_MANAGER_URI = '{urn:bbf:yang:obbaa:network-manager}network-manager'
DEVICE_URI = '{urn:bbf:yang:obbaa:network-manager}device'
DEVICE_MANAGEMENT_URI = '{urn:bbf:yang:obbaa:network-manager}device-management'
NETWORK_MANAGER_TYPE_URI = '{urn:bbf:yang:obbaa:network-manager}type'
NETWORK_MANAGER_NAME_URI = '{urn:bbf:yang:obbaa:network-manager}name'
NETWORK_MANAGER_ROOT_URI = '{urn:bbf:yang:obbaa:network-manager}root'
NETWORK_MANAGER_VENDOR_URI = '{urn:bbf:yang:obbaa:network-manager}vendor'
NETWORK_MANAGER_ROOT_URI = '{urn:bbf:yang:obbaa:network-manager}root'
ONU_CONFIG_INFO_URI = '{urn:bbf:yang:obbaa:onu-management}onu-config-info'
EXPECTED_SERIAL_NUMBER_URI = '{urn:bbf:yang:obbaa:onu-management}expected-serial-number'
EXPECTED_ATTACHMENT_POINTS_URI = '{urn:bbf:yang:obbaa:onu-management}expected-attachment-points'
EXPECTED_ATTACHMENT_POINT_URI = '{urn:bbf:yang:obbaa:onu-management}expected-attachment-point'
OLT_NAME_URI = '{urn:bbf:yang:obbaa:onu-management}olt-name'
VOMCI_ONU_MANAGEMENT_URI = '{urn:bbf:yang:obbaa:onu-management}vomci-onu-management'
VOMCI_FUNCTION_URI = '{urn:bbf:yang:obbaa:onu-management}vomci-function'
V_ANI_URI = '{urn:bbf:yang:bbf-xponvani}v-ani'
CHANNEL_PAIR_URI = '{urn:bbf:yang:bbf-xponvani}preferred-channel-pair'
BAA_NETWORK_MANAGER_NAME_URI = '/baa-network-manager:network-manager/baa-network-manager:managed-devices/baa-network-manager:device[baa-network-manager:name='
CHANNEL_TERMINATION = 'channelTermination'
SERIAL_NUMBER = 'serialNumber'
DOC = 'doc'
HITS = 'hits'
TOTAL = 'total'
VALUE = 'value'
_TOPOLOGY = '-topology'
OBCAS = 'obcas-'
DEVICE_NAME = 'deviceName'
LOCATION = 'location'
VENDOR = 'vendor'
ANI_REF_ID = 'aniRefId'
V_ANI_REF_ID = 'vaniRefId'
SPLITTER1 = 'splitter1'
SPLITTER2 = 'splitter2'
POWER_DISTRIBUTION_AREA = 'powerDistributionArea'
CABINET = 'cabinet'
VOMCI = 'vomci'
VANI_NAME = 'vani_name'
CHANNEL_PAIR_REF = 'channelPairRef'
OPERATION = 'operation'
TARGET = 'target'
NETCONF_NOTIFICATION_TARGET_PREFIX = "/baa-network-manager:network-manager/baa-network-manager:managed-devices/baa-network-manager:device[baa-network-manager:name="
REGEX_NETWORK_MANAGER = "^/baa-network-manager:network-manager/baa-network-manager.*]$"

TOPOLOGY_PERSISTER_NOTIFICATION_THREAD = 'topology_persister_notification_thread'
TOPOLOGY_PERSISTER_TIMER_THREAD = 'topology_persister_timer_thread'

TOPOLOGY_SEARCH_QUERY_JSON = 'topology_search_query.json'
TOPOLOGY_SEARCH_BY_DEVICE_REF_ID_JSON = 'topology_search_by_device_ref_id.json'
TOPOLOGY_GET_ONU_BY_OLT_JSON = 'topology_get_onu_by_olt.json'

GET_ALL_OLT_DEVICES_XML = 'get_all_olt_devices.xml'
GET_ALL_ONU_DEVICES_XML = 'get_all_onu_devices.xml'
GET_DEVICE_TYPE_XML = 'get_device_type.xml'
GET_DEVICE_DETAILS_XML = 'get_device_details.xml'
GET_ANI_XML = 'get-ani.xml'
GET_V_ANI_XML = 'get-v-ani.xml'
GET_CHANNEL_PAIR_FROM_VANI = 'get_channel_pair_from_vani.xml'
GET_CT_FROM_CHANNEL_PAIR_REF = 'get_ct_from_channel_pair_ref.xml'

### DEFECT NOTIFICATION CONSTANTS:
ACTIVE_DEFECT_NOTIFICATIONS_INDEX = ACTIVE_ALARMS_INDEX
HISTORY_DEFECT_NOTIFICATIONS_INDEX = ALARMS_HISTORY_INDEX
DEFECT_NOTIFICATION_SEARCH_QUERY_JSON = 'defect_notification_search_query.json'
ACTIVE_NOTIFICATIONS_INDEX_MAPPING_FILE = 'active_notifications_index_mapping.json'
HISTORY_NOTIFICATIONS_INDEX_MAPPING_FILE = 'active_notifications_index_mapping.json'
DEFECT_NOTIFICATION_PERSISTER_THREAD = 'defect_notification_persister_thread'
START_REST_SERVER_FOR_EXTERNAL_TOPOLOGY = 'start_rest_server_for_external_topology'
VANI_URI = '{urn:bbf:yang:bbf-xponvani}v-ani'
vANI_REF_ID = 'vAniRefId'
DEFECT_STATE_CHANGE = "defect-state-change"
DEFECT_STATE_CHANGE_URI = '{urn:bbf:yang:bbf-xponvani}defect-state-change'
DEFECT_URI = '{urn:bbf:yang:bbf-xponvani}defect'
DEFECT_TYPE_URI = '{urn:bbf:yang:bbf-xponvani}type'
BBF_XPON_DEFECT_PREFIX = 'bbf-xpon-def'
OBCAS_NOTIFICATION_ALARM = 'obcas-notification-alarm:v-ani-defect'
DEFECT_STATE_URI = '{urn:bbf:yang:bbf-xponvani}state'
DEFECT_LAST_CHANGE_URI = '{urn:bbf:yang:bbf-xponvani}last-change'
TOPOLOGY_SEARCH_QUERY_SEARCH_BY_ANI_REF_ID_JSON = 'topology_search_query_search_by_ani_ref_id.json'
ALARM_RESOURCE_DEVICE_NAME = "baa-network-manager:network-manager/baa-network-manager:managed-devices/baa-network-manager:device[baa-network-manager:name='"
ALARM_RESOURCE_INTERFACE_NAME = "']/baa-network-manager:root/if:interfaces-state/if:interface[if:name='"
ALARM_RESOURCE_SUFFIX = "']"

SINGLE_CODE = "'"
SQUARE_BRACKET_SUFFIX = "]"
