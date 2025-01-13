# READ ME

# can test with the TSPProblem.py
            
class TSPProblem:

    def __init__(self, file=None):
        self.list = [] # list of lists
        # If a file is provided, fill in the list with random permutation from file, otherwise have empty list
        if file is not None:
            self.filename = file + ".tsp" # so that you dont have to type .tsp after each file
            self.list = self.readTSP(self.filename, self.list)

    def readTSP(self, file, list): 
        # ReadTSP() works for the files we need to use in exercise 6. other files have different structures, it does not adapt

        # exercise 2 says all TSP files are in instances folder
        file = "Instances/" + file # navigate to instances folder.

        with open(file, 'r') as file:

            # skip until line read as NODE_COORD_SECTION
            currline = file.readline()
            while "NODE_COORD_SECTION" not in currline:
                currline = file.readline()

            # NODE_COORD_SECTION line found, now we start reading in the coordinates
            currline = file.readline()
            while "EOF" not in currline:
                line = [float (x) for x in currline.split()] # save each element in the line as int rather than string
                list.append(line) # append line written as list of ints
                newline = currline
                currline = file.readline() # no EOF in USA file, check if two blank lines in a row
                if currline == newline: #because USA cringe 
                    list.pop()
                    list.pop()
                    break
        return list

