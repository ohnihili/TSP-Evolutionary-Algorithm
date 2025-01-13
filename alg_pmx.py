import sys
import math
import time
from Population import Population
from Crossover import PMX
from ElitismSelection import ElitismSelection
from PopMute import pop_mute

# Main function to execute the evolutionary algorithm using PMX (Partially Mapped Crossover)
def execute_alg(data_name, pop_size, iteration: int, debug:bool = False):
    # Independent variables
    duration = 7200  # Maximum runtime duration set to 2 hours (7200 seconds)
    start_time = time.time()  # Record the start time of execution

    # Initialize population and selection mechanism
    pop_alg = Population(pop_size, data_name)  # Create the population with the given size and dataset
    alg_sel = ElitismSelection(pop_alg, debug=debug)  # Initialize the ElitismSelection mechanism
    
    # Debug coloring setup (for terminal output coloring)
    if debug:
        R = '\033[31m'  # Red for highlighting bad results
        G = '\033[32m'  # Green for success
        B = '\033[34m'  # Blue for neutral output
        RESET = '\033[0m'  # Reset terminal coloring

    # Evolutionary Cycle: Iterate through the given number of iterations
    for i in range(0, iteration):
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        
        # Stop execution if the duration exceeds the predefined limit (2 hours)
        if elapsed_time > duration:
            return alg_sel.pop.population  # Return the current population
        
        # Debug information on selection
        if debug:
            print("Parent Selection")

        # Elitism-based parent selection for creating the offspring
        alg_sel.ElitismSelectionAlg()
        offspring = Population(pop_size)  # Create a new offspring population
        
        # Create offspring population by crossover between selected parents
        for i in range(0, pop_size):
            parent1, parent2 = alg_sel.select_parents()  # Select two parents
            offspring.population.append(PMX(parent1, parent2))  # Apply PMX crossover to create offspring

        # Apply mutation to the offspring population (with a 75% mutation rate)
        pop_mute(offspring, "swap", 0.75)
        
        # Debug information on survivor selection
        if debug:
            print("\nSurvivor Selection")
        
        # Combine parent and offspring populations into a new population
        pop_grate = Population(pop_size*2)
        pop_grate.population = alg_sel.pop.population.copy()  # Copy the current population
        pop_grate.population.extend(offspring.population)  # Add the offspring to the combined population
        
        # Debug the population distances after mutation
        if debug:
            for ind in pop_grate.population:
                print(ind.distance)

        # Apply elitism to select the best individuals from the combined population
        alg_elim = ElitismSelection(pop_grate, benchmark=50, debug=debug)  # Select the top 50 best individuals
        alg_elim.ElitismSelectionAlg()  # Perform the elitism selection
        
        # Debug the results of the survivor selection
        if debug:
            print(f"Aggregate Pop: {len(alg_elim.pop.population)}")
            for i in range(0, alg_elim.size):
                print(f"{i}: {alg_elim.pop.population[i].distance}")
            print(f"Best Pop: {len(alg_elim.winner.population)}")
            for i in range(0, alg_elim.winner_size):
                print(f"{i}: {alg_elim.winner.population[i].distance}")

        # Update the current population to the newly selected population
        alg_sel.pop.population = alg_elim.winner.population.copy()

        # Debug output for population size and best individual distance
        if debug:
            print(f"Size of winner selection = {len(alg_elim.winner.population)}")
            print(f"\n{R}sel_Best:{B}{alg_sel.winner.population[0].distance}{R} >> elim_Best:{B}{alg_elim.winner.population[0].distance}{RESET}")

    return alg_sel.pop.population  # Return the final population after all iterations

# Main function to handle command-line input and execute the algorithm
def main():
    # Terminal colors setup for output formatting
    RESET = "\033[0m"
    R = "\033[31m"
    G = "\033[32m"
    B = "\033[34m"
    
    debug = False  # Default debug mode is off

    # Valid input options for population sizes, datasets, and iterations
    valid_sizes = [10, 20, 50, 100]
    valid_files = ["eil51", "eil76", "eil101", "st70", "kroA100", "kroC100", "lin105", "pcb442", "pr2392", "usa13509"]
    valid_iterations = [1, 5000, 10000, 20000]

    # Validate command-line input
    if len(sys.argv) < 4:
        print(f"{G}Usage:{RESET} python alg_pmx.py <pop_file> <pop_size> <iteration> <debug>") 
        print(f"files:{B}{valid_files}{RESET}")
        print(f"sizes:{B}{valid_sizes}{RESET}")
        print(f"iterations:{B}{valid_iterations}{RESET}")
        sys.exit(1)

    # Validate dataset input
    try:
        data_name = str(sys.argv[1])
        if sys.argv[1] not in valid_files:
            raise ValueError
    except ValueError:
        print("<pop_file> needs a valid string input")
        print(f"{G}{valid_files}{RESET}")
        sys.exit(1)

    # Validate population size input
    try:
        pop_size = int(sys.argv[2])
        if pop_size not in valid_sizes:
            raise ValueError
    except ValueError:
        print("<pop_size> needs to be a valid int")
        print(f"{G}{valid_sizes}{RESET}")
        sys.exit(1)

    # Validate iterations input
    try:
        iteration = int(sys.argv[3])
        if iteration not in valid_iterations:
            raise ValueError
    except ValueError:
        print("<iteration> needs to be a valid int")
        print(f"{G}{valid_iterations}{RESET}")
        sys.exit(1)

    # Check for optional debug flag
    if len(sys.argv) > 4 and sys.argv[4] == "debug":
        debug = True

    # Execute the algorithm with the provided arguments
    best_pop: list = execute_alg(data_name, pop_size, iteration, debug)

    # Debug: Print out the best population size and end message
    if debug:
        print(f"Pop best size: {len(best_pop)}")
        print(f"{G}Finished Execution!{RESET}")

    # Calculate interquartile range (IQR) distances for the best population
    iqr_index = [("q1", float(0.25 * pop_size)), ("med", float(0.5 * pop_size)), ("q3", float(0.75 * pop_size))]
    dist_ranges = []

    # Compute IQR values for population distances
    for label, percentile in iqr_index:
        if percentile % 1 == 0:
            dist_ranges.append((label, best_pop[int(percentile)].distance))
        else:
            low_mid = math.floor(percentile)
            upp_mid = math.ceil(percentile)
            iqr_avg = (best_pop[low_mid].distance + best_pop[upp_mid].distance) / 2
            dist_ranges.append((label, iqr_avg))

    # Debug: Print IQR distances
    if debug:
        print(f"IQRs {dist_ranges}")

    # Save results to file if not in debug mode
    if not debug:
        file_path = "pmx_results.txt"
        with open(file_path, 'a') as file:
            input_str = str(str(sys.argv[1:4]))
            file.write(input_str + '\n')
            range_strs = ', '.join(f"{label}:{dist}" for label, dist in dist_ranges)
            file.write(range_strs + '\n')

        return 0

# If run as a script, execute the main function
if __name__ == "__main__":
    main()
