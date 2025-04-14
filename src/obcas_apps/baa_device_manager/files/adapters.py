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

logger = logging.getLogger('adapters')


def main():
    adapter_dict_list, adapter_in_use_counter = dm.get_all_adapter_details()
    adapter_count = len(adapter_dict_list)

    with st.container(border=True):
        col1, col2 = st.columns([2, 2], gap="large")
        col1.metric("Total number of Adapters", adapter_count)
        col2.metric("Total number of adapters in use", adapter_in_use_counter)

    st.button("Refresh", type="primary")

    columns = st.columns(2)

    if int(adapter_count) > 2:
        for row in range(adapter_count):
            columns += st.columns(2)
    else:
        columns = st.columns(adapter_count)

    counter1 = 0

    for col in columns:
        if adapter_count > counter1:
            adapter_name = adapter_dict_list[counter1].get("adapter-name")
            counter1 = counter1 + 1
            title = col.container()

            # st.markdown("""
            # <style>.element-container:has(#button-after) + div button {
            #     background-color: #04AA6D;
            #     text-align: center;
            #     width: 400px;
            #     height: 80px;
            #     vertical-align: middle;
            #     border-radius: 145px;
            #     box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
            #     # padding-top: 1000px !important;
            #     # padding-bottom: 20px !important;
            #  }</style>""", unsafe_allow_html=True)
            #
            # st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)

            with title.expander(f"**{adapter_name.upper()}**"):
                adapt_dict = dm.get_adapter_dict(adapter_name, adapter_dict_list)
                logger.info("AdapterDict: %s", adapt_dict)
                column1 = st.columns(2)
                if adapter_count > 2:
                    adapter_rows = int(adapter_count / 2)
                    for rows in range(adapter_rows):
                        column1 += st.columns(2)
                counter = 0

                for container_col in column1:
                    if adapt_dict.__len__() > counter:
                        key, value = list(adapt_dict.items())[counter]
                        if key != "adapter-name":
                            container_col.metric(key, value)
                        counter += 1
        else:
            exit()


if __name__ == '__main__':
    main()
