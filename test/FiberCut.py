import AlarmManager
import GetTopology
import RandomTest

import random
import pandas as pd
import argparse
import os


def simulate_fiber_cut(state, level = 1):
    topology = GetTopology.Topology()
    topology.load_topology()

    cut_splitters = []

    if level == 1:
        if state == "raised":
            splv1s = []
            for onu in topology.onus:
                splv1s.append(onu.splitter1)

            splv1s = list(set(splv1s))

            cut_splitters = random.sample(splv1s, random.randint(1, 3))
            d = {
                "splitters": cut_splitters
            }

            if os.path.isfile("fiberCut.json"):
                state_pd = pd.read_json('fiberCut.json')

                if state == state_pd["state"].iloc[0]:
                    print("Alarms already raised, wait for clearing them")

                    exit(0)

            state_pd = pd.DataFrame(d)

            state_pd["state"] = state
        else:
            if os.path.isfile("fiberCut.json"):
                state_pd = pd.read_json('fiberCut.json')

                if state == state_pd["state"].iloc[0]:
                    print("Alarms not raised, wait for raising them")

                    exit(0)

                state_pd = pd.read_json('fiberCut.json')
                cut_splitters = state_pd["splitters"].to_list()

                state_pd["state"] = state
            else:
                print("Alarms not raised, wait for raising them")

                exit(0)
    else:
        if os.path.isfile("fiberCut.json"):
            state_pd = pd.read_json('fiberCut.json')
        else:
            print("Before need to run level 1")

            exit(0)

        cut_splitters = state_pd["splitters"].to_list()

        selected_splitters = random.sample(cut_splitters, random.randint(1, 1))

        splitter2 = ''
        for onu in topology.onus:
            if onu.splitter1 == selected_splitters[0]:
                splitter2 = onu.splitter2

        cut_splitters = []
        for onu in topology.onus:
            if onu.splitter2 == splitter2:
                if onu.splitter1 == selected_splitters:
                    continue

                cut_splitters.append(onu.splitter1)

        for cut_splitter in cut_splitters:
            state_pd.append({"splitters": cut_splitter, "state": state})

    print(f"Selected cut_splitter: {cut_splitters}")

    for cut_splitter in cut_splitters:
        for onu in topology.onus:
            if onu.splitter1 == cut_splitter:
                print(f"{state} alarm on onu {onu.vaniRefId}, OLT {onu.olt.host}:{onu.olt.port}")
                AlarmManager.fiber_cut(onu.olt.host, onu.olt.port, onu.vaniRefId, state)

    if os.path.isfile("noise_fiberCut.json"):
        noise_state_df = pd.read_json('noise_fiberCut.json')
    else:
        noise_state_df = pd.DataFrame()

    if state == 'raised':
        topology = topology

    noise_state_df = RandomTest.generate_random_alarms(topology, state, noise_state_df)

    state_pd.to_json('fiberCut.json')
    noise_state_df.to_json('noise_fiberCut.json')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('state', type=str, help='State of the alarm')
    parser.add_argument('level', type=int, help='State of the alarm', default=1)
    args = parser.parse_args()

    if args.state not in ["raised", "cleared"]:
        print("Can Only accept a value between 'raised' and 'cleared'")
        exit(0)

    if args.level not in [1, 2]:
        print("Can only accept value between 1 and 2")

    simulate_fiber_cut(args.state, args.level)
