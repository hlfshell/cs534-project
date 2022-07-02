from typing import Any, Dict, List
import traci

from traffic_agent.sumo import Simulation

traffic_light: Dict[str, Any]

class TrafficAgent():

    def __init__(
        self
    ):
        '''
        Note - a simulation must be active to create a TrafficAgent
        beccause it checks on existing traffic lights
        '''
        ids: List[str] = traci.trafficlight.getIDList()
        self.traffic_lights: Dict[str, Dict[str, int]] = {}
        for id in ids:
            self.traffic_lights[id] = {}
        self.get_traffic_lights()
    
    def _get_traffic_lights(self):
        for id in self.traffic_lights.keys():
            phase = traci.trafficlight.getPhase(id)
            duration = traci.trafficlight.getPhaseDuration(id)
            state = traci.trafficlight.getRedYellowGreenState(id)

            self.traffic_lights[id]["phase"] = phase
            self.traffic_lights[id]["duration"] = duration
            self.traffic_lights[id]["state"] = state

    def execute(self, simulation: Simulation) -> Dict[str, float]:
        while not simulation.complete():
            simulation.step()
            self.step()
        
        simulation.stop()
        stats = simulation.get_stats()
        simulation.shutdown()

        return stats

    def step(self):
        raise NotImplemented