import numpy as np
import os 
import pickle 

class MLS:

    
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
        # isKernel = self.checkIfKernel(tempKernel)
        # if isKernel is True:
        #     (self.kernels).append(tempKernel)
        #     goodCoKernel.append("1")
            
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
                    goodCoKernel.append("".join(tempCoKernel))
               
        self.kernelFound = True        
        self.goodCoKernel = goodCoKernel


class intersectionClass():
    def __init__(self, intersectionSOP, listFunctions):
            self.interSOP = intersectionSOP
            self.funcNum = listFunctions
            intersection = intersectionSOP[0]
            for i in range(1, len(intersectionSOP)):
                intersection = list(set(intersection) | set(list(intersectionSOP[i])))
            self.numLiterals = len(intersection)
            self.cost = self.numLiterals  * len(listFunctions)


class finalEquation():
    def __init__(self,functionNum):
        self.funNum = functionNum
        self.divisor = []
        self.quotient = []
        self.remainder = []

    def findRemainder(self, original, cokernel, intersectionSOP):
        tempCo = ""
        if(cokernel != "1"):
            tempCo = cokernel
        tempTerm = ["".join(sorted(s + tempCo)) for s in intersectionSOP]
        remainder = [i for i in original if "".join(sorted(i)) not in tempTerm] 
        return remainder

    def update(self, expression, SOP, cokernel):

        if(cokernel in self.divisor):
            return True

        if(len(SOP) >1):
            if len(self.divisor) == 0:
                rem = self.findRemainder(expression.sopForm, cokernel, SOP)
                self.remainder = rem
                (self.divisor).append(cokernel)
                (self.quotient).append(SOP)
                return True
            else:
                rem = self.findRemainder(expression.sopForm, cokernel, SOP)
                originalRem = self.remainder
                newRem = [s for s in originalRem if s in rem]
                if(len(newRem) < len(originalRem)):
                    (self.divisor).append(cokernel)
                    (self.quotient).append(SOP)
                    
                    self.remainder = newRem

                    return True
                else:
                    return False
        else:
            return False