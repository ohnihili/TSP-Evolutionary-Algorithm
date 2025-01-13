from Individual import Individual
import random

# Adding each of the crossover operators (Order Crossover, PMX Crossover,
# Cycle Crossover, Edge Recombination)

# Code copied from IndieMute.py
def random_range(size):
    index1, index2 = 0, 0 
    buffer = size - 1
    while index1 == index2:
        index1 = random.randint(0, buffer)
        index2 = random.randint(0, buffer)
    if index1 > index2:
        buffer = index1
        index1 = index2
        index2 = buffer
    return index1, index2

def Order(parent1, parent2):
    child = Individual()  # Initialize an empty Individual
    size = len(parent1.tsp.list)
    lower, upper = random_range(size)
    
    
    # Fill in the child with a subset from parent1
    for i in range(lower, upper + 1):
        child.tsp.list.append(parent1.tsp.list[i])

    # Fill the rest from parent2, starting from upper
    j=0
    for i in range(upper, size):
        if len(child.tsp.list) == size:
            return child
        if parent2.tsp.list[i] not in child.tsp.list:
            if size - lower > len(child.tsp.list):
                child.tsp.list.append(parent2.tsp.list[i])
            else:
                child.tsp.list.insert(j, parent2.tsp.list[i])
                j=j+1
    #continuing loop from start of parent 
    for i in range(0, size):
        if len(child.tsp.list) == size:
            return child
        if parent2.tsp.list[i] not in child.tsp.list:
            if size - lower > len(child.tsp.list):
                child.tsp.list.append(parent2.tsp.list[i])
            else:
                child.tsp.list.insert(j, parent2.tsp.list[i])
                j=j+1
    return child

def Edge_Recom(parent1, parent2):
    size = len(parent1.tsp.list)
    child = Individual()  # Initialize an empty Individual
    
    # Build the edge map using city identifiers as keys
    edge_map = {city[0]: set() for city in parent1.tsp.list}
    
    for p in [parent1, parent2]:
        for i in range(size):
            city = p.tsp.list[i][0]  # Use the city identifier
            left = p.tsp.list[(i - 1) % size][0]  # Use the city identifier
            right = p.tsp.list[(i + 1) % size][0]  # Use the city identifier
            edge_map[city].update([left, right])

    # Choose a starting city identifier at random
    current_city = random.choice(parent1.tsp.list)[0]
    child.tsp.list.append(next(city for city in parent1.tsp.list if city[0] == current_city))
    
    while len(child.tsp.list) < size:
        # Remove the current city from edge_map
        for key in edge_map.keys():
            edge_map[key].discard(current_city)

        # Find the next city to add
        if edge_map[current_city]:
            next_city = min(edge_map[current_city], key=lambda city: len(edge_map[city]))
        else:
            # If no more connected cities, choose a random unvisited city
            remaining_cities = [city for city in parent1.tsp.list if city[0] not in [c[0] for c in child.tsp.list]]
            next_city = random.choice(remaining_cities)[0]

        child.tsp.list.append(next(city for city in parent1.tsp.list if city[0] == next_city))
        current_city = next_city

    return child

def PMX(parent1, parent2, debug = False):
    child = Individual()  # Initialize an empty Individual
    size = len(parent1.tsp.list)
    lower, upper = random_range(size)
    # Initialize the child's list with None
    child.tsp.list = [None] * size

    # Copy the segment from parent1 to the child
    child.tsp.list[lower:upper + 1] = parent1.tsp.list[lower:upper + 1]
    if debug:
        R = '\033[31m'
        G = '\033[32m'
        B = '\033[34m'
        RESET = '\033[0m'
        print(f"PMX Child P1 Inheritance: {G}{child.tsp.list[0:lower]}{B}{child.tsp.list[lower:upper+1]}{RESET}{G}{child.tsp.list[upper+1:len(child.tsp.list)]}{RESET}\n")
    # Mapping from parent2's segment
    mapping = {parent1.tsp.list[i][0]: parent2.tsp.list[i] for i in range(lower, upper + 1)}
    if debug:
        formatted_string = ", ".join(f"{R}{key}{RESET}:{B}{value}{RESET}" for key, value in mapping.items())
        print(f"PMX Mapping K:V, {formatted_string}\n")

    # Fill the rest of the child with elements from parent2
    for i in range(size):
        if not child.tsp.list[i]:
            candidate = parent2.tsp.list[i]
            if debug:
                print(f"Original Value{G}{candidate}{RESET}")
                prev_candidate = candidate
            while candidate[0] in mapping.keys():
                candidate = mapping[candidate[0]]
                if debug:
                    print(f"Update:{R}{prev_candidate}{RESET} >> {G}{candidate}{RESET}")
                    prev_candidate = candidate
            child.tsp.list[i] = candidate
    if debug:
        print(f"\nPMX Crossover Child: {G}{child.tsp.list[0:lower]}{B}{child.tsp.list[lower:upper+1]}{G}{child.tsp.list[upper+1:len(child.tsp.list)]}{RESET}")
    return child

def Cycle(parent1, parent2, debug = False):
    child1 = Individual()  # Initialize an empty Individual
    child2 = Individual()
    size = len(parent1.tsp.list)

    # Initialize the child's list with None
    child1.tsp.list = [None] * size
    child2.tsp.list = [None] * size
    # Find cycles between parent1 and parent2
    start = 0
    inherit_p1 = True
    
    while None in child1.tsp.list:
        if child1.tsp.list[start] is None:
            cycle_indices = []
            current_index = start

            while current_index not in cycle_indices:
                cycle_indices.append(current_index)
                current_index = parent1.tsp.list.index(parent2.tsp.list[current_index])
            if debug:
                R = '\033[31m'
                G = '\033[32m'
                B = '\033[34m'
                RESET = '\033[0m'
                print(f"S:{R}{start}{RESET} Indexes:{R}{cycle_indices}{RESET}")
            # Assign the cycle elements to the child from parent1
            for index in cycle_indices:
                if inherit_p1:
                    child1.tsp.list[index] = parent1.tsp.list[index]
                else:
                    child1.tsp.list[index] = parent2.tsp.list[index]
                if inherit_p1:
                    child2.tsp.list[index] = parent2.tsp.list[index]
                else:
                    child2.tsp.list[index] = parent1.tsp.list[index]
            if debug:
                if inherit_p1:
                    print(f"P1: {B}{child1.tsp.list}{RESET}")
                else:
                    print(f"P2: {G}{child1.tsp.list}{RESET}")
                if not inherit_p1:
                    print(f"P1: {B}{child2.tsp.list}{RESET}")
                else:
                    print(f"P2: {G}{child2.tsp.list}{RESET}")
        inherit_p1 = not inherit_p1
        # Find the next start point
        start = child1.tsp.list.index(None) if None in child1.tsp.list else start + 1
    return child1, child2

if __name__ == "__main__":
    # Example usage of the crossover operators
    ind1 = Individual("test9")
    ind2 = Individual("test9")

    # Ensure the TSP lists are initialized before crossover
    ind1.tsp.list = ind1.tsp.list or []
    ind2.tsp.list = ind2.tsp.list or []

    print(f"Parent1: {ind1.tsp.list}\nParent2: {ind2.tsp.list}")

    child_order = Order(ind1, ind2)
    print(f"Order Crossover Child: {child_order.tsp.list}")

    child_edge = Edge_Recom(ind1, ind2)
    print(f"Edge Recombination Child: {child_edge.tsp.list}")

    child_pmx = PMX(ind1, ind2, True) #Change true to remove
    print(f"PMX Child: {child_pmx.tsp.list}")

    child_cycle1, child_cycle2= Cycle(ind1, ind2, True)
    print(f"Cycle Child1:{child_cycle1.tsp.list},\nCycle Child2:{child_cycle2.tsp.list}")
