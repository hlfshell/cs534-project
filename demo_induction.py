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
            print("Step: ", step)
            for id in traci.trafficlight.getIDList():
                print(f"{id} - {traci.trafficlight.getPhase(id)}")
        
        # Collect induction data        
        if traci.inductionloop.getLastStepVehicleNumber("L00_3_0") > 0:
            print("Vehicle at J0, West, Lane 0")
        if traci.inductionloop.getLastStepVehicleNumber("L01_0_1") > 0:
            print("Vehicle at J1, North, Lane 1")
        if traci.inductionloop.getLastStepVehicleNumber("L02_3_2") > 0:
            print("Vehicle at J2, West, Lane 2")
        if traci.inductionloop.getLastStepVehicleNumber("L04_2_0") > 0:
            print("Vehicle at J3, South, Lane 0")

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

    print("Total Steps: ", step)
    traci.close()
    sys.stdout.flush()


# main entry point
if __name__ == "__main__":

    sumoBinary = checkBinary('sumo')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "chicago/chicago.sumocfg"])
    run()
