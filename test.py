

from traffic_agent.sumo import Simulation
from traffic_agent.trainer import Trainer

simulation = Simulation("./sim/test.sumocfg")

trainer = Trainer(
    simulation,
    20,
    iterations_per=1,
    population_size=10,
    mutation_rate=0.07,
    crossover=1
)

trainer.train()