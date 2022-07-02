from typing import Any, Dict

from traffic_agent.sumo import Simulation

traffic_light: Dict[str, Any]

class TrafficAgent():

    def __init__(
        self,
    ):
        pass
            
    def execute(self, simulation: Simulation) -> Dict[str, float]:
        while not simulation.complete():
            simulation.step()
            self.step(simulation)
        
        simulation.stop()
        stats = simulation.get_stats()
        simulation.shutdown()

        return stats

    def step(self, simulation: Simulation):
        raise NotImplemented