import sys
import math
import time
from Population import Population
from Crossover import Edge_Recom  # Import the Edge Recombination crossover method
from TournamentSelection import TournamentSelection  # Import the Tournament Selection class
from PopMute import pop_mute  # Import mutation function

# Function to execute the evolutionary algorithm using Tournament Selection and Edge Recombination crossover
def execute_alg(data_name, pop_size, iteration: int, debug:bool = False):
    # Independent variables
    duration = 7200  # Maximum execution time (2 hours)
    start_time = time.time()  # Track the start time of the algorithm

    # Initialize population and selection mechanism
    pop_alg = Population(pop_size, data_name)  # Initialize population with specified size and dataset
    alg_sel = TournamentSelection(pop_alg)  # Initialize tournament selection for parent selection
    
    # If debug is enabled, set terminal color codes for enhanced output
    if debug:
        R = '\033[31m'  # Red
        G = '\033[32m'  # Green
        B = '\033[34m'  # Blue
        RESET = '\033[0m'  # Reset color

    # Evolutionary Cycle: Iterate for the number of specified iterations
    for i in range(0, iteration):
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        
        # If the elapsed time exceeds the maximum allowed duration, stop the execution
        if elapsed_time > duration:
            return alg_sel.pop.population  # Return the current population
        
        # Debugging: Display the selection process
        if debug:
            print("Parent Selection")
        
        # Initialize the offspring population
        offspring = Population(pop_size)
        
        # Generate the offspring by selecting parents and applying crossover
        for i in range(0, pop_size):
            # Select Parent 1 using tournament selection
            alg_sel.TournamentSelectionAlg()
            parent1 = alg_sel.winner[-1]  # Get the last selected winner (best individual)
            
            # Select Parent 2 using tournament selection
            alg_sel.TournamentSelectionAlg()
            parent2 = alg_sel.winner[-1]  # Get the second parent
            
            # Apply Edge Recombination crossover to create a new offspring
            offspring.population.append(Edge_Recom(parent1, parent2))
        
        # Apply mutation to the offspring population (inversion mutation with a 75% probability)
        pop_mute(offspring, "inversion", 0.75)
        
        # Debugging: Display survivor selection
        if debug:
            print("\nSurvivor Selection")
        
        # Create a new combined population (parents + offspring)
        pop_grate = Population(pop_size * 2)
        
        # Add current winners from the previous generation to the combined population
        for i in alg_sel.winner:
            pop_grate.population.append(i)
        
        # Add the newly created offspring to the combined population
        pop_grate.population.extend(offspring.population)
        
        # Debugging: Display population distances after combining
        if debug:
            for ind in pop_grate.population:
                print(ind.distance)
        
        # Perform tournament selection to select the survivors for the next generation
        alg_elim = TournamentSelection(pop_grate)
        
        # Select the top individuals to survive
        for i in range(0, pop_size):
            alg_elim.TournamentSelectionAlg()
        
        # Debugging: Display results of the selection
        if debug:
            print(f"Aggregate Pop: {len(alg_elim.list.population)}")
            for i in range(0, alg_elim.size):
                print(f"{i}: {alg_elim.list.population[i].distance}")
            print(f"Best Pop: {len(alg_elim.winner.population)}")
            for i in range(0, alg_elim.winner_size):
                print(f"{i}: {alg_elim.winner.population[i].distance}")
        
        # Update the current population with the selected winners
        alg_sel.winner = alg_elim.winner
        alg_sel.list.population = alg_sel.winner
        alg_sel.winner = []  # Clear winner list for the next generation
        alg_sel.winnerDist = []  # Clear distance list for the next generation

        # Debugging: Display the best individual from the selection process
        if debug:
            print(f"Size of winner selection = {len(alg_elim.winner.population)}")
            print(f"\n{R}sel_Best:{B}{alg_sel.winner.population[0].distance}{R} >> elim_Best:{B}{alg_elim.winner.population[0].distance}{RESET}")
    
    # Return the final population after all iterations
    return alg_sel.list.population

# Main function to handle command-line inputs and execute the algorithm
def main():
    # Terminal colors setup
    RESET = "\033[0m"
    R = "\033[31m"
    G = "\033[32m"
    B = "\033[34m"
    
    debug = False  # Default value for debug mode
    
    # Define valid input sizes, dataset names, and iterations for validation
    valid_sizes = [10, 20, 50, 100]
    valid_files = ["eil51", "eil76", "eil101", "st70", "kroA100", "kroC100", "lin105", "pcb442", "pr2392", "usa13509"]
    valid_iterations = [1, 5000, 10000, 20000]
    
    # Check for the correct number of command-line arguments
    if len(sys.argv) < 4:
        print(f"{G}Usage:{RESET} python alg_erx.py <pop_file> <pop_size> <iteration> <debug>") 
        print(f"files:{B}{valid_files}{RESET}")
        print(f"sizes:{B}{valid_sizes}{RESET}")
        print(f"iterations:{B}{valid_iterations}{RESET}")
        sys.exit(1)  # Exit if arguments are incorrect
    
    # Validate dataset name input
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

    # Check if debug flag is passed in the arguments
    if len(sys.argv) > 4 and sys.argv[4] == "debug": 
        debug = True

    # Execute the algorithm with the provided inputs
    best_pop: list = execute_alg(data_name, pop_size, iteration, debug)

    # Debugging: Output the size of the best population and completion message
    if debug:
        print(f"Pop best size: {len(best_pop)}")
        print(f"{G}Finished Execution!{RESET}")
    
    # Calculate interquartile ranges (IQR) for the best population
    iqr_index = [("q1", float(0.25 * pop_size)), ("med", float(0.5 * pop_size)), ("q3", float(0.75 * pop_size))]
    dist_ranges = []

    # Compute the IQR values based on distances of the individuals in the population
    for label, percentile in iqr_index:
        if percentile % 1 == 0:
            dist_ranges.append((label, best_pop[int(percentile)].distance))
        else:
            low_mid = math.floor(percentile)
            upp_mid = math.ceil(percentile)
            iqr_avg = (best_pop[low_mid].distance + best_pop[upp_mid].distance) / 2
            dist_ranges.append((label, iqr_avg))

    # Debugging: Output IQR values
    if debug:
        print(f"IQRs {dist_ranges}")

    # Write results to a file if not in debug mode
    if not debug:
        file_path = "erx_results.txt"
        with open(file_path, 'a') as file:
            input_str = str(str(sys.argv[1:4]))
            file.write(input_str + '\n')
            range_strs = ', '.join(f"{label}:{dist}" for label, dist in dist_ranges)
            file.write(range_strs + '\n')

    return 0  # Return success

# If the script is run directly, execute the main function
if __name__ == "__main__":
    main()
