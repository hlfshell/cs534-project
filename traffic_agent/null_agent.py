from __future__ import annotations

from traffic_agent.sumo import Simulation
from traffic_agent.traffic_controller import TrafficAgent


class NullAgent(TrafficAgent):

    def __init__(
        self,
    ):
        super().__init__()

    def step(self, simulation: Simulation):
        pass
