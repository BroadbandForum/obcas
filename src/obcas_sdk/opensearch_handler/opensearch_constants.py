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
Opensearch Constants:
"""
import os

class OpensearchConstants:
    OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", default='127.0.0.1')
    OPENSEARCH_PORT = os.getenv("OPENSEARCH_PORT", default=9200)
    OPENSEARCH_USER = os.getenv("OPENSEARCH_USER", default='admin')
    OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_PASSWORD", default='Obcas@2024')
    OPENSEARCH_CA_CERT_PATH = os.getenv("OPENSEARCH_CA_CERT_PATH", default='./root-ca.pem')