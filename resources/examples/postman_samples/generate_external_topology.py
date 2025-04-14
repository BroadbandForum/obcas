
import json
import copy

def write_to_json_file(path, content):
    with open(path , 'w') as fout:
        json_dumps_str = json.dumps(content, indent=4)
        print(json_dumps_str, file=fout)
    
def generate_onus_topology(onu_numbers):
    devices = []
    device = {}
    for i in range(onu_numbers):
        olt_id = i // 10
        olt_label = olt_id + 11
        ct_id = 1
        sp_id = (i // 5) % 2 + 1
        building_id = olt_id // 2 + 1
        pda_id = olt_id // 3 + 1
        device['deviceRefId'] = 'ont' + str(i + 1)
        splitter = 'OLT' + str(olt_label) + '.CT_' + str(ct_id) + '.SP' 
        device['splitter2'] = splitter
        device['splitter1'] = splitter + str(sp_id)
        device['location'] = 'building' + str(building_id)
        device['powerDistributionArea'] = 'PDA' + str(pda_id)
        devices.append(copy.deepcopy(device))
    return devices

write_to_json_file("external_onu_topology.json", generate_onus_topology(100))