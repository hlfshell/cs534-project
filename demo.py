#!/usr/bin/env python

import sys


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

# contains TraCI control loop
def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        step += 1
        traci.simulationStep()

        if step % 100 == 0:
            for id in traci.trafficlight.getIDList():
                print(f"{id} - {traci.trafficlight.getPhase(id)}")

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
    traci.start([sumoBinary, "-c", "sim/test.sumocfg"])
    run()
