import os
from traffic_agent.nn_agent import NNAgent

from traffic_agent.sumo import Simulation
from traffic_agent.trainer import Trainer

simulation = Simulation("./chicago/chicago.sumocfg")
simulation.start()

population = []

# population_directory = "populations/population_2"
# for filepath in os.listdir(population_directory):
#     print(filepath)
#     population.append(NNAgent.load(filepath, simulation))
    
trainer = Trainer(
    simulation,
    10,
    iterations_per=1,
    population_size=10,
    mutation_rate=0.007,
    crossover=2,
    population = population
)

trainer.train()