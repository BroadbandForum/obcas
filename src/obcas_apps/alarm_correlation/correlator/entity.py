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
import copy
from util import Util


class Entities:
    def __init__(self, nfEntities) -> None:
        self.__entities = {}
        self.__nfEntities = nfEntities
        self.lock = threading.Lock()

    def add(self, nf_name, entity):
        self.lock.acquire()
        try:
            self.__add(nf_name, entity)
        finally:
            self.lock.release()

    def __add(self, nf_name, entity):
        if nf_name not in self.__entities:
            self.__entities[nf_name]= self.__nfEntities()
        self.__entities[nf_name].add(entity)

    def remove(self, nf_name, entity):
        self.lock.acquire()
        try:
            if nf_name not in self.__entities:
                return
            self.__entities[nf_name].remove(entity)
        finally:
            self.lock.release()

    def search(self, nf_name, entity):
        self.lock.acquire()
        try:
            if nf_name not in self.__entities:
                return self.__nfEntities.empty()
            return self.__entities[nf_name].search(entity)
        finally:
            self.lock.release()

    def remove_nf(self, nf_name):
        self.lock.acquire()
        try:
            self.__entities.pop(nf_name, None)
        finally:
            self.lock.release()

    def get(self):
        self.lock.acquire()
        try:
            result = {}
            for nf_name in self.__entities:
                result[nf_name] = self.__entities[nf_name].get()
            return result
        finally:
            self.lock.release()

    def set(self, entities):
        self.lock.acquire()
        try:
            self.__entities = {}
            for nf_name in entities:
                for entity in entities[nf_name]:
                    self.__add(nf_name, entity)
        finally:
            self.lock.release()


class ListOfDicEntities:
    def __init__(self) -> None:
        self.__entities = []
        self.lock = threading.Lock()

    def add(self, entity):
        self.lock.acquire()
        try:
            self.__entities.append(entity)
        finally:
            self.lock.release()

    def remove(self, entity):
        indexes = []
        index = 0
        self.lock.acquire()
        try:
            for my_entity in self.__entities:
                if Util.dic_subsetof(entity, my_entity):
                    indexes.append(index)
                index += 1
            for index in indexes:
                self.__entities.pop(index)
        finally:
            self.lock.release()

    def search(self, entity):
        self.lock.acquire()
        result = []
        try:
            for my_entity in self.__entities:
                if Util.dic_subsetof(entity, my_entity):
                    result.append(copy.deepcopy(my_entity))
            return result
        finally:
            self.lock.release()
    
    def get(self):
        self.lock.acquire()
        try:
            return copy.deepcopy(self.__entities)
        finally:
            self.lock.release()
    
    def empty():
        return []

    
class DicEntities:
    def __init__(self) -> None:
        self.__entity = {}
        self.lock = threading.Lock()

    def add(self, entity):
        self.lock.acquire()
        try:
            self.__entity.update(entity)
        finally:
            self.lock.release()
        return True

    def remove(self, entity):
        self.lock.acquire()
        try:
            for key in entity:
                self.__entity.pop(key, None)
        finally:
            self.lock.release()

    def search(self, entity):
        self.lock.acquire()
        try:
            if Util.dic_subsetof(entity, self.__entity):
                return copy.deepcopy(self.__entity)
        finally:
            self.lock.release()

    def get(self):
        self.lock.acquire()
        try:
            return copy.deepcopy(self.__entity)
        finally:
            self.lock.release()
    
    def empty():
        return {}