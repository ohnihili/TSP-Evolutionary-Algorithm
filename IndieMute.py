#Testing for individual python tests. 
from Individual import Individual
import random
import sys

def ind_rolls(permutation):
    index1,index2 = 0,0 #Values to store indexes.
    buffer = len(permutation)-1
    while (index1 == index2 or abs(index1-index2) == 1):
        index1 = random.randint(0, buffer)
        index2 = random.randint(0, buffer)
    if (index1 > index2):
        buffer = index1
        index1 = index2
        index2 = buffer
    return index1, index2

def permu_mutate(permutation, mute_type):
    city_cache = []                     #Store Permutation Elements
    ind_low, ind_high = ind_rolls(permutation)
    #ind_low, ind_high = 1,3
    #print(f"We are operating on the indicies: L: {ind_low} R: {ind_high} with E:{len(permutation)}")
    #print(f"These are the elements L:{permutation[ind_low]} and R:{permutation[ind_high]}\n")
    #Insert pairs elements in the random index while mainting rest of the order.
    if mute_type == "insert":     
        ind_diff = ind_high - ind_low
        if(ind_diff == 2):
            city_cache.append(permutation[ind_high])
            permutation[ind_high] = permutation[ind_low+1]
            permutation[ind_low+1] = city_cache.pop()
        else:
            city_cache.append(permutation[ind_low+1])
            permutation[ind_low+1] = permutation[ind_high]

            for i in range(ind_high, ind_low+2, -1):
                permutation[i] = permutation[i-1]
            permutation[ind_low+2] = city_cache.pop()

    elif mute_type == "swap":
        city_cache.append(permutation[ind_high])
        permutation[ind_high] = permutation[ind_low]
        permutation[ind_low] = city_cache.pop()
    
    elif mute_type == "inversion":
        bound = round((ind_high - ind_low)/2 + 0.5)
        for i in range(bound):
            city_cache.append(permutation[ind_low + i])
            #print(f"we are swapping {permutation[ind_low + i]} and {permutation[ind_high - i]}\n")
            permutation[ind_low + i] = permutation[ind_high - i]
            permutation[ind_high - i] = city_cache.pop()

    elif mute_type == "scramble":
        for i in range (ind_high - ind_low + 2):
            index1 = random.randint(ind_low, ind_high)
            index2 = random.randint(ind_low, ind_high)
            while (index1 == index2):
                index2 = random.randint(ind_low, ind_high)
            city_cache.append(permutation[index1])
            permutation[index1] = permutation[index2]
            permutation[index2] = city_cache.pop()
    return permutation
    
def mutate(individual, mute_type, mute_prob = 0.2):
    mute_gauge = random.random()
    #print(mute_gauge)
    if(mute_gauge < mute_prob):
        permu_mutate(individual.tsp.list, mute_type)

#Testing code. 
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
    
    ind1 = Individual("eil101")
    print(f"Orignal Ind: {B}{ind1.tsp.list}{RESET}")
    mutate(ind1, sys.argv[1], 1)
    print(f"Mutated Ind: {B}{ind1.tsp.list}{RESET}")
    print(ind1.tsp.list)
    print("\n")