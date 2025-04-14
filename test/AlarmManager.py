import requests
import time

dying_gasp_type = "bbf-xpon-defects:dgi"
lost_of_burst = "bbf-xpon-defects:lobi"
temperature_high = "bbf-hardware-transceiver-alarm-types:temperature-high"

headers = {
    'Content-Type': 'application/json'
}


def raise_alarm(url, vani, type, state):
    data = {
        "requests": [
            {
                "v-ani": vani,
                "action": "ONUALARM",
                "type": type,
                "state": state
            }
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print(f'Alarm succesfully {state}:', response.json())
    else:
        print('Errore:', response.status_code, response.text)


def send_notification(url, resource, type, state, text):
    data = {
        "requests": [
            {
                "resource": resource,
                "action": "IETFALARM",
                "type-id": type,
                "type-qualifier": "",
                "severity": state,
                "text": text
            }
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print(f'Alarm succesfully {state}:', response.json())
    else:
        print('Errore:', response.status_code, response.text)


def fiber_cut(host, port, vani, state):
    url = f'http://{host}:{port}/polt/polt_actions'

    raise_alarm(url, vani, lost_of_burst, state)
    time.sleep(1)


def power_cut(host, port, vani, state):
    url = f'http://{host}:{port}/polt/polt_actions'

    raise_alarm(url, vani, dying_gasp_type, state)
    time.sleep(1)
    raise_alarm(url, vani, lost_of_burst, state)
    time.sleep(1)


def high_temperature(host, port, resource, state, text):
    url = f'http://{host}:{port}/polt/polt_actions'

    send_notification(url, resource, temperature_high, state, text)