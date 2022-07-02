


from typing import List
from traffic_agent.nn_agent import NNAgent


class Trainer():

    def __init__(
        self,
        generations: int,
        iterations_per: int = 1,
        population_size: int = 50,
        mutaton_rate: float = 0.0,
    ):
        self.population: List[NNAgent] = []
        pass

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
        pass

    def save_population(self):
        pass