#!/usr/bin/python3

import sys, getopt
#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
# num_hours_i_spent_on_this_assignment = 0
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# <Your feedback goes here>
"""

"""
#####################################################
#####################################################

def main(argv):
   inputfile = ''
   N=0
   try:
      opts, args = getopt.getopt(argv,"hn:i:",["N=","ifile="])
   except getopt.GetoptError:
      print ('sudoku.py -n <size of Sodoku> -i <inputputfile>')
      sys.exit(2)
   for opt, arg in opts:
       if opt == '-h':
           print ('sudoku.py  -n <size of Sodoku> -i <inputputfile>')
           sys.exit()
       elif opt in ("-n", "--N"):
           N = int(arg)
       elif opt in ("-i", "--ifile"):
           inputfile = arg
   instance = readInstance(N, inputfile)
   toCNF(N,instance,inputfile+str(N)+".cnf")




def readInstance (N, inputfile):
    #print(inputfile)
    if inputfile == '':
        return [[0 for j in range(N)] for i in range(N)]
    with open(inputfile, "r") as input_file:
        instance =[]
        for line in input_file:
            number_strings = line.split() # Split the line on runs of whitespace
            numbers = [int(n) for n in number_strings] # Convert to integers
            if len(numbers) == N:
                instance.append(numbers) # Add the "row" to your list.
            else:
                print("Invalid Sudoku instance!")
                sys.exit(3)
        #print(instance)
        return instance # a 2d list: [[1, 3, 4], [5, 5, 6]]


def encodeVar(i,j,k,map):

    #print("i,j,k: ")
    #print(i,j,k)
    #print("map val: ")
    #print(map.index([i,j,k]))
    return (1+map.index([i,j,k]))


def generateMap(N):
    arr = []
    count = 0
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            for k in range(1, N + 1):
                count = count + 1
                # print(i,j,k,count)

                arr.append([i, j, k])
    #print(arr)
    return arr


""" Question 1 """
def toCNF (N, instance, outputfile):
    """ Constructs the CNF formula C in Dimacs format from a sudoku grid."""
    """ OUTPUT: Write Dimacs CNF to output_file """
    output_file = open(outputfile, "w")
    "*** YOUR CODE HERE ***"

    # for i in range(0,N):
    #     for j in range(0,N):
    #         print(instance[i][j])
    numOfClauses = 0

    map = generateMap(N)


    for i in range(1,N+1):
        for j in range(1,N+1):
            for k in range(1,N+1):
                #print(i,j,k)
                output_file.write(str(encodeVar(i, j, k,map)) + " ")
                #print(str(encodeVar(i, j, k,map)))
            output_file.write(" 0\n")
            numOfClauses = numOfClauses + 1
    #print(numOfClauses)

    c1=0
    for i in range(1,N+1):
        for j in range(1,N+1):
            for k in range(1,N):
                for l in range(k+1,N+1):
                    output_file.write("-" + str(encodeVar(i, j, k,map)) + " -" + str(encodeVar(i, j, l,map)) + " 0\n")
                    #print("-" + str(encodeVar(i, k, j,map)) + " -" + str(encodeVar(i, l, j,map)))
                    numOfClauses = numOfClauses + 1
                    c1=c1+1
    #print(c1)


    c2=0
    for i in range(1,N+1):
        for j in range(1,N+1):
            for k in range(1,N):
                for l in range(k+1,N+1):
                    output_file.write("-" + str(encodeVar(i, k, j,map)) + " -" + str(encodeVar(i, l, j,map)) + " 0\n")
                    #print("-" + str(encodeVar(i, k, j,map)) + " -" + str(encodeVar(i, l, j,map)))
                    numOfClauses = numOfClauses + 1
                    c2 = c2+1
    #print(c2)


    c3=0
    for i in range(1,N+1):
        for j in range(1,N+1):
            for k in range(1,N):
                for l in range(k+1,N+1):
                    #print(i,j,k,l)
                    output_file.write("-" + str(encodeVar(k, i, j,map)) + " -" + str(encodeVar(l, i, j,map)) + " 0\n")
                    #print("-" + str(encodeVar(k, i, j,map)) + " -" + str(encodeVar(l, i, j,map)))
                    numOfClauses = numOfClauses + 1
                    c3 = c3+1
    #print(c3)

    c4=0
    for row in range(0, N):
        for col in range(0, N):
            if instance[row][col] != 0:
                # print(row+1)
                # print(col+1)
                #print((encodeVar(row+1, col+1, instance[row][col],map)))
                output_file.write(str(encodeVar(row+1, col+1,instance[row][col], map)) + ' 0\n')
                numOfClauses = numOfClauses + 1
                c4=c4+1
    #print(c4)

    nval = str(N**3)


    output_file.close()
    output_file = open(outputfile, "r")
    temp = output_file.read()
    output_file.close()
    output_file = open(outputfile, "w")
    output_file.write("p" + " " + "cnf " + nval + " " + str(numOfClauses) + "\n")
    output_file.write(temp)

    "*** YOUR CODE ENDS HERE ***"
    output_file.close()



if __name__ == "__main__":
   main(sys.argv[1:])
