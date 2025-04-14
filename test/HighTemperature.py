import AlarmManager
import GetTopology
import RandomTest

import random
import pandas as pd
import argparse

import os


def simulate_high_temperature(state):
    topology = GetTopology.Topology()
    topology.load_topology()

    cabinets = []

    if state == "major":
        cabinets = []
        for olt in topology.olts:
            cabinets.append(olt.cabinet)

        cabinets = list(set(cabinets))

        cabinets = random.sample(cabinets, 1)
        d = {
            "cabinets": cabinets
        }

        if os.path.isfile("highTemperature.json"):
            state_pd = pd.read_json('highTemperature.json')

            if state == state_pd["state"].iloc[0]:
                print("Alarms already raised, wait for clearing these")

                exit(0)

        state_pd = pd.DataFrame(d)

        state_pd["state"] = state
    else:
        if os.path.isfile("highTemperature.json"):
            state_pd = pd.read_json('highTemperature.json')

            if state == state_pd["state"].iloc[0]:
                print("Alarms not raised, wait for raising these")

                exit(0)

            state_pd = pd.read_json('highTemperature.json')
            cabinets = state_pd["cabinets"]

            state_pd["state"] = state
        else:
            print("Alarms not raised, wait for raising these")

            exit(0)

    print(f"Selected cabinets: {cabinets}")

    for cabinet in cabinets:
        for olt in topology.olts:
            if olt.cabinet == cabinet:
                resource = olt.resources[0]
                print(f"{state} alarm on resource {resource}, OLT {olt.host}:{olt.port}")

                AlarmManager.high_temperature(
                    olt.host,
                    olt.port,
                    resource,
                    state,
                    "The internal temperature has exceeded the high level"
                )

    if os.path.isfile("noise_highTemperature.json"):
        noise_state_df = pd.read_json('noise_highTemperature.json')
    else:
        noise_state_df = pd.DataFrame()

    if state == 'major':
        noise_state_df = RandomTest.generate_random_alarms(topology, 'raised', noise_state_df)
    else:
        noise_state_df = RandomTest.generate_random_alarms(topology, state, noise_state_df)

    state_pd.to_json('highTemperature.json')
    noise_state_df.to_json('noise_highTemperature.json')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('state', type=str, help='State of the alarm')
    args = parser.parse_args()

    if args.state not in ["major", "cleared"]:
        print("Can Only accept a value between 'major' and 'cleared'")
        exit(0)

    simulate_high_temperature(args.state)
