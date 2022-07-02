


from typing import List
from traffic_agent.nn_agent import NNAgent
from traffic_agent.sumo import Simulation


class Trainer():

    def __init__(
        self,
        simulation: Simulation,
        generations: int,
        iterations_per: int = 1,
        population_size: int = 50,
        mutation_rate: float = 0.0,
    ):
        self.simulation = simulation
        self.generations = generations
        self.iterations_per = iterations_per
        self.population_size = population_size
        self.mutation_rate = mutation_rate

        self.population: List[NNAgent] = []

    def train(self):
        for i in range(0, self.generations):
            fitnesses = self.find_generation_fitness()

            # TODO - organize fitnesses - lowest score bet
            # Create mating pairs based on probability of ranking
            # And pass-through best N to the population without
            # changes
            self.mate()

    def find_generation_fitness(self) -> List[float]:
        fitnesses: List[float] = []
        for agent in self.population:
            iteration_fitnesses: List[float] = []
            for i in range(0, self.iterations_per):
                fitness = self.find_fitness(agent)
                iteration_fitnesses.append(fitness)
            fitness = sum(iteration_fitnesses)/len(iteration_fitnesses)

            fitnesses.append(fitness)

        return fitnesses

    def find_fitness(self, agent: NNAgent) -> float:
        stats = agent.execute(self.simulation)

        # Generate a fitness from the provided stats
        # For now I'll just use totalTravelTime
        fitness = stats['totalTravelTime']

        return fitness

    def save_population(self):
        pass