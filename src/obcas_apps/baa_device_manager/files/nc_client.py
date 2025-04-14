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

import streamlit as st
from xml.etree import ElementTree as ET
import device_manager_util as dm
import logging
import os

logger = logging.getLogger('nc_client')


def main():
    column1, column2 = st.columns(2)
    with column1:
        request = st.text_area('Netconf Request', height=575)
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
    with col5:
        on_click = st.button('submit')
    if on_click:
        if not request:
            st.error("Please provide valid netconf request...!")
        else:
            nc_client_operation = str()
            with open("/obcas/netconf_requests/nc_client_request.xml", "wb") as f:
                logger.info("writing request content to file")
                tree = ET.ElementTree(ET.fromstring(request))
                config_or_filter, operation, file, device_dict = dm.get_config_or_filter(tree)
                nc_client_operation = operation
                f.write(ET.tostring(config_or_filter))
            response = dm.execute_nc_client_request(file, nc_client_operation, device_dict)
            logger.info("response is: ", response)
            res = response
            if nc_client_operation is "get" :
                res = os.linesep.join([s for s in response.splitlines() if s.strip()])  # trim empty lines
            with column2:
                st.text_area("Netconf Response", res, height=575)


if __name__ == '__main__':
    main()
