from Population import Population
from Individual import Individual
import copy
import random

def reverseSublist(list,start,end):
    list[start:end] = list[start:end][::-1]
    return list


class InverOverOperator:

    def __init__(self, population_size,num_generations, tsp_file):
        self.population_size = population_size
        self.num_generations = num_generations
        self.tsp_file = tsp_file
        
    #run inver over operation on population
    def run_inver_over(self):
        
        #initilise random population
        population = Population(self.population_size, self.tsp_file).population

        current_gen = 0
        probability = 0.02

        while current_gen < self.num_generations:   # While termination condition is not met
            for individual in population:           # for each individual in the population
                
                S = copy.deepcopy(individual)

                #select random city in S
                c1 = random.choice(S.tsp.list)

                #select second city
                while True:
                    if random.random() < probability:      # p=0.02 as in the paper, necessary for random mutations, select city two from same indv
                        c2 = random.choice(S.tsp.list)
                    else:                           # else, take srandom individual from population and take city next to c1
                        S2 = random.choice(population)
                        c1_in_S2 = S2.tsp.list.index(c1)

                        if c1_in_S2 == len(S.tsp.list)-1:
                            c2 = S2.tsp.list[c1_in_S2-1]
                        else:
                            c2 = S2.tsp.list[c1_in_S2+1]   #find index of c1 in second individual and take next element and set c2
                    
                    c1_index = S.tsp.list.index(c1)
                    c2_index = S.tsp.list.index(c2)

                    # if city before or after c1 in S equals city 2, break loop
    
                    if (c1_index > 0 and S.tsp.list[c1_index-1] == c2 or c1_index < len(S.tsp.list)-1 and S.tsp.list[c1_index+1] == c2):    
                        break

                    #inverse the section from the next city of city c1 to the city c2 in S
                    
                    if c1_index < c2_index:
                        S.tsp.list = reverseSublist(S.tsp.list,c1_index, c2_index)
                    else:
                        S.tsp.list = reverseSublist(S.tsp.list,c2_index, c1_index)
                    
                #compare S to individual, replace current individual in population with fittest result
                S.newDistance()

                if S.distance <= individual.distance:
                    individual = S
                    #individual = S

            current_gen+=1

            #print("generation ", current_gen, "done")
        
        # Return best solution cost from population once end condition is met
        pathcosts = []

        #iterate population and find pathcosts
        for i in population:
            pathcosts.append(i.distance)

        #set min pathcost
        self.minCost = min(pathcosts)
