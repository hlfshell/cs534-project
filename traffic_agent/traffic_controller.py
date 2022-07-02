from typing import Dict, List
import traci

from traffic_agent.sumo import Simulation

traffic_light: Dict[str, Any]

class TrafficAgent():

    def __init__(
        self,
        simulation: Simulation
    ):
        self.simulation = simulation
        
        ids: List[str] = traci.trafficlight.getIDList()
        self.traffic_lights: Dict[str, Dict[str, int]] = {}
        for id in ids:
            self.traffic_lights[id] = {}
        self.get_traffic_lights()
    
    def get_traffic_lights(self):
        for id in self.traffic_lights.keys():
            phase = traci.trafficlight.getPhase(id)
            duration = traci.trafficlight.getPhaseDuration(id)
            state = traci.trafficlight.getRedYellowGreenState(id)

            self.traffic_lights[id]["phase"] = phase
            self.traffic_lights[id]["duration"] = duration
            self.traffic_lights[id]["state"] = state

    def set_traffic_lights(self):
        for id in self.traffic_lights.keys():
            traci.trafficlight.setPhase(id, self.traffic_lights[id]["phase"])
            traci.trafficlight.setPhaseDuration(id, self.traffic_lights[id]["duration"])

    def step(self):
        raise NotImplemented
