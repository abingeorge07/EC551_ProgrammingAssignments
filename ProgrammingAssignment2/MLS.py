import numpy as np

## CLASS ##
# note A is A and a is not(A)
class MLS:

    # May not be useful
    def __init__(self, sop):
        self.numberKernel = 0
        self.sopForm = sop
        self.kernels = []#np.array([[]])
        self.cokernels = []
        # finding all the literals
        terms = "".join(sop)
        terms = list(set(terms))
        self.literals = terms
        self.numLiterals = len(terms)
        
        self.kernelFound = False
    
    # find list of all possible co-kernels
    def findCoKernel(self):
        totalPoss = 2**self.numLiterals
        for i in range(1,totalPoss):
            indices = [i for i, digit in enumerate(reversed(format(i, 'b')), 0) if digit == '1'] 
            tempArr = []
            for j in range(0, len(indices)):
                tempArr.append(self.literals[indices[j]])
            (self.cokernels).append(tempArr)
    
    def checkIfKernel(self, temp):
        intersection = temp[0]
        for i in range(1, len(temp)):
            intersection = list(set(intersection) & set(list(temp[i])))
        
        if(len(intersection) == 0):
            return True
        else:
            return False
    
    # find Kernels
    def findKernel(self):
        self.findCoKernel()
        # remove from the potential list of co-kernels
        # all the non co-kernels
        goodCoKernel = []
        # check if original function is a kernel
        tempKernel = (self.sopForm)[:]
        isKernel = self.checkIfKernel(tempKernel)
        if isKernel is True:
            (self.kernels).append(tempKernel)
            goodCoKernel.append("1")
            
        # which potential co-kernel will give a kernel
        for i in range(0, len(self.cokernels)):
            tempKernel = (self.sopForm)[:]
            tempCoKernel = (self.cokernels)[i]
            numRemoved = 0
            for j in range(0, len(tempKernel)):
                good = True
                for k in range(0,len(tempCoKernel)):
                    if tempCoKernel[k] in tempKernel[j]:
                        s1="".join(c for c in tempKernel[j] if c is not tempCoKernel[k])
                        tempKernel[j] = s1
                    else:
                        tempKernel[j] = ""
                        good = False
                        break
                
                if(good is True):
                    numRemoved = numRemoved + 1
                
                
            if(numRemoved > 1):
                tempKernel = list(filter(None, tempKernel))
                isKernel = self.checkIfKernel(tempKernel)
                if isKernel is True:
                    (self.kernels).append(tempKernel)
                    goodCoKernel.append(tempCoKernel)
               
        self.kernelFound = True        
 

## FUNCTIONS ## 
# Makes an array of the MLS object
def createArray(exp, numExpressions):
    expressions = []
    for i in range(0, numExpressions):
        tempObject = MLS(exp[i])
        expressions.append(tempObject)
        
    return expressions
    
 
# Runs a loop to find kernels of each expressions
def kernelSearch(exp, numExpressions):
    for i in range(0, numExpressions):
        if(not exp[i].kernelFound):
            exp[i].findKernel()
        
# Change expression so a is not(A)
def changeExp(exp, numExpressions):
    
    for i in range(0,numExpressions):
        for j in range(0, len(exp[i])):
            
            term = exp[i][j]
            index = (term).find("~") 
            
            while(index>= 0):
                termList = list(term)
                termList[index+1] = termList[index+1].lower()
                termList[index] = ''
                term = "".join(termList)
                exp[i][j] = term
                index = (exp[i][j]).find("~") 
    return exp
      

# print all the kernels for an expression
def printKernels(exp, numExpressions):
    
    for i in range(0, numExpressions):
        print("Original Expression:")
        print(exp[i].sopForm)
        print("\n")
        print("Kernels of the above expression:")
        if(not exp[i].kernelFound):
            exp[i].findKernel()
        print (*exp[i].kernels, sep="\n")
        print("\n\n")
      
      
      
      
 
#<Insert code from Visaal's part>
# Sample input #
G = ["BF", "BDE", "CF", "~AF"]
# G = ["BF"]
F = ["ABD", "AB~EF", "ACD", "CE", "AC~EF", "DE"]
G = set(G)
F = set(F)
G = list(G)
F = list(F)
numExpressions = 2
exp = [G, F]
# Sample input #



# changes all the nots to lower case
exp = changeExp(exp, numExpressions)
# creates an array of the MLS object
expressions = createArray(exp, numExpressions)
# finds all the kernels of each expression
kernelSearch(expressions, numExpressions)
#prints all the kernels
printKernels(expressions, numExpressions) 

