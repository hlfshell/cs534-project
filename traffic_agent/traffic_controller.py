from typing import Dict, List
import traci

from traffic_agent.sumo import Simulation

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
            self.traffic_lights[id]["phase"] = phase
            self.traffic_lights[id]["duration"] = duration

    def set_traffic_lights(self):
        for id in self.traffic_lights.keys():
            traci.trafficlight.setPhase(id, self.traffic_lights[id]["phase"])
            traci.trafficlight.setPhaseDuration(id, self.traffic_lights[id]["duration"])

    def step(self):
        raise NotImplemented
