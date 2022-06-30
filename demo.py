#!/usr/bin/env python

import os
import sys
import optparse

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

# contains TraCI control loop
def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        # det_vehs = traci.inductionloop.getLastStepVehicleIDs("det_0")
        # for veh in det_vehs:
        #     traci.vehicle.changeLane(veh, 2, 25)

        # step += 1

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
    options = get_options()

    # check binary
#    if options.nogui:
    sumoBinary = checkBinary('sumo')
#    else:
#   sumoBinary = checkBinardemoy('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "chicago/chicago.sumocfg"])#,
                            #  "--tripdemoinfo-output", "tripinfo.xml"])
    run()
