# -*- coding: utf-8 -*-
"""
CS 594, Porject Group 1

@author: Jesse Morzel
"""

"""
Define imports - standard packages
"""
import os, sys


"""
Define imports - custom packages
"""
import traci
import traci.constants as tc

"""
SUMO Variables
"""
sumoBinary = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", "C:/Users/jesse/Sumo/Chicago_01_Edit_01.sumocfg"]


"""
Custom functions
"""  


"""
Main Function
"""
def main():
    
    # Check for SUMO_HOME
     if 'SUMO_HOME' in os.environ:
         tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
         sys.path.append(tools)
     else:
         sys.exit("please declare environment variable 'SUMO_HOME'")
     
    # TraCI Simulation
     traci.start(sumoCmd)
     step = 0
     print(traci.trafficlight.getIDList())
     while step < 1000:
         traci.simulationStep()
         
         """
         Example commands
         """         
         #if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
         #    traci.trafficlight.setRedYellowGreenState("0","GrGr")
         
         # Get list of vehicle IDs
         #print(traci.vehicle.getIDList())
         
         # Count number of vehicles
         #print(traci.vehicle.getIDCount())
         
         # Get list of traffic light
         # print(traci.trafficlight.getIDList())
         
         # Set traffic light state
         traci.trafficlight.setPhase("27446709", 0)
         traci.trafficlight.setPhase("27446710", 0)
         traci.trafficlight.setPhase("27446719", 0)
         traci.trafficlight.setPhase("27446720", 0)
         traci.trafficlight.setPhase("27446756", 0)
         
         traci.trafficlight.setPhase("27477586", 0)
         traci.trafficlight.setPhase("27477590", 0)
         traci.trafficlight.setPhase("27477591", 0)
         traci.trafficlight.setPhase("28289299", 0)
         traci.trafficlight.setPhase("28289310", 0)
         
         traci.trafficlight.setPhase("28289318", 0)
         traci.trafficlight.setPhase("28289857", 0)
         traci.trafficlight.setPhase("28289874", 0)
         traci.trafficlight.setPhase("28289897", 0)
         traci.trafficlight.setPhase("28290256", 0)
         
         traci.trafficlight.setPhase("28290277", 0)
         traci.trafficlight.setPhase("28290281", 0)
         traci.trafficlight.setPhase("28290296", 0)
         
         if step > 500:
             traci.trafficlight.setPhase("27446709", 2)
             traci.trafficlight.setPhase("27446710", 2)
             traci.trafficlight.setPhase("27446719", 2)
             traci.trafficlight.setPhase("27446720", 2)
             traci.trafficlight.setPhase("27446756", 2)
             
             traci.trafficlight.setPhase("27477586", 2)
             traci.trafficlight.setPhase("27477590", 2)
             traci.trafficlight.setPhase("27477591", 2)
             traci.trafficlight.setPhase("28289299", 2)
             traci.trafficlight.setPhase("28289310", 2)
             
             traci.trafficlight.setPhase("28289318", 2)
             traci.trafficlight.setPhase("28289857", 2)
             traci.trafficlight.setPhase("28289874", 2)
             traci.trafficlight.setPhase("28289897", 2)
             traci.trafficlight.setPhase("28290256", 2)
             
             traci.trafficlight.setPhase("28290277", 2)
             traci.trafficlight.setPhase("28290281", 2)
             traci.trafficlight.setPhase("28290296", 2)
         
         
         step += 1
         
     traci.close()

    
if __name__ == "__main__":
    main()
