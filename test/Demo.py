# import curses

import NewFiberCut
import PowerCut
import HighTemperature
import RandomTest

FIBERCUT_LETTER = 'F'
POWERCUT_LETTER = 'P'
HIGHTEMPERATURE_LETTER = 'T'
RANDOM_LETTER = 'R'
RAISE_LETTER = 'R'
CLEAR_LETTER = 'C'


SIMULATION = {
    f"{FIBERCUT_LETTER}_{RAISE_LETTER}": lambda: NewFiberCut.simulate_fiber_cut('raised'),
    f"{FIBERCUT_LETTER}_{CLEAR_LETTER}": lambda: NewFiberCut.simulate_fiber_cut('cleared'),
    f"{POWERCUT_LETTER}_{RAISE_LETTER}": lambda: PowerCut.simulate_power_cut('raised'),
    f"{POWERCUT_LETTER}_{CLEAR_LETTER}": lambda: PowerCut.simulate_power_cut('cleared'),
    f"{HIGHTEMPERATURE_LETTER}_{RAISE_LETTER}": lambda: HighTemperature.simulate_high_temperature('major'),
    f"{HIGHTEMPERATURE_LETTER}_{CLEAR_LETTER}": lambda: HighTemperature.simulate_high_temperature('cleared'),
    f"{RANDOM_LETTER}_{RAISE_LETTER}": lambda: RandomTest.simulate_random('raised'),
    f"{RANDOM_LETTER}_{CLEAR_LETTER}": lambda: RandomTest.simulate_random('cleared')
}


if __name__ == '__main__':
    print("Fiber Cut")
    print(f"\t{FIBERCUT_LETTER}_{RAISE_LETTER}: Raise a Fiber Cut")
    print(f"\t{FIBERCUT_LETTER}_{CLEAR_LETTER}: Clear a Fiber Cut")
    print("Power Cut")
    print(f"\t{POWERCUT_LETTER}_{RAISE_LETTER}: Raise a Power Cut")
    print(f"\t{POWERCUT_LETTER}_{CLEAR_LETTER}: Clear a Power Cut")
    print("High Temperature")
    print(f"\t{HIGHTEMPERATURE_LETTER}_{RAISE_LETTER}: Raise a High Temperature")
    print(f"\t{HIGHTEMPERATURE_LETTER}_{CLEAR_LETTER}: Clear a High Temperature")
    print("Random Test")
    print(f"\t{RANDOM_LETTER}_{RAISE_LETTER}: Raise a Random Test")
    print(f"\t{RANDOM_LETTER}_{CLEAR_LETTER}: Clear a Random Test")
    print("\n")
    print("Insert the list of simulation, for example, type {FIBERCUT_LETTER}_{RAISE_LETTER} to simulate fiber cut "
          "alarms.")

    simulation_list = []
    recap_list = []

    while True:
        simulations = input(f"Simulate {recap_list}: ")

        all_good = True
        for simulation in simulations.split(","):
            simulation_list.append(SIMULATION[simulation])
            recap_list.append(simulation)

            if simulation not in SIMULATION.keys():
                all_good = False

        if all_good:
            break

    print(recap_list)

    for index in range(len(simulation_list)):
        simulation_list[index]()
        print(f"Test {recap_list[index]} DONE")
        if index+1 == len(simulation_list):
            input(f"Press Enter to end the Demo...")
        else:
            input(f"Press Enter to continue to test {recap_list[index+1]}...")

    print("\nSimulation Ended")
