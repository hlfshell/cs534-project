from __future__ import annotations
from math import floor
from uuid import UUID
import numpy as np

import pickle

import numpy as np
import torch

from torch import nn

from typing import Dict, List
from traffic_agent.activation_functions import relu, sigmoid
from traffic_agent.sumo import Simulation
from traffic_agent.traffic_controller import TrafficAgent


MIN_PHASE_DURATION = 3
MAX_PHASE_DURATION = 20

HISTORY = 5


class DeepQNetwork(nn.Module):

    def __init__(self, simulation: Simulation):
        super(DeepQNetwork, self).__init__()

        # Our simple NN model checks the observation space
        # being passed - which is the inductors.
        # Our output is the action space state, which is whether
        # or not to change the phase of the light.
        detectors = simulation.get_detector_ids()
        traffic_lights = simulation.get_traffic_light_ids()
        input_size = 2*HISTORY*len(detectors) # For each detector, we take 2 stats
        output_size = len(traffic_lights)

        # Now we create a simple sequential NN
        self.model = nn.Sequential(
            # Input 
            nn.Linear(input_size, 64),
            nn.ReLU(),

            nn.Linear(64, 64),
            nn.ReLU(),

            # Output
            nn.Linear(64, output_size),
        )
    
    def forward(self, x):
        return self.model(x)
    
    def save(self, filepath: str):
        torch.save(self.state_dict(), filepath)
    
    def load(self, filepath: str):
        self.load_state_dict(torch.load(filepath))


class DeepQAgent(TrafficAgent):

    def __init__(
        self,
        simulation: Simulation,
        model: DeepQNetwork = None
    ):
        '''
        Note - a simulation must be active to create a NNAgent
        beccause it checks on existing traffic lights and
        induction loops
        '''
        super().__init__()

        if id is not None:
            self._id = id
        
        self.traffic_light_ids = simulation.get_traffic_light_ids()

        detectors = simulation.get_detector_ids()
        self.input_size = 2*HISTORY*len(detectors)

        # Setup a blank history
        self.history: List[float] = []
        for _ in range(0, self.input_size):
            self.history.append(0)
    
        if model is None:
            self.model = DeepQNetwork(simulation)
        else:
            model = model

    def infer(self, simulation: Simulation) -> List[float]:
        # Build the data array
        data = []
        detectors = simulation.get_detectors()
        for id in detectors.keys():
            data.append(detectors[id]["speed"] / 10)
            data.append(detectors[id]["occupancy"] / 100)
        
        self.history += data
        self.history = self.history[-self.input_size:]

        input = torch.from_numpy(np.array(self.history)).float()

        Q = self.model.forward(input)

        q_values = Q.data.numpy()

        return q_values
    
    def step(self, simulation: Simulation):
        # Update detector state
        self.update_detectors(simulation)

        # Get traffic light phase changes from NN
        changes = self.infer(simulation)

        # Increment traffic light phase if change > threshold
        for id in self.traffic_light_ids:
            index = self.traffic_light_ids.index(id)
            change = changes[index]

            if change >= 0.5:
                simulation.increment_traffic_phase(id)

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
    def load(self, filepath: str, simulation: Simulation) -> AveragedNNAgent:
        with open(filepath, 'rb') as file:
            data = pickle.load(file)
            return AveragedNNAgent(
                simulation,
                neurons_per_layer=data["neurons_per_layer"],
                hidden_layers=data["hidden_layers"],
                weights=data["weights"],
                id = data["id"]
            )