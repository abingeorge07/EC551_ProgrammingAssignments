import numpy as np
import os 
import pickle 
class LUT_object():
    def __init__(self):
        self.divisor = []
        self.quotient = []
        self.remainder = []

    def __init__(self, divisor, quotient, remainder):
        self.divisor = divisor
        self.quotient = quotient
        self.remainder = remainder
    
    def updateLUT(self, divisor, quotient, remainder):
        self.divisor = divisor
        self.quotient = quotient
        self.remainder = remainder

    def dependencies(self, LUT, wire, dependent2me):
        # if the input to this lut comes from another lut
        self.LUTdependents = LUT
        self.wireDependents = wire
        self.dep2me = dependent2me

class LUT():
    def __init__(self):
        self.numLUT = 0
        self.LUTinputs = 0

    def findColIndex(self, rowConnections, key):
        matrix = self.LUT_connections_MAT
        usedMat = self.LUTconnections_used



        for i in range(0, len(rowConnections)):
            newRowConnections = []
            found = False
            for j in range(0, self.numLUT):
                if(matrix[rowConnections[i]][j] == 1 and (rowConnections[i] not in self.newMap.values()) and (j not in self.newMap.values())):
                    newRowConnections.append(j)

            if(len(newRowConnections) > 0):
                found = True
                self.newMap [key] = rowConnections[i]
                self.indicesComp.remove(key)
                break

        if(not found):
            return False

        for i in range(0,len(self.LUTdict[key].dep2me)):
            tempLUT_index = self.LUTdict[key].dep2me[i]
            tempLUT = self.LUTdict[tempLUT_index]
            if len(tempLUT.dep2me) > 0:
                finalCol = self.findColIndex(rowConnections, tempLUT_index)
                if(finalCol == False):
                    return False
            else:
                iterator = 0
                exists = False
                while(iterator < len(rowConnections)):
                    exists = True
                    for j in range(0, self.numLUT):
                        if(matrix[rowConnections[iterator]][j] == 1):
                            exists = False
                            break

                    if(exists == True):
                        break
                    else:
                        iterator = iterator + 1

                if(exists == True):
                    self.newMap [tempLUT_index] = rowConnections[iterator]
                    self.indicesComp.remove(tempLUT_index)
                    return True
                else:
                    self.newMap [tempLUT_index] = rowConnections[0]
                    self.indicesComp.remove(tempLUT_index)
                    return True


    def findRowIndex(self, colConnections, key):
        matrix = self.LUT_connections_MAT
        usedMat = self.LUTconnections_used

        for i in range(0, len(colConnections)):
            newColConnections = []
            found = False
            for j in range(0, self.numLUT):
                if(matrix[colConnections[i]][j] == 1 and (colConnections[i] not in self.newMap.values()) and (j not in self.newMap.values())):
                    newColConnections.append(j)

            if(len(newRowConnections) > 0):                
                found = True
                self.newMap [key] = colConnections[i]
                self.indicesComp.remove(key)
                break

        if(not foundLUT):
            return False

        for i in range(0,len(self.LUTdict[key].LUTdependents)):
            tempLUT_index = self.LUTdict[key].LUTdependents[i]
            tempLUT = self.LUTdict[tempLUT_index]
            if len(tempLUT.LUTdependents) > 0:
                finalRow = self.findRowIndex(colConnections, tempLUT_index)
                if(finalRow == False):
                    return False
            else:
                iterator = 0
                exists = False
                while(iterator < len(colConnections)):
                    exists = True
                    for j in range(0, self.numLUT):
                        if(matrix[j][colConnections[iterator]] == 1):
                            exists = False
                            break

                    if(exists == True):
                        break
                    else:
                        iterator = iterator + 1

                if(exists == True):
                    self.newMap [tempLUT_index] = colConnections[iterator]
                    self.indicesComp.remove(tempLUT_index)
                else:
                    self.newMap [tempLUT_index] = colConnections[0]
                    self.indicesComp.remove(tempLUT_index)

        return True        

    def inputAndOuputConnections(self,key):
        matrix = self.LUT_connections_MAT
        usedMat = self.LUTconnections_used
        
        foundLUT = False
        for i in range(0, self.numLUT):
            #check ith row
            rowConnections =[]
            colConnections = []
            for j in range(0, self.numLUT):
                if(matrix[i][j] == 1 and (i not in self.newMap.values()) and (j not in self.newMap.values()) and i != j):
                    rowConnections.append(j)
            rowConnections.sort()

            for j in range(0, self.numLUT):
                if(matrix[j][i] == 1 and (i not in self.newMap.values()) and (j not in self.newMap.values()) and i != j):
                    colConnections.append(j)

            colConnections.sort()

            if(rowConnections != colConnections):
                foundLUT = True
                self.newMap [key] = i
                self.indicesComp.remove(key)
                break
        
        if(not foundLUT):
            return False

        for i in range(0,len(self.LUTdict[key].dep2me)):
            tempLUT_index = self.LUTdict[key].dep2me[i]
            tempLUT = self.LUTdict[tempLUT_index]
            if len(tempLUT.dep2me) > 0:
                finalCol = self.findColIndex(rowConnections, tempLUT_index)
                if(finalCol == False):
                    return False
            else:
                iterator = 0
                exists = False
                while(iterator < len(rowConnections)):
                    exists = True
                    for j in range(0, self.numLUT):
                        if(matrix[rowConnections[iterator]][j] == 1):
                            exists = False
                            break

                    if(exists == True):
                        break
                    else:
                        iterator = iterator + 1

                if(exists == True):
                    self.newMap [tempLUT_index] = rowConnections[iterator]
                    self.indicesComp.remove(tempLUT_index)
                else:
                    self.newMap [tempLUT_index] = rowConnections[0]
                    self.indicesComp.remove(tempLUT_index)
            


        for i in range(0,len(self.LUTdict[key].LUTdependents)):
            tempLUT_index = self.LUTdict[key].LUTdependents[i]
            tempLUT = self.LUTdict[tempLUT_index]
            if len(tempLUT.LUTdependents) > 0:
                finalRow = self.findRowIndex(colConnections, tempLUT_index)
                if(finalRow == False):
                    return False
            else:
                iterator = 0
                exists = False
                while(iterator < len(colConnections)):
                    exists = True
                    for j in range(0, self.numLUT):
                        if(matrix[j][colConnections[iterator]] == 1):
                            exists = False
                            break

                    if(exists == True):
                        break
                    else:
                        iterator = iterator + 1

                if(exists == True):
                    self.newMap [tempLUT_index] = colConnections[iterator]
                    self.indicesComp.remove(tempLUT_index)
                else:
                    self.newMap [tempLUT_index] = colConnections[0]
                    self.indicesComp.remove(tempLUT_index)

        return True

    def outputConnections(self,key):
        matrix = self.LUT_connections_MAT
        usedMat = self.LUTconnections_used
        
        foundLUT = False
        for i in range(0, self.numLUT):
            #check ith row
            rowConnections =[]
            for j in range(0, self.numLUT):
                if(matrix[i][j] == 1 and (i not in self.newMap.values()) and (j not in self.newMap.values())  and i != j):
                    rowConnections.append(j)
            

            if(len(rowConnections) >= 0 ):
                foundLUT = True
                self.newMap [key] = i
                self.indicesComp.remove(key)
                break
        
        if(not foundLUT):
            return False

        for i in range(0,len(self.LUTdict[key].dep2me)):
            tempLUT_index = self.LUTdict[key].dep2me[i]
            tempLUT = self.LUTdict[tempLUT_index]
            if len(tempLUT.dep2me) > 0:
                finalCol = self.findColIndex(rowConnections, tempLUT_index)
                if(finalCol == False):
                    return False
            else:
                iterator = 0
                exists = False
                while(iterator < len(rowConnections)):
                    exists = True
                    for j in range(0, self.numLUT):
                        if(matrix[rowConnections[iterator]][j] == 1):
                            exists = False
                            break

                    if(exists == True):
                        break
                    else:
                        iterator = iterator + 1

                if(exists == True):
                    self.newMap [tempLUT_index] = rowConnections[iterator]
                    self.indicesComp.remove(tempLUT_index)
                else:
                    self.newMap [tempLUT_index] = rowConnections[0]
                    self.indicesComp.remove(tempLUT_index)


        return True


    def inputConnections(self,key):
        matrix = self.LUT_connections_MAT
        usedMat = self.LUTconnections_used
        
        foundLUT = False
        for i in range(0, self.numLUT):
            colConnections = []
            
            for j in range(0, self.numLUT):
                if(matrix[j][i] == 1 and (i not in self.newMap.values()) and (j not in self.newMap.values()) and i != j):
                    colConnections.append(j)

            if(len(colConnections) > 0):
                foundLUT = True
                self.newMap [key]= i
                self.indicesComp.remove(key)
                break
        
        if(not foundLUT):
            return False

        for i in range(0,len(self.LUTdict[key].LUTdependents)):
            tempLUT_index = self.LUTdict[key].LUTdependents[i]
            tempLUT = self.LUTdict[tempLUT_index]
            if len(tempLUT.LUTdependents) > 0:
                finalRow = self.findRowIndex(colConnections, tempLUT_index)
                if(finalRow == False):
                    return False
            else:
                iterator = 0
                exists = False
                while(iterator < len(colConnections)):
                    exists = True
                    for j in range(0, self.numLUT):
                        if(matrix[j][colConnections[iterator]] == 1):
                            exists = False
                            break

                    if(exists == True):
                        break
                    else:
                        iterator = iterator + 1

                if(exists == True):
                    self.newMap [tempLUT_index]= colConnections[iterator]
                    self.indicesComp.remove(tempLUT_index)
                else:
                    self.newMap [tempLUT_index] = colConnections[0]
                    self.indicesComp.remove(tempLUT_index)

        return True


    def mapAppropriately(self):

        self.indicesComp = [*range(0,self.numLUT,1)]
        self.newMap = {}

    
        while(len(self.indicesComp) > 0):
            for key in self.indicesComp :
                tempLUT = self.LUTdict[key]
                if(len(tempLUT.dep2me) > 0 and len(tempLUT.LUTdependents)>0):
                    tempOut = self.inputAndOuputConnections(key)
                    if (tempOut == False):
                        return False

                elif(len(tempLUT.dep2me) > 0 ):
                    tempOut = self.outputConnections(key)
                    if (tempOut == False):
                        return False
                elif (len(tempLUT.LUTdependents)>0):   
                    tempOut = self.inputConnections(key)
                    if (tempOut == False):
                        return False   
                else:
                    self.newMap[key] = key
                    self.indicesComp.remove(key)
                
                print(self.newMap)
                input("Pause")



    def assignVal(self, numLUT, LUTsize, auxFun, allFunc, fpga, fullyBool, inputsDict):
        self.numLUT = numLUT
        self.LUTinputs = LUTsize
        self.numLUT_used = 0
        self.inputsDict = inputsDict
        self.outputDict = self.findOutputDict()
        self.LUTconnections_used = np.zeros((numLUT, numLUT))
        if(not fullyBool):
            self.LUT_connections_MAT = self.convertLUTconnections_toMat(fpga)
        self.LUTdict = {}   
        self.function2LUT={}
        self.assignAuxFun(auxFun)
        self.assignMainFun(allFunc)
        if(not fullyBool):
            self.mapAppropriately()
        self.findNumberConnections()
        if(self.numLUT_used > self.numLUT):
            print("NOT ENOUGH LUTS\n")
            print("NEEDS ATLEAST "+str(self.numLUT_used) +" LUTS.\n")
            input("Press enter to continue")

    def findOutputDict(self):
        outDict = {}

        for i in range(0, self.numLUT):
            outDict[i] = len(self.inputsDict) + (self.numLUT * self.LUTinputs) + i

        return outDict
        

    def convertLUTconnections_toMat(self, fpga):
        
        outputMat = np.zeros((self.numLUT, self.numLUT))
        for i,  lut in enumerate(fpga.luts):

            for conn in lut.connections:
                outputMat[i][fpga.luts.index(conn)] = 1

        return outputMat
  

    def findNumberConnections(self):
        totalConnections = 0
        
        for key in self.LUTdict.keys():
            temp = self.LUTdict[key]
            if(len(temp.wireDependents) > 0):
                totalConnections = totalConnections + len(temp.wireDependents[0]) 
            totalConnections = len(temp.LUTdependents) + totalConnections
        self.totalConnections = totalConnections

    def assignAuxFun(self, auxFun):
        
        mainDivisor = []
        mainQuotient = []

        for i in range(0, len(auxFun)):

            dependent = 0
            iterator = 0
            prevLUT = -1
            dependentArr = []
            strTemp = "F"+str(i+1)
            tempFunction = auxFun[i].remainder

            while(len(tempFunction) > 0 ):
                if(iterator > 0):
                    dependent = 1
                
                wireDepend = []
                mainFunction = []
                currentLiterals = 0

                for i in range(0, len(tempFunction)):
                    mainFunction.append(tempFunction[i])
                    numLiterals = self.countLiterals(mainDivisor, mainQuotient, mainFunction)
                    if(numLiterals > self.LUTinputs-dependent):
                        mainFunction[len(mainFunction)-1] = ""
                    else:
                        currentLiterals = numLiterals
                        tempFunction[i] =""

                # removing all the empty list element
                tempFunction = [s for s in tempFunction if s != ""]
                mainFunction = [s for s in mainFunction if s != ""]
                
                
                # finding all the wire dependencies to the LUT
                b = set()
                b.add("".join(mainFunction))
                b = list(b)
                wireDepend = [s for s in b if s != ""]

            
                # Updating the current LUT 
                iterator = iterator + 1
                self.LUTdict[self.numLUT_used] = LUT_object(1, mainFunction, 0)
                
                if(len(tempFunction) > 0):
                    dependent2me =[self.numLUT_used + 1]
                else:
                    dependent2me = []   

                self.LUTdict[self.numLUT_used].dependencies(dependentArr, wireDepend,dependent2me)

                # Updating for next LUT
                dependentArr = [self.numLUT_used]
                self.numLUT_used = self.numLUT_used + 1          
                             
                
            self.function2LUT[strTemp] = self.numLUT_used -1


    def countLiterals(self, div, quo, rem):
        tempDiv = set("".join(div))
        tempQuo = set(quo)
        tempRem = set("".join(rem))
        tempUnion = tempDiv.union(tempQuo)
        tempUnion = tempUnion.union(tempRem)
        # print(tempUnion)
        return len(tempUnion)
        # input("Pause")


    def findNumLiteral(self, name, divisor, quotient, remainder):
        dependent = 0
        iterator = 0
        prevLUT = -1
        dependentArr = []


        while(len(divisor) > 0 or len(remainder)>0 ):
            if(iterator > 0):
                dependent = 1
            
            mainDivisor = []
            mainQuotient = []
            mainRemainder = []
            wireDepend = []
            currentLiterals = 0

            for i in range(0, len(divisor)):
                mainDivisor.append(divisor[i])
                mainQuotient.append(quotient[i][0])
                
                numLiterals = self.countLiterals(mainDivisor, mainQuotient, mainRemainder)
                if(numLiterals > self.LUTinputs-dependent):
                    mainDivisor[len(mainDivisor)-1] = ""
                    mainQuotient[len(mainQuotient)-1] = ""
                else:
                    currentLiterals = numLiterals
                    divisor[i] = ""
                    quotient[i] =""
                    


            for i in range(0, len(remainder)):
                mainRemainder.append(remainder[i])
                numLiterals = self.countLiterals(mainDivisor, mainQuotient, mainRemainder)
                if(numLiterals > self.LUTinputs-dependent):
                    mainRemainder[len(mainRemainder)-1] = ""
                else:
                    currentLiterals = numLiterals
                    remainder[i] =""

            # removing all the empty list elements
            divisor = [s for s in divisor if s != ""]
            quotient = [s for s in quotient if s != ""]
            remainder = [s for s in remainder if s != ""]
            mainDivisor = [s for s in mainDivisor if s != ""]
            mainQuotient = [s for s in mainQuotient if s != ""]
            mainRemainder = [s for s in mainRemainder if s != ""]
            
            
            # finding all the LUT dependencies to the LUT
            a = set()
            strTemp = ""
            # print(mainQuotient)
            # input("Pause")
            for i in range(0,len(mainQuotient)):
                if(mainQuotient[i][0] == "F"):
                    a.add(self.function2LUT[mainQuotient[i]])
                else:
                    strTemp = strTemp.join(mainQuotient[i])
                    # print(strTemp)
                    # input("Pause")
            a = list(a)
            for i in range(0,len(a)):
                dependentArr.append(a[i])

            # finding all the wire dependencies to the LUT
            b = set()
            b.add(strTemp)
            b.add("".join(mainDivisor))
            b.add("".join(mainRemainder))
            b = list(b)
            wireDepend = [s for s in b if s != ""]
        
            if(len(mainDivisor) == 0):
                mainDivisor = 1
            if(len(mainRemainder) == 0):
                mainRemainder = 0

            # Updating the current LUT 
            iterator = iterator + 1
            # print(mainQuotient)
            # print(mainRemainder)
            # print(mainDivisor)
            # input("Pause")

            if(len(divisor) > 0 or len(remainder)>0 ):
                dependent2me = [self.numLUT_used+1]
            else:
                dependent2me = []

            self.LUTdict[self.numLUT_used] = LUT_object(mainDivisor, mainQuotient, mainRemainder)
            self.LUTdict[self.numLUT_used].dependencies(dependentArr, wireDepend, dependent2me)

            # Updating for next LUT
            dependentArr = [self.numLUT_used]
            self.numLUT_used = self.numLUT_used + 1
     

        self.function2LUT[name] = self.numLUT_used - 1

    def assignMainFun(self, allFunctions):
        for i in range(0, len(allFunctions)):
            self.findNumLiteral(allFunctions[i].functionName, allFunctions[i].divisor, allFunctions[i].quotient, allFunctions[i].remainder)
        
    # Prints all information of the LUT
    def printEverything(self):

        lutNUM = int(input("Which LUT would you like to inspect from 0 - "+str(self.numLUT_used - 1)+"? \nIf -1 entered then all LUT assignments will be displayed\n"))

        if(lutNUM>-1 and lutNUM<self.numLUT_used ):
            key = lutNUM
            # LUT number
            print("LUT "+str(key))

            LUT_temp = self.LUTdict[key]
            functionPrinted = 0

            # print function
            print("Function")


            if LUT_temp.divisor == 1 :
                print("+".join(LUT_temp.quotient), end="")
            else:                
                for j in range(0, len(LUT_temp.divisor)):
                    if j != 0:
                        print("+", end = "")
                    print("(" + LUT_temp.quotient[j]+")" + LUT_temp.divisor[j], end="")
                    functionPrinted = 1
        
            if LUT_temp.remainder != 0:
                if(len(LUT_temp.remainder) != 0 ):
                    if(functionPrinted == 1):
                        print("+", end="")
                    print("+".join(LUT_temp.remainder), end="")

            if (len(LUT_temp.LUTdependents) > 0):
                for j in LUT_temp.LUTdependents:
                    print(" + L"+str(j))
                
            print("\n")
        
        elif (lutNUM == -1):

            for key in self.LUTdict.keys():
                # LUT number
                print("LUT "+str(key))

                LUT_temp = self.LUTdict[key]
                functionPrinted = 0

                # print function
                print("Function")


                if LUT_temp.divisor == 1 :
                    print("+".join(LUT_temp.quotient), end="")
                else:                
                    for j in range(0, len(LUT_temp.divisor)):
                        if j != 0:
                            print("+", end = "")
                        print("(" + LUT_temp.quotient[j]+")" + LUT_temp.divisor[j], end="")
                        functionPrinted = 1
                
                

                if LUT_temp.remainder != 0:
                    if(len(LUT_temp.remainder) != 0 ):
                        if(functionPrinted == 1):
                            print("+", end="")
                        print("+".join(LUT_temp.remainder), end="")

                if (len(LUT_temp.LUTdependents) > 0):
                    for j in LUT_temp.LUTdependents:
                        print(" + L"+str(j))
                    
                print("\n")



        # key_list=list(self.function2LUT.keys())
        # val_list=list(self.function2LUT.values())


        # for key in self.LUTdict.keys():
        #     LUT_temp = self.LUTdict[key]
        #     functionPrinted = 0

        #     # LUT number
        #     print("LUT "+str(key))


        #     # print function
        #     print("Function")

        #     if LUT_temp.divisor == 1 :
        #         print("+".join(LUT_temp.quotient), end="")
        #     else:                
        #         for j in range(0, len(LUT_temp.divisor)):
        #             if j != 0:
        #                 print("+", end = "")
        #             print("(" + LUT_temp.quotient[j]+")" + LUT_temp.divisor[j], end="")
        #             functionPrinted = 1
            
            

        #     if LUT_temp.remainder != 0:
        #         if(len(LUT_temp.remainder) != 0 ):
        #             if(functionPrinted == 1):
        #                 print("+", end="")
        #             print("+".join(LUT_temp.remainder))
                
        #     print("\n")

        #     # LUT dependencies
        #     print("Dependent on the following LUTs:")
        #     print(LUT_temp.LUTdependents)

        #     print("LUTS dependent on this LUT:")
        #     print(LUT_temp.dep2me)

        #     # Wire dependencies
        #     print("Dependent on the following wires:")
        #     print(LUT_temp.wireDependents)

        #     #Print function name
        #     print("Function Output: ", end="")

        #     if (key in val_list):
        #         ind = val_list.index(key)
        #         print(key_list[ind])              
        #     else:
        #         print("Intermediate output")

        #     print("\n\n")

 
