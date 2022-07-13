from pathlib import Path
from random import choices
from typing import List
from traffic_agent.nn_agent import NNAgent, mate
from traffic_agent.sumo import Simulation


class Trainer():

    def __init__(
        self,
        simulation: Simulation,
        generations: int,
        iterations_per: int = 1,
        population_size: int = 50,
        mutation_rate: float = 0.0,
        crossover: int = 0,
        population: List[NNAgent] = []
    ):
        self.simulation = simulation
        self.generations = generations
        self.iterations_per = iterations_per
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover = crossover

        self.population: List[NNAgent] = population
        if len(population) == 0:
            simulation.start()
            while len(self.population) < self.population_size:
                self.population.append(NNAgent(simulation))
            simulation.shutdown()

    def train(self):
        fitnesses: List[float] = []
        for generation in range(0, self.generations):
            print("****************************************************")
            print(f"Starting Generation {generation+1}")
            print("****************************************************")
            fitnesses = self.find_generation_fitness(fitnesses=fitnesses)

            # The fitness index is equivalent to the
            # population index, so we must sort both
            # equvialently to do this right
            fitness_population = zip(fitnesses, self.population)
            sorted_fitness_population = sorted(fitness_population)

            fitness_scores = [x[0] for x in sorted_fitness_population]
            self.population = [x[1] for x in sorted_fitness_population]

            # Save the best agent and the entire population
            best_file_path = f"best_model_generation_{generation+1}.pk"
            population_folder = f"populations/population_{generation+1}"
            Path(population_folder).mkdir(parents=True, exist_ok=True)

            self.population[0].save(best_file_path)
            for index, agent in enumerate(self.population):
                agent.save(f"{population_folder}/agent_{index}.pk")

            # Now that we have our fittest, save the fittest and announce
            # it
            print("****************************************************")
            print(f"Generation {generation+1} results:")
            print(f"Healthiest agent is {self.population[0]._id} with a fitness of {fitness_scores[0]}")
            print(f"Average fitness was {sum(fitness_scores)/len(fitness_scores)}")
            print(f"Worst score was {fitness_scores[-1]}")
            print(f"Best agent saved to {best_file_path}; population saved to {population_folder}")
            print("****************************************************")

            # Now it's time for the networks to produce the next generation

            # Our weighted probability of choosing a fitness score
            # is based upon the lowest fitness score, but we want
            # that to have the highest weight. So we need to take the
            # inverse of that score to offset the weight.
            weighted_fitness_scores = [1/(x**2) for x in fitness_scores]

            new_population: List[NNAgent] = []
            if self.crossover > 0:
                new_population = self.population[0:self.crossover]
                fitnesses = fitness_scores[0:self.crossover]
            else:
                # If we're not doing crossover, we need to just reset
                # fitnesses
                fitnesses = []
            
            while len(new_population) < self.population_size:
                a = choices(self.population, weights=weighted_fitness_scores)[0]
                b = None
                while b != a:
                    b = choices(self.population, weights=weighted_fitness_scores)[0]

                agent = mate(self.simulation, a, b, self.mutation_rate)
                new_population.append(agent)

    def find_generation_fitness(self, fitnesses: List[float] =[]) -> List[float]:
        fitnesses_starting_length = len(fitnesses)
        for index, agent in enumerate(self.population):
            # This is to prevent retraining agents that
            # were brought on for being the best in prior
            # generations
            if index < fitnesses_starting_length:
                continue
            iteration_fitnesses: List[float] = []
            for _ in range(0, self.iterations_per):
                print(f"Finding fitness for agent {agent._id}")
                fitness = self.find_fitness(agent)
                iteration_fitnesses.append(fitness)

            fitness = sum(iteration_fitnesses)/len(iteration_fitnesses)

            fitnesses.append(fitness)

        return fitnesses

    def find_fitness(self, agent: NNAgent) -> float:
        self.simulation.start()
        stats = agent.execute(self.simulation)

        # Generate a fitness from the provided stats
        # For now I'll just use totalTravelTime
        fitness = stats['totalTravelTime']

        self.simulation.shutdown()

        return fitness

    def save_population(self):
        pass