from __future__ import annotations
from random import uniform
import sched
from uuid import UUID

import pickle

from typing import Dict, List
from traffic_agent.sumo import Simulation
from traffic_agent.traffic_controller import TrafficAgent


MIN_PHASE_DURATION = 3
MAX_PHASE_DURATION = 25


class ScheduleAgent(TrafficAgent):

    def __init__(
        self,
        simulation: Simulation,
        id: UUID = None,
        schedule: Dict[str, Dict[str, List[float]]] = None
    ):
        '''
        Note - a simulation must be active to create a NNAgent
        beccause it checks on existing traffic lights and
        induction loops
        '''
        super().__init__()

        if id is not None:
            self._id = id

        self.schedule = schedule
        if self.schedule is None:
            self.schedule = {}
            lights = simulation.get_light_durations()
            for id in lights.keys():
                phases = lights[id]
                for phase in phases:
                    phase["duration"] = uniform(MIN_PHASE_DURATION, MAX_PHASE_DURATION)
                self.schedule[id] = phases

        self.traffic_lights = simulation.get_traffic_lights()
        self.traffic_light_ids = simulation.get_traffic_light_ids()

    def step(self, simulation: Simulation):
        for id in self.traffic_light_ids:
            # Decrement each traffic light duration by one, as
            # one step is one second. For each that are set to
            # zero, grab the current network's duration setting
            # for it.
            self.traffic_lights[id]["duration"] -= 1
            
            if self.traffic_lights[id]["duration"] <= -1:  
                index = simulation.get_traffic_light_phase(id)
                duration = self.schedule[id][index]["duration"]
                simulation.set_traffic_light_duration(id, duration)
                self.traffic_lights[id]["duration"] = duration

    def save(self, filepath: str):
        '''
        This serializes the agent and writes it to the file
        Generally the only thing we need to save an agent
        is its weights. Due to lack of time we'll use
        pickle, as problematic as that is. 
        '''
        with open(filepath, 'wb') as file:
            data = {
                "id": self._id,
                "schedule": self.schedule
            }
            pickle.dump(data, file)
    
    @classmethod
    def load(self, filepath: str, simulation: Simulation) -> ScheduleAgent:
        with open(filepath, 'rb') as file:
            data = pickle.load(file)
            return ScheduleAgent(
                simulation,
                id = data["id"],
                schedule = data["schedule"]
            )


def mate(simulation, a: ScheduleAgent, b: ScheduleAgent, mutation_rate = 0.0) -> ScheduleAgent:
    simulation.start()
    schedule: Dict[str, Dict[str, List[float]]] = {}

    for id in a.schedule.keys():
        schedule[id] = []
        for index, phase in enumerate(a.schedule[id]):
            # Determine - parent a, parent b, or mutation?
            if uniform(0, 1) < mutation_rate:
                schedule[id].append({ "duration": uniform(MIN_PHASE_DURATION, MAX_PHASE_DURATION) })                
            elif uniform(0, 1) < 0.5: # Parent is A!
                schedule[id].append({ "duration": phase["duration"] })
            else: # Parent is B!
                schedule[id].append({ "duration": b.schedule[id][index]["duration"] })

    return ScheduleAgent(simulation, schedule=schedule)
