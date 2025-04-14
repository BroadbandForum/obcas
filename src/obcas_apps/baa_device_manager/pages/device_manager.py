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
from streamlit_option_menu import option_menu
from files import home, devices, adapters, nc_client


def add_upper_nav_bar():
    st.markdown(
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
        unsafe_allow_html=True)

    st.markdown("""
        <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
          <a class="navbar-brand" href="https://youtube.com/dataprofessor" target="_blank">Data Professor</a>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
              <li class="nav-item active">
                <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="/devices" target="_blank">YouTube</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="https://twitter.com/thedataprof" target="_blank">Twitter</a>
              </li>
            </ul>
          </div>
        </nav>
        """, unsafe_allow_html=True)


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
    st.set_page_config(page_title="Device Manager", page_icon="pages/images/BBF.ico", initial_sidebar_state="collapsed", layout="wide")
    remove_padding_from_top_bar()

    selected = option_menu(None, ["Home", "Devices", "Adapters", 'NC Client', 'Logout'],
                           icons=['house', 'cloud-upload', "list-task", 'gear', 'app-indicator'],
                           menu_icon="cast", default_index=0, orientation="horizontal")

    if selected == "Home":
        home.main()
    elif selected == "Devices":
        devices.main()
    elif selected == "Adapters":
        adapters.main()
    elif selected == "NC Client":
        nc_client.main()
    elif selected == "Logout":
        st.switch_page("pages/relogin.py")


if __name__ == '__main__':
    main()
