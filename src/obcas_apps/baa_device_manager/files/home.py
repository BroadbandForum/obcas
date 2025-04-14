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
import streamlit as st
import device_manager_util as dm

logger = logging.getLogger('home')


def main():
    logger.info('Starting baa device manager!!')

    device_dict = dm.get_device_counters()

    if device_dict.get('device-name') is not None:
        devices = device_dict.get('device-name').__len__()
        connected_devices = dm.get_connected_device(device_dict)  # connected = true
        connected_and_aligned = dm.get_connected_and_aligned_device(device_dict)  # connected/aligned = true
        aligned_devices = dm.get_aligned_device(device_dict)  # aligned = true
        error_state_devices = dm.get_error_state(device_dict)  # alignment state= error
        device_adapter_family_dict = dm.get_device_count_per_adapter(dm.get_device_family(device_dict))
        device_adapter_family_dict_keys = list(device_adapter_family_dict.keys())
    else:
        devices = 0
        connected_devices = 0
        connected_and_aligned = 0
        aligned_devices = 0
        error_state_devices = 0
        device_adapter_family_dict = {}
        device_adapter_family_dict_keys = []

    st.title("OB-BAA Device manager")
    st.button("Refresh Device Details", type="primary")
    st.subheader("BAA Devices Summary by State")

    with st.container(border=True):
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Number of Devices", devices)
        col2.metric("Number of Connected & Aligned Devices", connected_and_aligned)
        col3.metric("Number of Connected Devices", connected_devices)
        col4.metric("Number of Aligned Devices", aligned_devices)
        col5.metric("Number of Devices in Error State", error_state_devices)

    st.subheader("BAA Devices per Family Type")

    device_adapter_index = 0
    with st.container(border=True):
        column = st.columns(2)
        if len(device_adapter_family_dict_keys) > 2:
            rows = int(len(device_adapter_family_dict_keys) / 2)
            for row in range(rows):
                column += st.columns(2)
        for col in column:
            if len(device_adapter_family_dict) > device_adapter_index:
                key, value = list(device_adapter_family_dict.items())[device_adapter_index]
                col.metric(key, device_adapter_family_dict[key])
                device_adapter_index += 1


if __name__ == '__main__':
    main()
