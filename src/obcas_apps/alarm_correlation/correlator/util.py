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

import copy


class Util:
    def dic_subsetof(dic1, dic2) -> bool:
        for key in dic1:
            if key not in dic2:
                return False
            if dic1[key] != dic2[key]:
                return False
        return True

    def dic_exists_in_dics(dic, dics):
        for dic1 in dics:
            if Util.dic_subsetof(dic, dic1):
                return True
        return False

    def documents_to_json(documents, key, multiple_value = False):
        result = {}
        for document in documents:
            if key not in document:
                continue
            value = copy.deepcopy(document)
            value.pop(key, None)
            if not multiple_value:
                result[document[key]] = value
            else:
                if document[key] in result:
                    result[document[key]].append(value)
                else:
                    result[document[key]] = [value]
        return result
