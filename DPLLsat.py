#!/usr/bin/python3

import sys, getopt
import collections
import copy
import random

N=10000
sys.setrecursionlimit(N)


class SatInstance:
    def __init__(self):
        pass
    def from_file(self, inputfile):
        self.clauses = list()
        self.VARS = set()
        self.p = 0
        self.cnf = 0
        with open(inputfile, "r") as input_file:
            self.clauses.append(list())
            maxvar = 0
            for line in input_file:
                tokens = line.split()
                if len(tokens) != 0 and tokens[0] not in ("p", "c"):
                    for tok in tokens:
                        lit = int(tok)
                        maxvar = max(maxvar, abs(lit))
                        if lit == 0:
                            self.clauses.append(list())
                        else:
                            self.clauses[-1].append(lit)
                if tokens[0] == "p":
                    self.p = int(tokens[2])
                    self.cnf = int(tokens[3])
            assert len(self.clauses[-1]) == 0
            self.clauses.pop()
            # print(maxvar)
            # print(self.p)
            if not (maxvar == self.p):
                print("Non-standard CNF encoding!")
                sys.exit(5)
      # Variables are numbered from 1 to p
        for i in range(1,self.p+1):
            self.VARS.add(i)
    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s



def main(argv):
   inputfile = ''
   verbosity=False
   inputflag=False
   try:
      opts, args = getopt.getopt(argv,"hi:v",["ifile="])
   except getopt.GetoptError:
      print ('DPLLsat.py -i <inputCNFfile> [-v] ')
      sys.exit(2)
   for opt, arg in opts:
       if opt == '-h':
           print ('DPLLsat.py -i <inputCNFfile> [-v]')
           sys.exit()
    ##-v sets the verbosity of informational output
    ## (set to true for output veriable assignments, defaults to false)
       elif opt == '-v':
           verbosity = True
       elif opt in ("-i", "--ifile"):
           inputfile = arg
           inputflag = True
   if inputflag:
       instance = SatInstance()
       instance.from_file(inputfile)
       solve_dpll(instance, verbosity)
   else:
       print("You must have an input file!")
       print ('DPLLsat.py -i <inputCNFfile> [-v]')


""" Question 2 """
# Finds a satisfying assignment to a SAT instance,
# using the DPLL algorithm.
# Input: a SAT instance and verbosity flag
# Output: print "UNSAT" or
#    "SAT"
#    list of true literals (if verbosity == True)
#    list of false literals (if verbosity == True)
#
#  You will need to define your own
#  solve(VARS, F), pure-elim(F), propagate-units(F), and
#  any other auxiliary functions

def propagateUnits(F):

    unitClauses = []
    nonUnitClauses = []
    # print("original F:")
    # print(F)
    for i in F:
        #print(i)
        if len(i) == 1:
            unitClauses.append(i)
            #print(i)
        else:
            nonUnitClauses.append(i)
           # print(i)

    # print("Unit Clauses: ")
    # print(unitClauses)
    # print("NonUnit Clauses: ")
    # print(nonUnitClauses)

    for x in unitClauses:
        for c in nonUnitClauses:
            for y in c:
                if x[0] == y:
                    nonUnitClauses.remove(c)
                if -x[0] == y or x[0] == -y:
                    #print(y)
                    c.remove(y)

    F = nonUnitClauses + unitClauses
    # print("F after propagateunits(): ")
    # print(F)
    return F


def pureElim(F):
    # print("Original F: ")
    # print(F)

    temp = []
    negatives = []
    nonNegatives=[]

    for i in F:
        #print(i)
        for j in i:
            #print(j)
            temp.append(j)
            #temp.sort()

    #print(temp)
    for x in temp:
        #print(x)
        if x<0:
            negatives.append(x)
        else:
            nonNegatives.append(x)

    negatives.sort()
    nonNegatives.sort()

    impures = []

    for k in negatives:
        for l in nonNegatives:
            #print(k,l)
            if (k==-l):
                #print("True")
                impures.append(k)

    for i in impures:
        for j in temp:
            if(i==j) or (-i==j):
                temp.remove(j)

    for x in temp:
        for y in F:
            for z in y:
                if(x==z):
                    F.remove(y)
                    if [x] not in F:
                        F.append([x])
    # print(negatives)
    # print(nonNegatives)
    # print(impures)
    # print("Pure literals: ")
    # print(temp)
    # print("F after pure-elim(): ")
    # print(F)

    return F

def pickVariable(VARS,F):
    #print(F)

    varList = list(VARS)
    randVar = random.choice(varList)

    return randVar

def FisConsistentSet(VARS,F):
    listVar = list(VARS)
    # print("Lengh listvar: ")
    # print(len(listVar))
    # print("length of F:")
    # print(len(F))

    for i in F:
        if len(i) != 1:
            return False

    # if(len(F) == len(listVar)):
    return True


def FcontainsEmptyClause(F):
    for i in F:
        if len(i)==0:
            return True
        else:
            return False


def solve_dpll(instance, verbosity):
    # print(instance)
    # print(instance.VARS)
    # print(verbosity)
    ###########################################
    # Start your code

    VARS = instance.VARS
    F = instance.clauses
    result = solve(VARS,F)

    pos=[]
    neg=[]

    if(result == []):
        print("UNSAT")
    else:
        print("SAT")
        for i in result:
            for j in i:
                if j>0:
                    pos.append(j)
                elif j<0:
                    neg.append(j)

    if verbosity==True:
        print(pos)
        print(neg)


    # End your code
    return True
    ###########################################

def solve(VARS,F):
    #print(F)
    F_1 = propagateUnits(F)
    F_2 = pureElim(F_1)

    # print("propagate unit results: ")
    # print(F_1)
    #
    # print("pure elim results: ")
    # print(F_2)

    if FcontainsEmptyClause(F_2):
        return []
    elif FisConsistentSet(VARS,F_2):
        return F_2

    F_2_f = copy.deepcopy(F_2)
    F_2_s = copy.deepcopy(F_2)

    maxVar = pickVariable(VARS, F_2)

    F_2_f.append([maxVar])
    F_2_s.append([-maxVar])


    if (solve(VARS,F_2_f)) != []:
        return solve(VARS,F_2_f)
    elif (solve(VARS,F_2_f)) == []:
        return solve(VARS,F_2_s)

if __name__ == "__main__":
   main(sys.argv[1:])
