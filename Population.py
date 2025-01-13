# Population.py

from Individual import Individual
# when using tsp_file the name should be without the extension ie. "eil51"
class Population:
    def __init__(self, pop_size, tsp_file = None):
        # Changing pop size depending on file, allows for testing multiple sizes
        self.pop_size = pop_size
        if tsp_file:
            self.population = self.fill_pop(tsp_file)
        else:
            self.population = []
    # fills the list with the individual objects
    
    def fill_pop(self, tsp_file):
        #call the individual function in a loop with pop_size indivudals 
        pop_list = []
        for _ in range(self.pop_size):
            individual = Individual(tsp_file)
            pop_list.append(individual)
        return pop_list
    
    # for testing purposes, Print function
    def print_pop(self):
        for Individual in self.population:
            print(Individual.tsp.list)  # Replace 'individual.tsp' with the specific attribute/method you want to print
            print()

if __name__ == "__main__":
    pop1 = Population(2,"eil51")
    pop1.print_pop()
    
        
        