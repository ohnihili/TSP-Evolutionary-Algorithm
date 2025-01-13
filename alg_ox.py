import sys
from Population import Population
from Crossover import Order
from PopMute import pop_mute
from FitnessProp import FitnessProportionalSelection
from ElitismSelection import ElitismSelection

# Validates that the population has no duplicate cities in any individual's tour
def validate_population(population):
    for individual in population.population:
        tsp_list = individual.tsp.list
        # Ensure that all cities in the tour are unique by converting the list to a set
        if len(tsp_list) != len(set(map(tuple, tsp_list))):
            raise ValueError(f"Duplicate cities found in individual: {individual.tsp.list}")

# Logs statistics about the population for the current generation
def log_population_stats(population, generation, log, mutation_prob, stagnant_generations, best_distance):
    # Find the best and worst individual based on distance (fitness measure)
    best_individual = min(population.population, key=lambda ind: ind.distance)
    worst_individual = max(population.population, key=lambda ind: ind.distance)
    
    # Calculate the average distance (fitness) of the population
    avg_distance = sum(ind.distance for ind in population.population) / len(population.population)
    
    # Count unique individuals by converting their tours to a set of tuples
    unique_individuals = len(set([tuple(map(tuple, ind.tsp.list)) for ind in population.population]))

    # Log generation data: best/worst/average distance, mutation probability, etc.
    log.write(f"--- Generation {generation} ---\n")
    log.write(f"Best Distance: {best_individual.distance}\n")
    log.write(f"Worst Distance: {worst_individual.distance}\n")
    log.write(f"Average Distance: {avg_distance}\n")
    log.write(f"Mutation Probability: {mutation_prob}\n")
    log.write(f"Stagnant Generations: {stagnant_generations}\n")
    log.write(f"Unique Individuals: {unique_individuals}\n\n")

# Main function to execute the evolutionary algorithm with Order crossover
def execute_alg_ox(data_name, pop_size, generations, mutation_prob, log_file):
    # Open a log file to record results throughout execution
    log = open(log_file, 'w')
    log.write(f"Algorithm Execution\nDataset: {data_name}\nPopulation Size: {pop_size}\nGenerations: {generations}\nMutation Prob: {mutation_prob}\n\n")

    # Initialize the population with a given dataset and fill it with individuals
    population = Population(pop_size, data_name)
    population.population = population.fill_pop(data_name)

    # Ensure the initial population has no invalid individuals
    validate_population(population)
    
    # Get the best individual from the initial population
    initial_best_individual = min(population.population, key=lambda ind: ind.distance)
    initial_best_distance = initial_best_individual.distance
    log.write(f"Initial Best Distance: {initial_best_distance}\n")

    # Variables to track the best distance achieved and the number of generations without improvement
    lowest_distance_achieved = initial_best_distance
    stagnant_generations = 0
    last_best_distance = initial_best_distance

    # Evolution loop, runs for the given number of generations
    for generation in range(generations):
        # Adaptive mutation probability, decreases linearly as generations progress
        mutation_prob = max(0.1, mutation_prob * (1 - generation / generations))

        # Create a new offspring population
        offspring = Population(pop_size)
        while len(offspring.population) < pop_size:
            # Select two parents using fitness proportional selection
            parent1, parent2 = FitnessProportionalSelection(population).select_multiple(2)
            # Create a child using Order crossover from the selected parents
            child1 = Order(parent1, parent2)
            # Add the child to the offspring population
            offspring.population.append(child1)

        # Apply mutation to the offspring population using insertion mutation
        pop_mute(offspring, "insert", mutation_prob)

        # Create a combined population of parents and offspring for selection
        combined_population = Population(pop_size * 2)
        combined_population.population = population.population.copy()
        combined_population.population.extend(offspring.population)

        # Apply elitism selection to choose the best individuals for the next generation
        elitism_selection = ElitismSelection(combined_population)
        elitism_selection.ElitismSelectionAlg()
        selected_survivors = elitism_selection.winner.population
        population.population = selected_survivors

        # Validate that no duplicates or invalid individuals are in the new population
        validate_population(population)

        # Get the best individual of the current generation
        best_individual = min(population.population, key=lambda ind: ind.distance)

        # Check for stagnation: If no improvement, increase stagnation count
        if best_individual.distance == last_best_distance:
            stagnant_generations += 1
        else:
            # Reset stagnation if improvement is made
            stagnant_generations = 0
            last_best_distance = best_individual.distance

        # Log statistics every 50 generations
        if generation % 50 == 0:
            log_population_stats(population, generation, log, mutation_prob, stagnant_generations, best_individual.distance)

        # Update the lowest distance achieved if an improvement is found
        if best_individual.distance < lowest_distance_achieved:
            lowest_distance_achieved = best_individual.distance

    # Final population logging and closing the log file
    final_best_individual = min(population.population, key=lambda ind: ind.distance)
    final_best_distance = final_best_individual.distance

    log.write(f"\n--- Final Results ---\n")
    log.write(f"Initial Best Distance: {initial_best_distance}\n")
    log.write(f"Lowest Distance Achieved: {lowest_distance_achieved}\n")
    log.write(f"Final Best Distance: {final_best_distance}\n")
    log.close()

# Entry point for running the algorithm with command-line arguments
if __name__ == "__main__":
    # Ensure the user provides enough command-line arguments
    if len(sys.argv) < 4:
        print("Usage: python alg_oxrun.py <data_name> <population_size> <iterations> <mutation_prob>")
        sys.exit(1)

    # Parse command-line arguments for dataset name, population size, generations, and mutation probability
    data_name = sys.argv[1]
    pop_size = int(sys.argv[2])
    generations = int(sys.argv[3])
    mutation_prob = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
    log_file = f"result_{data_name}_pop{pop_size}_gen{generations}.txt"

    # Execute the algorithm with the provided parameters
    execute_alg_ox(data_name, pop_size, generations, mutation_prob, log_file)
