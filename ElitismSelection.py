import math
import random
from Individual import Individual
from Population import Population

class ElitismSelection:  # Corrected class name
    def __init__(self, pop: Population, benchmark = 2, debug = False):
        self.pop = pop
        self.size = len(pop.population)
        self.winner_size = math.ceil(self.size/100*benchmark)
        self.winner = Population(self.winner_size)
        self.parent_ind = 0
        self.debug = debug
    
    def ElitismSelectionAlg(self):
        # Selects top individuals (2% by default)
        ranking = []
        for i in range(self.size):
            ind: Individual = self.pop.population[i]
            ind.distance = calculatewholedistance(ind.tsp.list)
            ranking.append([i, ind.distance])
        
        ranking.sort(key=lambda x: x[1])  # Sort by distance
        best_indices = [index for index, distance in ranking]

        # Append the winner to the population
        for i in range(self.winner_size):
            best_ind: Individual = self.pop.population[best_indices[i]]   
            self.winner.population.append(best_ind)

        # Debugging
        if self.debug:
            R = '\033[31m'
            G = '\033[32m'
            B = '\033[34m'
            RESET = '\033[0m'
            print(ranking)
            print(f"{R}Best Cities Ordered, {B}{best_indices}{RESET}")
            best_permutation = best_ind.tsp.list
            formatted_string = ", ".join(str(city[0]) for city in best_permutation)
            print(f"{R}Token Perm: {B}{formatted_string}{RESET}")   
            for individual in self.winner.population:
                ind_list = individual.tsp.list
                formatted_string = ", ".join(str(city[0]) for city in ind_list)
                print(f"{R}Perm:Best {B}{formatted_string}{RESET}\n")
        return
    
    def select_parents(self):
        elite: Individual = self.winner.population[self.parent_ind]
        if self.parent_ind >= self.winner_size - 1:
            self.parent_ind = 0
        else:
            self.parent_ind += 1
        parent2: Individual = self.pop.population[random.randint(0, self.size - 1)]
        return elite, parent2

# Calculated distance between two nodes
def calculatedistance(a, b):
    distance = (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2
    return math.sqrt(distance)

# Calculate disctance for the whole map
def calculatewholedistance(ind_list):
    wholedistance = 0
    for i in range(len(ind_list)):
        if i < len(ind_list) - 1:
            wholedistance += calculatedistance(ind_list[i], ind_list[i + 1])
        else:
            wholedistance += calculatedistance(ind_list[0], ind_list[i])
    return wholedistance
