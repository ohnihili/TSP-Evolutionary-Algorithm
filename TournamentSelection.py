import random
import math
from Population import Population

class TournamentSelection:
    def __init__(self, population):

        self.list = population
        self.length = len(self.list.population)
        self.winner = []
        self.winnerDist = []
        self.winner, self.winnerDist = self.TournamentSelectionAlg()

    #k=5
    def TournamentSelectionAlg(self):
        numbers = range(0,self.length)
        
        #compare list
        competition = []
        # get 5 random sequence
        random_numbers = random.sample(numbers, 5)
        for number in random_numbers:
            competition.append(self.list.population[number])

        m =[]
        for i in range(5):
            #calculate the distance with these sequence
            temp = calculatewholedistance(competition[i])
            m.append(temp)
            #get the best out of 5
    
        self.winner.append(competition[m.index(min(m))])
        self.winnerDist.append(min(m))
        return self.winner, self.winnerDist

        #get the best of 5 winners
        #winner_num = min(range(len(winner)), key=lambda i: winner[i][0])
        #winner.append(winner[winner_num][1])
        

def calculatedistance(a,b):
        distance = (a[1]-b[1])**2 + (a[2]-b[2])**2
        distance = math.sqrt(distance)
        return distance

def calculatewholedistance(list):
        wholedistance = 0
        for i in range(len(list.tsp.list)-1):
            wholedistance += calculatedistance(list.tsp.list[i],list.tsp.list[i+1])
        wholedistance += calculatedistance(list.tsp.list[0],list.tsp.list[-1])
        return wholedistance

#Testing Code
#pop1 = Population(10,"test9")
#a = TournamentSelection(pop1)
#print(a.winner[0].tsp.list)
#print(a.winnerDist)
