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
Opensearch Client API:
"""

import logging

import pybreaker
from opensearch_handler.opensearch_constants import OpensearchConstants
from opensearchpy import OpenSearch

logger = logging.getLogger('opensearch_client')


class OpensearchClient:
    """
    Opensearch Client
    """

    def __init__(self):
        try:
            self.opensearch_client = OpenSearch(
                hosts=[{'host': OpensearchConstants.OPENSEARCH_HOST, 'port': OpensearchConstants.OPENSEARCH_PORT}],
                http_compress=True,  # enables gzip compression for request bodies
                http_auth=(OpensearchConstants.OPENSEARCH_USER, OpensearchConstants.OPENSEARCH_PASSWORD),
                use_ssl=True,
                verify_certs=True,
                ssl_assert_hostname=False,
                ssl_show_warn=False,
                ca_certs=OpensearchConstants.OPENSEARCH_CA_CERT_PATH)
        except pybreaker.CircuitBreakerError as e:
            logger.error("%s, Circuit breaker error has occurred when trying to create Opensearch client", e)
            self.opensearch_client = None
            raise Exception(e)

    def search(self, os_index, search_body):
        """
        Searches for data in the specified index using the provided search body.
        Circuit breaker protect to get data form Opensearch.

        Args:
            os_index (str): The name of the index to search.
            search_body (dict): The search body.

        Returns:
            dict: The search results.

        Raises:
            CircuitBeakerError : If a circuit breaker error has occurred when trying to get data from Opensearch.

        """
        try:
            result = self._search(os_index, search_body)
            logger.debug("Circuit breaker get data from Opensearch successfully")
            return result
        except pybreaker.CircuitBreakerError as e:
            logger.error("%s, Circuit breaker error has occurred when trying to get data from Opensearch", e)
            raise Exception(e)

    def add_data_to_index(self, os_index, message, id=None):
        """
        Adds the specified data to the specified index.
        Circuit breaker protects add the specified data to the specified index.

        Args:
            os_index (str): The name of the index to add the data to.
            message (dict): The data to add.

        Returns:
            dict: The response from Opensearch

        Raises:
            CircuitBeakerError : If a circuit breaker error has occurred when trying to add the specified data to the Opensearch.

        """
        try:
            result = self._add_data_to_index(os_index, message, id)
            logger.debug("Circuit breaker add the specified data to the Opensearch successfully")
            return result
        except pybreaker.CircuitBreakerError as e:
            logger.error("%s, Circuit breaker error has occurred when add the specified data to the Opensearch", e)
            raise Exception(e)

    def add_index(self, os_index, index_body):
        """
        Adds the specified index into opensearch
        Circuit breaker protects add the specified data to the specified index.

        Args:
            os_index (str): The name of the index
            index_body (dict): index mapping and details

        Returns:
            dict: The response from Opensearch

        Raises:
            CircuitBeakerError : If a circuit breaker error has occurred when trying to add the specified data to the Opensearch.

        """
        try:
            result = self._create_index(os_index, index_body)
            logger.debug("Circuit breaker add the specified index to the Opensearch successfully")
            return result
        except pybreaker.CircuitBreakerError as e:
            logger.error("%s, Circuit breaker error has occurred when add the specified data to the Opensearch", e)
            raise Exception(e)

    def _add_data_to_index(self, os_index, message, doc_id=None):
        if doc_id is not None:
            add_data_result = self.opensearch_client.index(index=os_index, body=message, id=doc_id)
        else:
            add_data_result = self.opensearch_client.index(index=os_index, body=message)
        return add_data_result

    def _update_data_to_index(self, os_index, message, doc_id):
        return self.opensearch_client.update(index=os_index, body=message, id=doc_id)
    def update_data_to_index(self, os_index, message, doc_id):
        """
        updates the specified data into opensearch index
        Circuit breaker protects add the specified data to the specified index.

        Args:
            os_index (str): The name of the index
            index_body (dict): index mapping and details

        Returns:
            dict: The response from Opensearch

        Raises:
            CircuitBeakerError : If a circuit breaker error has occurred when trying to add the specified data to the Opensearch.

        """
        try:
            result = self._update_data_to_index(os_index, message, doc_id)
            logger.debug("Circuit breaker updated the data to the index of Opensearch successfully")
            return result
        except pybreaker.CircuitBreakerError as e:
            logger.error("%s, Circuit breaker error has occurred when add/update the specified data to the Opensearch", e)
            raise Exception(e)

    def _search(self, os_index, search_body):
        return self.opensearch_client.search(index=os_index, body=search_body)

    def _create_index(self, os_index, index_body):
        return self.opensearch_client.indices.create(index=os_index, body=index_body)

    def get_indexes(self, indexes):
        return self.opensearch_client.indices.get(indexes)

    def delete_document_from_index(self, index, document_id):
        return self.opensearch_client.delete(index=index, id=document_id)

    def check_if_document_exists_in_index(self, index, document_id):
        return self.opensearch_client.exists(index=index, id=document_id)

    def close_connection(self):
        """
        Disconnect to opensearch_handler server
        """
        self.opensearch_client.close()
