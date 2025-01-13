# Fitness-Prop.py

from Population import Population
import random

class FitnessProportionalSelection:
    def __init__(self, population):
        self.population = population  #population object containing list of individual objects
        self.total_fitness = self.calculate_total_fitness()

    def calculate_total_fitness(self):
        # sum of population fitness score
        total_fitness = 0
        for individual in self.population.population:
            if individual.distance == 0:
                print(f"Zero distance found for individual: {individual.tsp.list}")  # Trace output for zero distance
                total_fitness += 1e-6  # Assign a small fitness value for zero distance
            else:
                total_fitness += 1 / individual.distance  # Lower distance == more fit
        return total_fitness


    def select_individual(self):
        # Individual selection based on fitness-prop
        selection_point = random.uniform(0, self.total_fitness)
        current_sum = 0
        
        for individual in self.population.population:
            if individual is None or individual.distance == 0:
                continue  # Skip invalid individuals
            current_sum += 1 / individual.distance  # sum of scores
            if current_sum >= selection_point:
                return individual
        return None  # Return None if no valid individual is found

    def select_multiple(self, num_selections):
        # Individuals selected based on fitness-prop
        selected_individuals = []
        for _ in range(num_selections):
            individual = self.select_individual()
            if individual is not None:
                selected_individuals.append(individual)
        
        # Ensure we have exactly num_selections individuals
        while len(selected_individuals) < num_selections:
            # If not enough individuals, select randomly from the population
            selected_individuals.append(random.choice(self.population.population))

        return selected_individuals


# Testing code
if __name__ == "__main__":
    
    pop = Population(5, "eil51")
    # pop = Population(5, "eil76")
    # pop = Population(5, "eil101")
    # pop = Population(5, "kroA100")
    # pop = Population(5, "kroC100")
    # pop = Population(5, "lin105")
    # pop = Population(5, "pcb442")
    # pop = Population(5, "pr2392")
    # pop = Population(5, "st70")
    # pop = Population(5, "usa13509")

    fps = FitnessProportionalSelection(pop)
    
    # Select individual using fitness-prop method
    selected = fps.select_individual()
    print("Selected individual with distance:", selected.distance)
    
    # Select multiple individuals using fitness-prop metho
    selected_multiple = fps.select_multiple(3)
    print("Selected multiple individuals:")
    for ind in selected_multiple:
        print(ind.distance)
