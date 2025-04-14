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

#!/usr/bin/env python
# encoding: utf-8
"""
    Constants to be used for netconf connections

    """
import os
class NetconfConstants:
    """
    Class that defines the constants that would be required by the netconf_api

    """
    BAA_SERVER_IP = os.getenv("BAA_SERVER_IP", default='127.0.0.1')
    BAA_NBI_PORT = os.getenv("BAA_NBI_PORT", default='9292')
    BAA_USERNAME = os.getenv("BAA_USERNAME", default='admin')
    BAA_PASSWORD = os.getenv("BAA_PASSWORD", default='password')
    BAA_NC_REQUEST_PATH = os.getenv("BAA_NC_REQUEST_PATH", default='/obcas/netconf_requests/')