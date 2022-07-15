import os
from traffic_agent.averaged_nn_agent import AveragedNNAgent
from traffic_agent.averaged_nn_agent import mate as averaged_mate
from traffic_agent.incremental_nn_agent import IncrementalNNAgent
from traffic_agent.nn_agent import NNAgent

from traffic_agent.sumo import Simulation
from traffic_agent.trainer import Trainer

simulation = Simulation("./chicago_02/chicago_02.sumocfg", gui=False)
simulation.start()

population = []

# population_directory = "populations/population_14"
# print(f"Loading population from {population_directory}")
# for filepath in os.listdir(population_directory):
#     population.append(NNAgent.load(f"{population_directory}/{filepath}", simulation))

trainer = Trainer(
    simulation,
    10,
    iterations_per=1,
    population_size=10,
    mutation_rate=0.05,
    crossover=2,
    population=population,
    agent=IncrementalNNAgent,
    mate=averaged_mate
)

trainer.train()