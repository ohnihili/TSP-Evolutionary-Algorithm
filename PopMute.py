from IndieMute import mutate
from Population import Population
import sys

def pop_mute(pop: Population, mute_type, mute_prob):
    for individual in pop.population:
        mutate(individual, mute_type, mute_prob)
    return

def list_mute(list, mute_type, mute_prob):
    for ind in list:
        mutate(list, mute_type, mute_prob)
    return
#Main 
if __name__ == "__main__":
    valid_mutes = ["insert", "swap", "inversion", "scramble"]
    RESET = "\033[0m"
    R = "\033[31m"
    G = "\033[32m"
    B = "\033[34m"
    if sys.argv < 2 or sys.argv[1] not in valid_mutes:
        print(f"{R}Usage:{RESET} python IndieMute.py <mute_type>") 
        print(f"{G}Valid Mutes: {B}{valid_mutes}{RESET}")
        sys.exit(1)
    
    pop1 = Population(4,"eil51")
    print("Unmutated")
    for i in range(pop1.pop_size):
        print(f"{G}P{i}: {B}{pop1.population[i].tsp.list}{RESET}")
    print("\n")

    pop_mute(pop1, valid_mutes, 1)
    print("Mutated")
    for i in range(pop1.pop_size):
        print(f"{G}P{i}: {B}{pop1.population[i].tsp.list}{RESET}")
    print("\n")