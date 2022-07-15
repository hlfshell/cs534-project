from __future__ import annotations
from math import floor
from random import uniform
from uuid import UUID
import numpy as np

import pickle

from typing import Dict, List
from traffic_agent.sumo import Simulation
from traffic_agent.traffic_controller import TrafficAgent

LAST_N_SAMPLES = 5
MIN_PHASE = 3

class IncrementalNNAgent(TrafficAgent):

    def __init__(
        self,
        simulation: Simulation,
        neurons_per_layer = 50,
        hidden_layers = 3,
        weights = None,
        id: UUID = None,
    ):
        '''
        Note - a simulation must be active to create a NNAgent
        beccause it checks on existing traffic lights and
        induction loops
        '''
        super().__init__()

        if id is not None:
            self._id = id

        self.neurons_per_layer = neurons_per_layer
        self.hidden_layers = hidden_layers
        
        if weights is not None:
            self.weights = weights
        else:
            self.weights: List[np.ndarray] = []
        
        self.detectors: Dict[str, Dict[str, List[float]]] = {}

        self._prepare_network(simulation)

    def _prepare_network(self, simulation: Simulation):
        detectors = simulation.get_detector_ids()

        for id in detectors:
            self.detectors[id] = {
                "speed": [],
                "occupancy": []
            }

        traffic_lights = simulation.get_traffic_light_ids()
        self.traffic_light_ids = traffic_lights
        self.traffic_lights = simulation.get_traffic_lights()

        if len(self.weights) == 0:
            input_size = 2*len(detectors) # For each detector, we take 2 stats
            # input_size = len(detectors) # For each detector, we take 2 stats
            output_size = len(traffic_lights)

            input_weights = np.random.uniform(low=-1, high=1, size=(input_size, self.neurons_per_layer))

            self.weights = [input_weights]
            for _ in range(0, self.hidden_layers):
                self.weights.append(
                    np.random.uniform(low=-1, high=1, size=(self.neurons_per_layer, self.neurons_per_layer))
                )

            output_weights = np.random.uniform(low=-1, high=1, size=(self.neurons_per_layer, output_size))

            self.weights.append(output_weights)

    def update_detectors(self, simulation: Simulation):
        detectors = simulation.get_detectors()
        for id in self.detectors.keys():
            speed = detectors[id]["speed"] / 100
            occupancy = detectors[id]["occupancy"] / 100
            self.detectors[id]["speed"].append(speed)
            if len(self.detectors[id]["speed"]) > LAST_N_SAMPLES:
                self.detectors[id]["speed"] = self.detectors[id]["speed"][0:LAST_N_SAMPLES]
            self.detectors[id]["occupancy"].append(occupancy)
            if len(self.detectors[id]["occupancy"]) > LAST_N_SAMPLES:
                self.detectors[id]["occupancy"] = self.detectors[id]["occupancy"][0:LAST_N_SAMPLES] 
            
    def infer(self, simulation: Simulation) -> List[float]:
        # Build the data array
        data = []

        for id in self.detectors.keys():
            speeds = self.detectors[id]["speed"]
            occupancies = self.detectors[id]["occupancy"]

            data.append(sum(speeds)/len(speeds))
            data.append(sum(occupancies)/len(occupancies))


        input = np.array(data)

        hidden = relu(np.dot(input, self.weights[0]))

        output = sigmoid(np.dot(hidden, self.weights[1]))

        return output
    
    def step(self, simulation: Simulation):
        # Update detector state
        self.update_detectors(simulation)
        
        # Get traffic light phase changes from NN
        changes = self.infer(simulation)
       
        # Increment traffic light phase if change > threshold
        for id in self.traffic_light_ids:
                    
            index = self.traffic_light_ids.index(id)
            change = changes[index]
                        
            #Increment counter
            self.traffic_lights[id]["counter"] = self.traffic_lights[id]["counter"] + 1
            
            #Update phases
            temp_phase = simulation.get_phase(id)            
            if self.traffic_lights[id]["phase"] != temp_phase:
                self.traffic_lights[id]["counter"] = 0
                self.traffic_lights[id]["phase"] = temp_phase
            
            # Increment phase if determined by NN and counter > MIN_PHASE                                 
            if change >= 0.5:                                
                if self.traffic_lights[id]["counter"] > MIN_PHASE:            
                    simulation.inc_traffic_light_phase(id)    
                    #temp_phase = 6

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
                "weights": self.weights,
                "neurons_per_layer": self.neurons_per_layer,
                "hidden_layers": self.hidden_layers
            }
            pickle.dump(data, file)
    
    @classmethod
    def load(self, filepath: str, simulation: Simulation) -> IncrementalNNAgent:
        with open(filepath, 'rb') as file:
            data = pickle.load(file)
            return IncrementalNNAgent(
                simulation,
                neurons_per_layer=data["neurons_per_layer"],
                hidden_layers=data["hidden_layers"],
                weights=data["weights"],
                id = data["id"]
            )

# standard sigmoid activation function
def sigmoid(input):
    return 1/(1+np.exp(-input))

# Standard relu
def relu(x):
    return (x > 0) * x

def mate(simulation, a: IncrementalNNAgent, b: IncrementalNNAgent, mutation_rate = 0.0) -> IncrementalNNAgent:
    simulation.start()
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

    return IncrementalNNAgent(simulation, neurons_per_layer=a.neurons_per_layer, hidden_layers=a.hidden_layers,weights=weight)
