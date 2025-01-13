#InverOverMain.py
# main file for running inver_over algorithm

from InverOverOperator import InverOverOperator
import statistics

#Run the inver-over algorithm with a population size of 50 for 20000 generations
#on the TSP instances mentioned above. Run the algorithm on each instance 30
#times. Report the average cost of the tour you obtained for each instance as well
#the standard deviation.


#testing
#a = InverOverOperator(50,10,"eil51")
#a.run_inver_over()
#print(a.minCost)

#list of instances
instances = ["eil51", "eil76", "eil101", "kroA100", "kroC100", "lin105", "pcb442", "pr2392", "st70"]

#instancesTest = ["eil51", "eil76", "eil101"]


print("Implementation of the Inver Over algorithm\nfor the Travelling Salesman Problem \n\nEach instance run 30 times, with a population of 50 over 20000 generations")
# loop over each instance
for inst in instances:

    #init vector to hold minimum costs
    instance_min_costs = []

    # run inver_over alg 30 times 
    for x in range(30):

        a = InverOverOperator(50,20000, inst)
        a.run_inver_over()
        instance_min_costs.append(a.minCost)
    
    # calculate average cost and standard Deviation
    average_cost = sum(instance_min_costs)/len(instance_min_costs)
    standard_dev = statistics.stdev(instance_min_costs)

    #output results
    print("==============================================")
    print("Instance: ", inst )
    print("\nAverage Tour Cost: ", average_cost)
    print("Standard Deviation: ", standard_dev)
    print("==============================================")



