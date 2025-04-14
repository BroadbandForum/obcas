import AlarmManager
import GetTopology
import RandomTest

import random
import pandas as pd
import argparse
import os


def simulate_power_cut(state):
    topology = GetTopology.Topology()
    topology.load_topology()

    power_distributions = []

    if state == "raised":
        pds = []
        for onu in topology.onus:
            pds.append(onu.powerDistributionArea)

        pds = list(set(pds))

        power_distributions = random.sample(pds, 1)
        d = {
            "power_distribution": power_distributions
        }

        if os.path.isfile("powerCut.json"):
            state_pd = pd.read_json('powerCut.json')

            if state == state_pd["state"].iloc[0]:
                print("Alarms already raised, wait for clearing these")

                exit(0)

        state_pd = pd.DataFrame(d)

        state_pd["state"] = state
    else:
        if os.path.isfile("powerCut.json"):
            state_pd = pd.read_json('powerCut.json')

            if state == state_pd["state"].iloc[0]:
                print("Alarms not raised, wait for raising these")

                exit(0)

            state_pd = pd.read_json('powerCut.json')
            power_distributions = state_pd["power_distribution"]

            state_pd["state"] = state
        else:
            print("Alarms not raised, wait for raising these")

            exit(0)

    print(f"Selected power_distributions: {power_distributions}")

    for power_distribution in power_distributions:
        for onu in topology.onus:
            if onu.powerDistributionArea == power_distribution:
                print(f"{state} alarm on onu {onu.vaniRefId}, OLT {onu.olt.host}:{onu.olt.port}")
                AlarmManager.power_cut(onu.olt.host, onu.olt.port, onu.vaniRefId, state)

    if os.path.isfile("noise_powerCut.json"):
        noise_state_df = pd.read_json('noise_powerCut.json')
    else:
        noise_state_df = pd.DataFrame()

    noise_state_df = RandomTest.generate_random_alarms(topology, state, noise_state_df)

    state_pd.to_json('powerCut.json')
    noise_state_df.to_json('noise_powerCut.json')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('state', type=str, help='State of the alarm')
    args = parser.parse_args()

    if args.state not in ["raised", "cleared"]:
        print("Can Only accept a value between 'raised' and 'cleared'")
        exit(0)

    simulate_power_cut(args.state)
