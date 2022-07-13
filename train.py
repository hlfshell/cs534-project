import os
from traffic_agent.nn_agent import NNAgent

from traffic_agent.sumo import Simulation
from traffic_agent.trainer import Trainer

simulation = Simulation("./chicago/chicago.sumocfg")
simulation.start()

population = []

# population_directory = "populations/population_14"
# print(f"Loading population from {population_directory}")
# for filepath in os.listdir(population_directory):
#     population.append(NNAgent.load(f"{population_directory}/{filepath}", simulation))
    
trainer = Trainer(
    simulation,
    25,
    iterations_per=1,
    population_size=20,
    mutation_rate=0.05,
    crossover=2,
    population=population
)

trainer.train()