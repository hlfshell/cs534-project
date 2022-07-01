#!/usr/bin/env python

from collections import defaultdict
from random import choice, randint
import sys
from typing import Dict


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


# Marks when the traffic light was swapped phase last
traffic_light_steps: Dict[str, int] = defaultdict(lambda: 0)

def get_light_duration() -> int:
    return randint(15, 40)

# contains TraCI control loop
def run():
    step = 0

    # Set the phase lights to random values (0, 1, 2)
    # for initial setup
    for id in traci.trafficlight.getIDList():
        traci.trafficlight.setPhase(id, choice([0, 1, 2]))
        traci.trafficlight.setPhaseDuration(id, 90)
        traffic_light_steps[id] = get_light_duration()


    while traci.simulation.getMinExpectedNumber() > 0:
        step += 1
        traci.simulationStep()

        # increment each step count for the traffic light
        for id in traci.trafficlight.getIDList():
            traffic_light_steps[id] -= 1
            if traffic_light_steps[id] <= 0:
                # Now swap it to the next phase, resetting
                # from 3 -> 0
                traffic_light_steps[id] = 0
                current_phase = traci.trafficlight.getPhase(id)
                next_phase = (current_phase + 1) % 3
                duration = get_light_duration()
                print(f"Changing traffic light {id} from {current_phase} to {next_phase} for {duration} seconds")
                traci.trafficlight.setPhase(id, next_phase)
                traci.trafficlight.setPhaseDuration(id, 90)
                traffic_light_steps[id] = duration

    print("Vehicles")
    vehicle_ids = traci.vehicle.getIDList()
    for vehicle_id in vehicle_ids:
        results = traci.vehicle.getSubscriptionResults(vehicle_id)
        print(f"{vehicle_id}>>{results}")

    print("Routes")
    route_ids = traci.route.getIDList()
    print(route_ids)
    for route_id in route_ids:
        results = traci.route.getSubscriptionResults(route_id)
        print(f"{route_id}>>{results}")

    traci.close()
    sys.stdout.flush()


# main entry point
if __name__ == "__main__":

    sumoBinary = checkBinary('sumo')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "sim/test.sumocfg"])#,
                            #  "--tripdemoinfo-output", "tripinfo.xml"])
    run()
