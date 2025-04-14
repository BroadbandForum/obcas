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
import device_manager_util as dm
import logging
import streamlit.components.v1 as components

logger = logging.getLogger('devices')


def get_device(device_name, device_dict_list):
    with st.container(border=True):
        dev_dict = dm.get_device_dict(device_name, device_dict_list)
        logger.info("DeviceDict: %s", dev_dict)
        if dev_dict.get('device-name') is not None:
            get_config_response = dm.get_device_configuration(device_name)
        else:
            get_config_response = '<!--Device:' + device_name + ' Not present in BAA-->'
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.button("Back", type="primary")
        with col4:
            st.write(f"**{device_name}**")
        with col7:
            st.download_button(
                label="Download device config",
                data=get_config_response,
                file_name=device_name + '_device_config.xml',
                mime='text/csv',
                type='primary',
            )

        dev_dict.pop("device-name")  # Hide this value in the display column
        if dev_dict.get("device-connection-type") != "call-home":
            dev_dict.pop("password")  # Hide this value in the display column
        column = st.columns(3)
        if len(dev_dict) > 3:
            parameter_count = int(len(dev_dict) / 3)
            for parameters in range(parameter_count):
                column += st.columns(3)
        counter = 0

        for clm in column:
            if dev_dict.__len__() > counter:
                key, value = list(dev_dict.items())[counter]
                if key == "device-connected":
                    if value == "false":
                        clm.metric(label=key, value=value, delta="-DOWN", delta_color="normal")
                    elif value == "true":
                        clm.metric(label=key, value=value, delta="UP", delta_color="normal")
                else:
                    clm.metric(label=key, value=value)
                counter += 1


def ChangeButtonColour(widget_label, font_color, background_color='transparent'):
    htmlstr = f"""
        <script>
            var elements = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < elements.length; ++i) {{ 
                if (elements[i].innerText == '{widget_label}') {{ 
                    elements[i].style.color ='{font_color}';
                    elements[i].style.background = '{background_color}';
                    elements[i].style.padding = '50px'
                }}
            }}
        </script>
        """
    components.html(f"{htmlstr}", height=0, width=0)


def main():
    device_dict_list = dm.get_all_device_details()
    device_count = len(device_dict_list)
    st.button("Refresh", type="primary")

    if device_count > 4:
        columns = st.columns(4)
        rows = st.columns(1)  # display each device details in expanded layout
        for row in range(device_count):
            columns += st.columns(4)
            rows += st.columns(1)
    else:
        columns = st.columns(device_count)
        rows = st.columns(1)

    device_counter = 0
    for col in columns:
        if device_count > device_counter:
            device_name = device_dict_list[device_counter].get("device-name")
            with col.container():
                on_click = st.button(device_name, use_container_width=True)
                ChangeButtonColour(device_name, 'Black', '#C6CACE')
            if on_click:
                row_counter = device_counter // 4
                with rows[row_counter].container():
                    get_device(device_name, device_dict_list)
            device_counter += 1
        else:
            exit()


if __name__ == '__main__':
    main()
