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

from flask import Flask, jsonify, request
import topology_utils as tp_utils
import persister_app_constants as pa_constants

app = Flask(__name__)

@app.route('/external_pon_topology', methods=['POST'])
def add_splitter_location_details():
        pon_topology = request.json
        __persist_olt_location_details(pon_topology)
        __persist_onu_splitter_details(pon_topology)
        return jsonify(pon_topology), 201

def __persist_olt_location_details(pon_topology):
        location_dict_list = []
        for details in pon_topology["olt"]:
                location_dict = {}
                location_dict[pa_constants.DEVICE_REF_ID] = details[pa_constants.DEVICE_REF_ID]
                location_dict[pa_constants.CABINET] = details[pa_constants.CABINET]
                location_dict_list.append(location_dict)
        tp_utils.persist_splitter_and_location_in_topology_document(location_dict_list, pa_constants.OLT_TOPOLOGY_INDEX)

def __persist_onu_splitter_details(pon_topology):
        location_splitter_dict_list = []
        for details in pon_topology["onu"]:
                location_splitter_dict = {}
                location_splitter_dict[pa_constants.DEVICE_REF_ID] = details[pa_constants.DEVICE_REF_ID]
                location_splitter_dict[pa_constants.SPLITTER1] = details[pa_constants.SPLITTER1]
                location_splitter_dict[pa_constants.SPLITTER2] = details[pa_constants.SPLITTER2]
                location_splitter_dict[pa_constants.LOCATION] = details[pa_constants.LOCATION]
                location_splitter_dict[pa_constants.POWER_DISTRIBUTION_AREA] = details[pa_constants.POWER_DISTRIBUTION_AREA]
                location_splitter_dict_list.append(location_splitter_dict)
        tp_utils.persist_splitter_and_location_in_topology_document(location_splitter_dict_list, pa_constants.ONU_TOPOLOGY_INDEX)

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)