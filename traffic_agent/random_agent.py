from __future__ import annotations
from random import uniform

from typing import List
from traffic_agent.sumo import Simulation
from traffic_agent.traffic_controller import TrafficAgent


MIN_PHASE_DURATION = 3
MAX_PHASE_DURATION = 20


class RandomAgent(TrafficAgent):

    def __init__(
        self,
        simulation: Simulation,
    ):
        '''
        Note - a simulation must be active to create a NNAgent
        beccause it checks on existing traffic lights and
        induction loops
        '''
        super().__init__()

        traffic_lights = simulation.get_traffic_light_ids()
        self.traffic_light_ids = traffic_lights
        self.traffic_lights = simulation.get_traffic_lights()

    def step(self, simulation: Simulation):
        for id in self.traffic_light_ids:
            # Decrement each traffic light duration by one, as
            # one step is one second. For each that are set to
            # zero, grab the current network's duration setting
            # for it.
            self.traffic_lights[id]["duration"] -= 1
            
            if self.traffic_lights[id]["duration"] <= -1:  
                index = self.traffic_light_ids.index(id)
                duration = uniform(MIN_PHASE_DURATION, MAX_PHASE_DURATION)
                self.traffic_lights[id]["duration"] = duration
                simulation.set_traffic_light_duration(id, duration)
