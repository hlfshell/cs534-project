from __future__ import annotations
from random import uniform
import numpy as np

from collections import defaultdict
from typing import Dict, List
from traffic_agent.sumo import Simulation
from traffic_agent.traffic_controller import TrafficAgent


MIN_PHASE_DURATION = 10
MAX_PHASE_DURATION = 45


class NNAgent(TrafficAgent):

    def __init__(
        self,
        simulation: Simulation,
        hidden_layer_size=100,
        weights = None
    ):
        super().__init__()

        self.hidden_layer_size = hidden_layer_size
        
        if weights is not None:
            self.weights = weights
        else:
            self.weights: List[np.ndarray] = []

        self._prepare_network(simulation)

    def _prepare_network(self, simulation: Simulation):
        detectors = simulation.get_detectors()
        traffic_lights = self.simulation.get_traffic_lights()
        self.traffic_light_ids = traffic_lights

        input_size = len(detectors)
        output_size = len(traffic_lights)

        self.weights = [
            np.random.uniform(low=-1, high=1, size=(input_size, self.hidden_layer_size)),
            np.random.uniform(low=-1, high=1, size=(self.hidden_layer_size, output_size)),
        ]

    def infer(self):
        input = np.array([])

        hidden = relu(np.dot(input, self.weights[0]))

        output = sigmoid(np.dot(hidden, self.weights[1]))

        # output is a range from 0-1, so lets convert that
        # to our min/max phase duration
        durations: List[float] = [map(x) for x in output]

        return durations
    
    def step(self):
        pass

    def save(self):
        raise NotImplemented
    
    @classmethod
    def load(self) -> NNAgent:
        raise NotImplemented


# standard sigmoid activation function
def sigmoid(input):
    return 1/(1+np.exp(-input))


# Standard relu
def relu(x):
    return (x > 0) * x


def map(value) -> float:
    outMin = MIN_PHASE_DURATION
    outMax = MAX_PHASE_DURATION
    inMin = 0
    inMax = 1
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))


def mate(a: NNAgent, b: NNAgent, mutation_rate = 0.0) -> NNAgent:
    weights = []
    for index_weight, weight in enumerate(a.weights):
        new_weight = np.copy(weight)

        # Each weight layer is of size (input, output) so we have
        # to do two loops on it.
        for index_outer, new_weights in enumerate(weight):
            for index_inner, value in enumerate(new_weights):
                # Determine - parent a, parent b, or mutation?
                if uniform(0, 1) < mutation_rate:
                    new_weight[index_outer][index_inner] = uniform(-1, 1)
                elif uniform(0, 1) < 0.5: # Parent is A!
                    new_weight[index_outer][index_inner] = value
                else: # Parent is B!
                    new_weight[index_outer][index_inner] = b.weights[index_weight][index_outer][index_inner]

        weights.append(new_weight)

    return NNAgent(a.simulation, hidden_layer_size=a.hidden_layer_size, weights=weight)
