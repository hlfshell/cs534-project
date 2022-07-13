from __future__ import annotations
from time import perf_counter
from typing import Any, Dict
from uuid import uuid4

from traffic_agent.sumo import Simulation


MAX_ALLOWED_STEPS = 5000
PRINT_EVERY = 250
# MAX_ALLOWED_STEPS = 100 # For testing


class TrafficAgent():

    def __init__(
        self,
    ):
        self._id = uuid4()
            
    def execute(self, simulation: Simulation) -> Dict[str, float]:
        steps = 0
        simulation_times = 0.0
        agent_times = 0.0
        while not simulation.complete():
            steps += 1
            if steps % PRINT_EVERY == 0:
                print(f"Step {steps}")
                print(f"Average of {simulation_times/PRINT_EVERY}s per simulation step and {agent_times/PRINT_EVERY}s per agent step")
                simulation_times = 0.0
                agent_times = 0.0
            if steps >= MAX_ALLOWED_STEPS:
                print(f"Exceeded max steps allowed - {MAX_ALLOWED_STEPS}")
                break
            start_simulation = perf_counter()
            simulation.step()
            end_simulation = perf_counter()
            self.step(simulation)
            end_agent = perf_counter()

            simulation_times += end_simulation - start_simulation
            agent_times += end_agent - end_simulation
        
        simulation.stop()
        stats = simulation.get_stats()
        print("STATS", stats)
        simulation.shutdown()

        return stats

    def step(self, simulation: Simulation):
        raise NotImplemented
    
    def __eq__(self, other: TrafficAgent) -> bool:
        if other == None:
            return False
        return self._id == other._id