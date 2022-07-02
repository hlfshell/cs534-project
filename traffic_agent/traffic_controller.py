from __future__ import annotations
from typing import Any, Dict
from uuid import uuid4

from traffic_agent.sumo import Simulation

traffic_light: Dict[str, Any]

class TrafficAgent():

    def __init__(
        self,
    ):
        self._id = uuid4()
            
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
    
    def __eq__(self, other: TrafficAgent) -> bool:
        return self._id == other._id