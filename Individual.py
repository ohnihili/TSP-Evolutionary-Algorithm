from TSPProblem import TSPProblem
import math
import random


class Individual(TSPProblem):
    def __init__(self, tsp_file=None):  # initialize with something like a = Individual("eil101")
        if tsp_file is None:
            self.tsp = TSPProblem()
            self.distance = float('inf')  # setting initial distance to a high value (no valid tour)
        else:
            self.tsp = TSPProblem(tsp_file)  # creates a tsp problem, that is now a part of this individual
            random.shuffle(self.tsp.list)  # randomizes the list when initialized
            self.newDistance()  # calculate distance of the random list

    def newDistance(self):
        self.distance = 0.0  # setting initial distance to 0
        if len(self.tsp.list) < 2:  # Edge case: not enough cities to calculate a route
            self.distance = float("inf")  # Infinite distance for invalid tours
            return

        a = self.tsp.list[-1][1]  # last city's x coord
        b = self.tsp.list[0][1]  # first city's x coord
        c = self.tsp.list[-1][2]  # last city's y coord
        d = self.tsp.list[0][2]  # first city's y coord

        # Calculate the distance between the first and last city (complete the tour)
        self.distance += math.sqrt((a - b) ** 2 + (c - d) ** 2)

        # Calculate the distance between consecutive cities in the tour
        for i in range(len(self.tsp.list) - 1):
            a = self.tsp.list[i + 1][1]  # next city's x coord
            b = self.tsp.list[i][1]  # current city's x coord
            c = self.tsp.list[i + 1][2]  # next city's y coord
            d = self.tsp.list[i][2]  # current city's y coord
            self.distance += math.sqrt((a - b) ** 2 + (c - d) ** 2)

        # Check if the distance is still 0 (something went wrong), assign a large distance
        if self.distance == 0.0:
            print(f"Error: Calculated distance is 0 for {self.tsp.list}")  # Debugging line
            self.distance = float('inf')  # Assign infinity or a large value for invalid distances
        else:
            print(f"Calculated distance: {self.distance}")  # Debugging line

# Testing the class
if __name__ == "__main__":
    a = Individual("eil101")
    print(a.distance)
    a.newDistance()
    print(a.distance)
    print(a.tsp)
