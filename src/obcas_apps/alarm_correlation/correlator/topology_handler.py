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
#
# Created by Jafar Hamin (Nokia) in March 2024


import threading
import os
from mylogging import get_logger
from topology import get_topologies
from util import Util
from retriever import Retriever


TOPOLOGY_SYNCH_INTERVAL_SEC = int(os.environ.get('TOPOLOGY_SYNCH_INTERVAL_SEC', 120))

logger = get_logger()

class TopologyHandler:
    def periodically_update_topology():
        logger.info('\n\n\n##################### Updating topology ...')
        TopologyHandler.update_topolgoy()
        threading.Timer(TOPOLOGY_SYNCH_INTERVAL_SEC, TopologyHandler.periodically_update_topology).start()

    def update_topolgoy():
        onus_topology = Retriever.retrieve_onus_topology()
        logger.debug('onus')
        for onu in onus_topology:
            logger.debug(onu)
        olts_topology = Retriever.retrieve_olts_topology()
        logger.debug('olts')
        for olt in olts_topology:
            logger.debug(olt)
        TopologyHandler.update_onu_olt_topolgoy(onus_topology, olts_topology)

    def update_onu_olt_topolgoy(onus_topology, olts_topology):
        topology_json = TopologyHandler.format_onu_olt_topolgoy(onus_topology, olts_topology)
        get_topologies().update(topology_json)        

    def format_onu_olt_topolgoy(onus_topology, olts_topology):
        onus_json = Util.documents_to_json(onus_topology, 'deviceRefId')
        olts_json = Util.documents_to_json(olts_topology, 'deviceRefId')
        onus_json.update(olts_json)
        return onus_json

