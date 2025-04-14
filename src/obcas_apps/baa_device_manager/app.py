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
from device_manager_constants import DeviceManagerConstants

logger = logging.getLogger('dm_app')


def remove_padding_from_top_bar():
    st.markdown("""
        <style>
            #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
        </style>
        """, unsafe_allow_html=True)

    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>

        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.markdown("""
        <style>
        [data-testid="stDecoration"] {display: none;}
        </style>""", unsafe_allow_html=True)


def main():
    """
    main method Starts the OB-BAA device manager web application which represents the device statistics.
    From the device manager GUI we should be able to see the device created in OB-BAA, and it's status.
    :return:
    """

    st.set_page_config(page_title="Login", page_icon="pages/images/BBF.ico", initial_sidebar_state="collapsed")
    remove_padding_from_top_bar()

    user = st.text_input("User name")
    password = st.text_input("Password", type="password")
    redirect = st.button("LOGIN")

    if redirect:
        if user == DeviceManagerConstants.UI_USERNAME and password == DeviceManagerConstants.UI_PASSWORD:
            st.switch_page("pages/device_manager.py")
        else:
            st.error("Please login with correct credentials...!")


if __name__ == '__main__':
    main()
