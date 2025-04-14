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


from entity import Entities, DicEntities
from correlator import Correlators, get_correlators
from alarm import AllAlarms, get_alarms
from mylogging import get_logger

logger = get_logger()

class AllTopologies:

    def __init__(self):
        self.__topologies = Entities(DicEntities)

    def add(self, nf_name, tags):
        self.__topologies.add(nf_name, tags)
        correlators = get_correlators()
        for label in tags:
            if tags[label] is not None: 
                correlators.add(label, tags[label], nf_name)

    def remove(self, nf_name, tags):
        correlators = get_correlators()
        for label in tags:
            correlators.remove(label, tags[label], nf_name)
        self.__topologies.remove(nf_name, tags)

    def search(self, nf_name, tags):
        return self.__topologies.search(nf_name, tags)

    def remove_nf(self, nf_name):
        tags = self.search(nf_name, {})
        correlators = get_correlators()
        for label in tags:
            correlators.remove(label, tags[label], nf_name)
        get_alarms().remove_nf(nf_name)
        self.__topologies.remove_nf(nf_name)

    def get(self):
        return self.__topologies.get()

    def update(self, new_topology):
        logger.debug('updating topology to new topology %s' % (new_topology))
        current_topology = self.get()
        for nf_name in current_topology:
            if nf_name not in new_topology:
                logger.debug('removing nf_name %s' % (nf_name))
                self.remove_nf(nf_name)
                continue
            for label in current_topology[nf_name]:
                if label not in new_topology[nf_name] or current_topology[nf_name][label] != new_topology[nf_name][label]:
                    logger.debug('removing label %s:%s' % (label, current_topology[nf_name][label]))
                    self.remove(nf_name, {label:current_topology[nf_name][label]})
        for nf_name in new_topology:
            self.add(nf_name, new_topology[nf_name])


allTopologies = None

def get_topologies():
    global allTopologies
    if allTopologies is None:
        allTopologies = AllTopologies()
    return allTopologies