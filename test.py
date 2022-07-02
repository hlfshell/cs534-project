

from traffic_agent.sumo import Simulation
from traffic_agent.trainer import Trainer

simulation = Simulation("./chicago/chicago.sumocfg")

trainer = Trainer(
    simulation,
    50,
    iterations_per=1,
    population_size=50,
    mutation_rate=0.07,
    crossover=3
)

trainer.train()