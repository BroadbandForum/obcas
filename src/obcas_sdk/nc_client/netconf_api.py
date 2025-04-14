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

"""
Netconf API class defines the APIs to be used to send netconf requests and receive and parse the netconf responses

"""
import logging
import os
from xml.dom.minidom import parseString

import ncclient
from jinja2 import FileSystemLoader, Environment, select_autoescape
from ncclient import manager
from typing import Any
from netconf_console.operations import Rpc
from xml.etree import ElementTree as ET
from nc_client.ncc_constants import NetconfConstants


logger = logging.getLogger('netconf_api')
logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

env = Environment(loader=FileSystemLoader(NetconfConstants.BAA_NC_REQUEST_PATH), autoescape=select_autoescape(['xml']))

class NcClient:

    def send_nc_request(operation, template_name, *args):
        """
        *send_baa_request(operation, template_name, *args)* - Can send different netconf requests(get,edit-config,action and get-config requests) to BAA,
                                                            Sample netconf requests can be found in ./netconf_requests/
        :param operation:
        :param template_name:
        :param args:
        :return:
        """
        with manager.connect(host=NetconfConstants.BAA_SERVER_IP,
                             port=NetconfConstants.BAA_NBI_PORT,
                             username=NetconfConstants.BAA_USERNAME,
                             password=NetconfConstants.BAA_PASSWORD,
                             timeout=30,
                             hostkey_verify=False,
                             device_params={'name': 'nexus'}) as m:
            if operation == 'get':
                logger.info('\n get operation')
                get_template = env.get_template(template_name)
                thisFilter = get_template.render(*args)
                logger.info('\n get filter: %s', thisFilter)
                response = m.get(filter=thisFilter)
                logger.info('\n get response: %s', parseString(response.xml).toprettyxml())
                return parseString(response.xml).toprettyxml()
            elif operation == 'edit-config':
                logger.info('\n edit-config operation')
                edit_config_template = env.get_template(template_name)
                config = edit_config_template.render(*args)
                response = m.edit_config(target='running', config=config)
                logger.info('\n edit-config response: %s', parseString(response.xml).toprettyxml())
                return parseString(response.xml).toprettyxml()
            elif operation == 'get-config':
                logger.info('get-config operation')
                get_config_template = env.get_template(template_name)
                getConfigFilter = get_config_template.render(*args)
                response = m.get_config(source='running', filter=getConfigFilter)
                logger.info('get-config response %s', parseString(response.xml).toprettyxml())
                return parseString(response.xml).toprettyxml()
            elif operation == 'action':
                template_path = os.getenv("BAA_NC_REQUEST_PATH", default='/obcas/netconf_requests/') + template_name
                response = Rpc.invoke(self=None, ns=Any, mc=m, filename=template_path)
                action_response = ET.tostring(response).decode("utf-8")
                logger.info('action response %s', action_response)
                return parseString(action_response).toprettyxml()
            else:
                logger.info('Operation not supported')