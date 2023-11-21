import numpy as np
import os 
import pickle 
from LUT_class import LUT_class
from LUT_class import FPGA
from MLS_class import MLS
from MLS_class import intersectionClass
from MLS_class import finalEquation
from LUT_mat import LUT_object
from LUT_mat import LUT




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
        print("Cokernels of the above expression:")
        print (*exp[i].goodCoKernel, sep="\n")
        print("\n\n")


# finds the intersection between 2 lists
def findIntersection_SOP(sop1, sop2):
    lst3 = [value for value in sop1 if value in sop2]
    return lst3

# updates the ideal intersections
def updateIdeal(tempObject, idealIntersections):
    # Converting integer list to string list
    tempArr = tempObject.funcNum
    tempArr.sort()
    s = [str(i) for i in tempArr]
    # Join list items using join()
    res = "".join(s)

    tempSOP = tempObject.interSOP

    if(len(tempSOP) > 1):

        if (res in idealIntersections.keys()):
            tempVal = idealIntersections[res].cost
            if(tempVal < tempObject.cost):
                idealIntersections[res] = tempObject
        else:
            idealIntersections[res] = tempObject

    return idealIntersections



# find all the intersections of all the kernels
def findIntersections(expressions, numExpressions):
    idealIntersections = {}
    allIntersections = []

    for i in range(0,numExpressions-1):
        exp1_kernel = expressions[i].kernels
        exp1_cokernel = expressions[i].goodCoKernel
        for j in range(i+1, numExpressions):
            exp2_kernel = expressions[j].kernels
            exp2_cokernel = expressions[j].goodCoKernel
            for k in range(0, len(exp1_kernel)):
                for l in range(0,len(exp2_kernel)):
                    intersec = findIntersection_SOP(exp1_kernel[k], exp2_kernel[l])
                    if (len(intersec) > 0):
                        tempObject = intersectionClass(intersec, [i,j])
                        tempObject.cokernels = [exp1_cokernel[k], exp2_cokernel[l]]
                        allIntersections.append(tempObject)
                        idealIntersections = updateIdeal(tempObject, idealIntersections)
      
    return allIntersections, idealIntersections
      


def finalAllFunctions(finalEquationArr):
    listOfFunctions = []
    num = 1
    for i in range(0, len(finalEquationArr)):
        for j in range(0, len(finalEquationArr[i].divisor)):
            tempQuotient = finalEquationArr[i].quotient[j]
            tempQuotient = sorted(tempQuotient)
            # if(not((len(finalEquationArr[i].divisor) ==1 and  finalEquationArr[i].divisor[0] == "") and len(finalEquationArr[i].remainder) == 0)):
            if(tempQuotient not in listOfFunctions):
                listOfFunctions.append(tempQuotient)
                strNew = "F"+str(num)
                finalEquationArr[i].quotient[j] = [strNew]
                num = num + 1
            else:
                ind = listOfFunctions.index(tempQuotient, 0 , len(listOfFunctions))
                strNew = "F"+str(ind+1)
                finalEquationArr[i].quotient[j] = [strNew]
    return listOfFunctions


def convert2finalEq(auxEq):
    finalArr = []
    for i in range(0, len(auxEq)):
        finalArr.append(finalEquation(0))
        finalArr[i].remainder = auxEq[i]
        strTemp = "F"+str(i+1)
        finalArr[i].functionName = strTemp  

    return finalArr

# find the ideal intersection
# temporary code
def findIdealIntersection(idealIntersections, numExpressions, finalEquationArr, expressions):
    numTimesLeft = numExpressions -2
    tempIntersections = []

    # for key in idealIntersections.keys():
    for key in range (0, len(idealIntersections)):
        tempArr = idealIntersections[key].funcNum
        copyFinalEquation = finalEquationArr[:]
        for i in range(0, len(tempArr)):
            equationNum = tempArr[i]
            dec = finalEquationArr[equationNum].update(expressions[equationNum], idealIntersections[key].interSOP, idealIntersections[key].cokernels[i])

            if(dec == False):
                finalEquationArr = copyFinalEquation
                break

    for i in range(0, numExpressions):
        if(len(finalEquationArr[i].divisor) == 0):
            finalEquationArr[i].quotient = [expressions[i].sopForm]
            finalEquationArr[i].divisor.append("")

    auxFunctions = finalAllFunctions(finalEquationArr)

    auxFunctions = convert2finalEq(auxFunctions)

    numStart = len(auxFunctions) + 1

    indices2remove = []
    for i in range(0, numExpressions):
        # print(finalEquationArr[i].divisor)
        # print(finalEquationArr[i].quotient)
        # print(finalEquationArr[i].remainder)
        # input("Pause")
        if(((len(finalEquationArr[i].divisor) ==1 and  finalEquationArr[i].divisor[0] == "") and len(finalEquationArr[i].remainder) == 0)):
            indices2remove.append(i)
        else:
            finalEquationArr[i].functionName = "F"+str(numStart)
            numStart = numStart + 1


    if(len(indices2remove) > 0):
        finalEquationArr = [finalEquationArr[i] for i in range(0, len(finalEquationArr)) if i not in indices2remove]

    return finalEquationArr, auxFunctions
        
def createFinalEqArr(numExpressions):
    finalEquationArr = []
    for i in range(0,numExpressions):
        temp = finalEquation(i)
        finalEquationArr.append(temp)

    return finalEquationArr

def printFinalEquation(finalEquationArr, auxEq):
    numExpressions = len(finalEquationArr)

    for i in range(0,len(auxEq)):
        print(auxEq[i].functionName+": "+"+".join(auxEq[i].remainder))



    for i in range(0, numExpressions):
        print(finalEquationArr[i].functionName + ": ", end ="")
        for j in range(0, len(finalEquationArr[i].divisor)):
            if j != 0:
                print("+", end = "")
            print("(" + "+".join(finalEquationArr[i].quotient[j])+")" + finalEquationArr[i].divisor[j], end="")

        if(len(finalEquationArr[i].remainder) != 0):
            print("+", "+".join(finalEquationArr[i].remainder))
        else:
            print("\n")
 
# creating the bitstream
def createBitstream(myLUT):
    fileName = input("Enter filename for the bitstream:\n")
    f = open(fileName+".bit", "wb")

    pickle.dump(myLUT, f)
    
    f.close()

# reading the bitstream
def readBitstream():
    newLUT = LUT()
    fileNum = -1

    while(fileNum<1 or fileNum >= i):
        print("Choose the bitstream file, enter 0 if you want to exit.\n")
        i = 1
        dir = []
        for dirnames in os.listdir():
            print(str(i)+") "+ dirnames+"\n")
            dir.append(dirnames)
            i = i+1
        
        fileNum = int(input("Which file do you want to open? "))
        if(fileNum == 0):
            return newLUT

        # os.system('cls' if os.name == 'nt' else 'clear')
        
        if(fileNum<1 or fileNum >= i):
            print("Invalid choice\n\n")

    f = open(dir[fileNum-1], "rb")
    newLUT = pickle.load(f)
    f.close()

    return newLUT

def resourceAllocation(myLUT):
    # percentage of LUTs used
    print("Percentage of LUTs used:")
    print(str(myLUT.numLUT_used*100/myLUT.numLUT))

    # number of connections
    print("\nPercentage of connections: ")
    print(str(myLUT.totalConnections*100/((myLUT.LUTinputs+1)*myLUT.numLUT)))

    # total memory should be here
    print("\nTotal memory required: ")
    print(str(myLUT.totalConnections + (myLUT.numLUT_used*(2**myLUT.LUTinputs))) + " bits")




## V functions
# SOP Conversion Functions

def row_to_term(row):

    """Convert a binary string to a term for SOP."""

    variables = 'ABCDEFGH'

    return ''.join([f'{var}' if val == '1' else f'~{var}' if val == '0' else '' for var, val in zip(variables, row)])



def dec_to_bin(dec_num, num_vars):

    """Convert a decimal number to a binary string of length num_vars."""

    return format(dec_num, f'0{num_vars}b')



def bit_diff_count(a, b):

    """Count the number of differing bits between two binary strings."""

    return sum([av != bv for av, bv in zip(a, b)])



def simplify_sop(binary_combinations):

    """Attempt to simplify the SOP using a basic one-bit differ combination approach."""

    changes = True

    prev_combinations = binary_combinations.copy()

    

    while changes:

        changes = False

        new_combinations = set()

        marked = set()



        for i in range(len(prev_combinations)):

            for j in range(i+1, len(prev_combinations)):

                if bit_diff_count(prev_combinations[i], prev_combinations[j]) == 1:

                    changes = True

                    new_term = ''.join(['-' if av != bv else av for av, bv in zip(prev_combinations[i], prev_combinations[j])])

                    new_combinations.add(new_term)

                    marked.add(prev_combinations[i])

                    marked.add(prev_combinations[j])



        for term in prev_combinations:

            if term not in marked:

                new_combinations.add(term)



        prev_combinations = list(new_combinations)



    return prev_combinations









def parse_sop_formula(sop_formula, num_vars):

    terms = sop_formula.replace(" ", "").split("+")
    var_map = {chr(97 + i): i for i in range(num_vars)}  # Map 'a' to 0, 'b' to 1, etc.
    minterms = set()
    for term in terms:
        minterm = ['0'] * num_vars
        i = 0
        while i < len(term):
            if term[i] == '~':
                # If the variable is negated, skip it and move to the next variable
                i += 2
                continue
            # Set the corresponding bit in the minterm to '1'
            minterm[var_map[term[i]]] = '1'
            i += 1
        # Convert the binary minterm to decimal and add to the set
        minterms.add(int(''.join(minterm), 2))



    return list(minterms)

def findUniqueInputs(exp):
    temp = set()
    strT = []
    for e in exp:
        for t in e:
            for c in t:
                strT.append(c)

    temp = set(strT)
    temp = sorted(list(temp))
    inputDict = {}

    it = 0

    for lit in temp:
        inputDict[lit] = it
        it = it + 1


    return inputDict
    


def main():
    num_LUTs = int(input("Enter the number of LUTs: "))
    lut_type = int(input("Enter LUT type (4 or 6 inputs): "))
    # connectivity = input("Enter connectivity (fully/partially): ").lower()
    
    connectivity = "fully"

    logic_expressions = []
    use_independent_sop = input("Do you want to enter an independent SOP formula? (yes/no): ").lower()

    fullSimplifiedSOP = []

    if use_independent_sop == 'yes':

        num_expressions = int(input("Enter the number of logic expressions: "))

        for _ in range(num_expressions):
            num_vars = int(input("Enter the number of variables in the formula: "))
            sop_formula = input("Enter the independent SOP formula: ")
            decimal_numbers = parse_sop_formula(sop_formula, num_vars)
            binary_combinations = [dec_to_bin(dec, num_vars) for dec in decimal_numbers]
            simplified_combinations = simplify_sop(binary_combinations)
            simplified_terms = [row_to_term(row) for row in simplified_combinations]
            logic_expressions.append(' + '.join(simplified_terms))
            fullSimplifiedSOP.append(simplified_terms)

    else:

        num_expressions = int(input("Enter the number of logic expressions: "))
        for _ in range(num_expressions):
            num_vars = int(input("Enter the number of variables for this expression: "))
            print(f"Enter {num_vars} decimal numbers for the truth table of expression {_ + 1}:")
            decimal_numbers = list(map(int, input().split()))
            binary_combinations = [dec_to_bin(dec, num_vars) for dec in decimal_numbers]
            simplified_combinations = simplify_sop(binary_combinations)
            simplified_terms = [row_to_term(row) for row in simplified_combinations]
            logic_expressions.append(' + '.join(simplified_terms))
            fullSimplifiedSOP.append(simplified_terms)




    fpga = FPGA(num_LUTs, lut_type, connectivity)
    fullyBool = True

    interconnectionArr = []
    if connectivity == 'partially':
        fullyBool = False
        custom_connect = input("Do you want to set up custom connections? (yes/no): ").lower()
        if custom_connect == 'yes':
            fpga.setup_custom_connectivity()



    finalEq_simplified = createFinalEqArr(num_expressions)
    # changes all the nots to lower case
    exp_sim = changeExp(fullSimplifiedSOP, num_expressions)
    inputsDict = findUniqueInputs(exp_sim)
    # creates an array of the MLS object
    expressions_sim = createArray(exp_sim, num_expressions)
    # finds all the kernels of each expression
    kernelSearch(expressions_sim, num_expressions)
    # prints all the kernels
    ## FINDING ALL THE INTERSECTIONS OF THE KERNEL
    # find all the intersections of the kernels
    [listIntersections_sim, idealIntersections_sim]=findIntersections(expressions_sim, num_expressions)
    [finalEq_simplified, auxEq_sim]= findIdealIntersection(listIntersections_sim, num_expressions, finalEq_simplified, expressions_sim)
    
    # printFinalEquation(finalEq_simplified, auxEq_sim)

    # LUT assignment
    myLUT_sim = LUT()
    myLUT_sim.finalEq = finalEq_simplified
    myLUT_sim.auxEq = auxEq_sim
    myLUT_sim.assignVal(num_LUTs, lut_type, auxEq_sim, finalEq_simplified, fpga, fullyBool, inputsDict)
    # myLUT_sim.printEverything()

    return myLUT_sim

def inputWire(myLUT):

    inputDict = myLUT.inputsDict

    for key in inputDict.keys():
        print("INPUT "+str(key)+ " ->  WIRE " + str(inputDict[key])) 

def outputWire(myLUT):
    outDict = myLUT.outputDict

    for key in outDict.keys():
        print("LUT "+str(key)+ " ->  WIRE " + str(outDict[key])) 


def internalWires(myLUT):
    inputWire(myLUT)
    print("\n")
    outputWire(myLUT)
    outDict = myLUT.outputDict
    inputDict = myLUT.inputsDict
    dictLUT = myLUT.LUTdict

    for key in dictLUT.keys():
        print("LUT "+str(key))
        tempLUT = dictLUT[key]
        print("\nINPUT WIRES")

        for term in tempLUT.LUTdependents:
            print(str(outputDict[term]), end=", ")

        for term in tempLUT.wireDependents:
            for c in term:
                print(str(inputDict[c]), end=", ")

        print("\n\nOUTPUT WIRES")

        for term in tempLUT.dep2me:
            print(str((term*myLUT.LUTinputs)+len(inputDict)), end=", ")

        if(len(tempLUT.dep2me)== 0):
            print(str(outDict[key]), end="")

        print("\n")
        


def outputFunction(myLUT):
        
    printStatus = True

    while printStatus is True:

        print("\n\n1) Function assigned to the LUT\n2) Internal Connections \n3) External Input connections\n4) External output connections\n5) Store bitstream\n6) Resource allocation summary\n7) Go back! \n8) Stop the program!\n\n")
        choice = int(input("What is thy choice? "))
        os.system('cls' if os.name == 'nt' else 'clear')

        if(choice == 1):
            myLUT.printEverything()
        elif(choice == 2):
            internalWires(myLUT)
        elif(choice == 3):
            inputWire(myLUT)
        elif(choice == 4):
            outputWire(myLUT)
        elif choice == 5:
            createBitstream(myLUT)
        elif choice == 6:
            resourceAllocation(myLUT)
        elif choice == 7:
            printStatus = False
        elif choice == 8:
            exit()
        else:
            print("Invalid choice")


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    while True: 
        choice = int(input("Choose your method of input \n\n1) Type in your boolean function(s) in SOP format. \n2) Load bitstream\n\nWhat shall thee choose? "))
        os.system('cls' if os.name == 'nt' else 'clear')
        chosen = False
        if choice == 1:
            myLUT = main()  
            chosen = True
        elif choice == 2:
            myLUT = readBitstream()
            chosen = True
        else:
            print("Invalid input\n")

        if(chosen == True):
            outputFunction(myLUT)
