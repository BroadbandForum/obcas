import AlarmManager
import GetTopology

import random
import pandas as pd
import argparse

import os

ALARMS = [
    ("Fiber Cut", AlarmManager.fiber_cut),
    ("Power Cut", AlarmManager.power_cut)
]


def generate_random_alarms(topology, state, df):
    if state == 'raised':
        noise_alarms = random.randint(2, 5)
        print(f"noise_alarms: {noise_alarms}")
        onus = random.sample(topology.onus, noise_alarms)
        index_alarms = [random.randint(0, 1) for _ in range(noise_alarms)]

        d = {
            "onus": [onus.deviceRefId for onus in onus],
            "alarm_raised": index_alarms
        }

        df = pd.DataFrame(d)
        df["state"] = state
    else:
        onus = df["onus"].apply(
            lambda x: next((onu_x for onu_x in topology.onus if onu_x.deviceRefId == x), None)
        )
        index_alarms = df["alarm_raised"]

    for onu, index_alarm in zip(onus, index_alarms):
        alarm_to_raise = ALARMS[index_alarm]
        print(f"{state} alarm on onu {onu.vaniRefId}, OLT {onu.olt.host}:{onu.olt.port}")

        alarm_to_raise[1](onu.olt.host, onu.olt.port, onu.vaniRefId, state)

    df["state"] = state

    return df


def simulate_random(state):
    topology = GetTopology.Topology()
    topology.load_topology()

    onus = []
    if state == "raised":
        onus = random.sample(topology.onus, 5)
        index_alarms = [random.randint(0, 1) for _ in range(5)]

        if os.path.isfile("random.json"):
            state_pd = pd.read_json('random.json')

            if state == state_pd["state"].iloc[0]:
                print("Alarms already raised, wait for clearing these")

                exit(0)

        d = {
            "onus": [onus.deviceRefId for onus in onus],
            "alarm_raised": index_alarms
        }

        state_pd = pd.DataFrame(d)
        state_pd["state"] = state
    else:
        if os.path.isfile("random.json"):
            state_pd = pd.read_json('random.json')

            if state == state_pd["state"].iloc[0]:
                print("Alarms not raised, wait for raising these")

                exit(0)

            state_pd = pd.read_json('random.json')

            onus = state_pd["onus"].apply(
                lambda x: next((onu for onu in topology.onus if onu.deviceRefId == x), None)
            )
            index_alarms = state_pd["alarm_raised"]

            state_pd["state"] = state
        else:
            print("Alarms not raised, wait for raising these")

            exit(0)

    print(f"Selected ONUS: {[onu.vaniRefId for onu in onus]}")

    for onu, index_alarm in zip(onus, index_alarms):
        alarm_to_raise = ALARMS[index_alarm]
        print(f"{state} alarm on onu {onu.vaniRefId}, OLT {onu.olt.host}:{onu.olt.port}")

        alarm_to_raise[1](onu.olt.host, onu.olt.port, onu.vaniRefId, state)

    state_pd.to_json('random.json')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('state', type=str, help='State of the alarm')
    args = parser.parse_args()

    if args.state not in ["raised", "cleared"]:
        print("Can Only accept a value between 'raised' and 'cleared'")
        exit(0)

    simulate_random(args.state)
