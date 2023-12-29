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


            if(len(newRowConnections) >= len(self.LUTdict[key].dep2me)):
                found = True
                self.newMap [key] = rowConnections[i]
                self.indicesComp.remove(key)
                break

        # print(self.newMap)
        # print(found)
        # print(i)
        # print(newRowConnections)
        # print(len(self.LUTdict[key].dep2me))
        # input("Pause 7")

        if(not found):
            return False


        rowConnections = newRowConnections[:]

        for i in range(0,len(self.LUTdict[key].dep2me)):
            tempLUT_index = self.LUTdict[key].dep2me[i]
            tempLUT = self.LUTdict[tempLUT_index]
            if len(tempLUT.dep2me) > 0:
                finalCol = self.findColIndex(rowConnections, tempLUT_index)
                # print(finalCol)
                # input("Pause 6")
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

                doneBool = False
                # print(exists)
                # input("Pause 8")
                if(exists == True):
                    tempNum= rowConnections[iterator]
                    if tempNum not in self.newMap.values():
                        self.newMap [tempLUT_index] = tempNum
                        rowConnections.remove(self.newMap [tempLUT_index])
                        self.indicesComp.remove(tempLUT_index)
                        doneBool = True
                    else:
                        rowConnections.remove(tempNum)
                if(doneBool == False):
                    for term in rowConnections:
                        tempNum = term
                        # print(tempNum)
                        # print(self.newMap.values())
                        # input("Pause 9")
                        if tempNum not in self.newMap.values():
                            self.newMap [tempLUT_index] = tempNum
                            rowConnections.remove(self.newMap [tempLUT_index])
                            self.indicesComp.remove(tempLUT_index)
                            # print(self.newMap)
                            # print(self.indicesComp)
                            # input("Pause 12")
                            doneBool = True
                            break
                        else:
                            rowConnections.remove(tempNum)

                if(len(rowConnections) == 0 and doneBool == False):
                    return False
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

            if(len(newColConnections) >= len(self.LUTdict[key].LUTdependents)):                
                found = True
                self.newMap [key] = colConnections[i]
                self.indicesComp.remove(key)
                break

        if(not foundLUT):
            return False

        colConnections = newColConnections
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

                doneBool = False
                if(exists == True):
                    tempNum= colConnections[iterator]

                    if tempNum not in self.newMap.values():
                        self.newMap [tempLUT_index] = tempNum
                        colConnections.remove(self.newMap [tempLUT_index])
                        self.indicesComp.remove(tempLUT_index)
                        doneBool = True
                    else:
                        colConnections.remove(tempNum)
                if(doneBool == False):
                    for term in colConnections:
                        tempNum = term

                        if tempNum not in self.newMap.values():
                            self.newMap [tempLUT_index] = tempNum
                            colConnections.remove(self.newMap [tempLUT_index])
                            self.indicesComp.remove(tempLUT_index)
                            doneBool = True
                            break
                        else:
                            colConnections.remove(tempNum)

                if(len(colConnections) == 0 and doneBool == False):
                    return False

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

            # need to check if there is enough input for the dependents and enout
            # for the dep2me
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

                doneBool = False
                if(exists == True):
                    tempNum= rowConnections[iterator]

                    if tempNum not in self.newMap.values():
                        self.newMap [tempLUT_index] = tempNum
                        rowConnections.remove(self.newMap [tempLUT_index])
                        self.indicesComp.remove(tempLUT_index)
                        doneBool = True
                    else:
                        rowConnections.remove(tempNum)
               
                if(doneBool == False):
                    for term in rowConnections:
                        tempNum = term

                        if tempNum not in self.newMap.values():
                            self.newMap [tempLUT_index] = tempNum
                            rowConnections.remove(self.newMap [tempLUT_index])
                            self.indicesComp.remove(tempLUT_index)
                            doneBool = True
                            break
                        else:
                            rowConnections.remove(tempNum)

                if(len(rowConnections) == 0 and doneBool == False):
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


                doneBool = False
                if(exists == True):
                    tempNum= colConnections[iterator]

                    if tempNum not in self.newMap.values():
                        self.newMap [tempLUT_index] = tempNum
                        colConnections.remove(self.newMap [tempLUT_index])
                        self.indicesComp.remove(tempLUT_index)
                        doneBool = True
                    else:
                        colConnections.remove(tempNum)
                
                if(doneBool == False):
                    for term in colConnections:
                        tempNum = term

                        if tempNum not in self.newMap.values():
                            self.newMap [tempLUT_index] = tempNum
                            colConnections.remove(self.newMap [tempLUT_index])
                            self.indicesComp.remove(tempLUT_index)
                            doneBool = True
                            break
                        else:
                            colConnections.remove(tempNum)

                if(len(colConnections) == 0 and doneBool == False):
                    return False

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
            

            if(len(rowConnections) >= len(self.LUTdict[key].dep2me)):
                foundLUT = True
                self.newMap [key] = i
                self.indicesComp.remove(key)
                break
        
        print(self.newMap)
        print(i)
        print(rowConnections)
        print(len(self.LUTdict[key].dep2me))
        input("Pause 4")
        if(not foundLUT):
            return False

        for i in range(0,len(self.LUTdict[key].dep2me)):
            tempLUT_index = self.LUTdict[key].dep2me[i]
            tempLUT = self.LUTdict[tempLUT_index]

            if len(tempLUT.dep2me) > 0:
                finalCol = self.findColIndex(rowConnections, tempLUT_index)
                print(finalCol)
                input("Pause 5")
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
                print(exists)
                input("quick check")
                doneBool = False
                if(exists == True):
                    tempNum= rowConnections[iterator]

                    if tempNum not in self.newMap.values():
                        self.newMap [tempLUT_index] = tempNum
                        rowConnections.remove(self.newMap [tempLUT_index])
                        self.indicesComp.remove(tempLUT_index)
                        doneBool = True
                    else:
                        rowConnections.remove(tempNum)
                
                if(doneBool == False):
                    for term in rowConnections:
                        tempNum = term

                        if tempNum not in self.newMap.values():
                            self.newMap [tempLUT_index] = tempNum
                            rowConnections.remove(self.newMap [tempLUT_index])
                            self.indicesComp.remove(tempLUT_index)
                            doneBool = True
                            break
                        else:
                            rowConnections.remove(tempNum)

                # print(self.indicesComp)
                if(len(rowConnections) == 0 and doneBool == False):
                    return False


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

            if(len(colConnections) >= len(self.LUTdict[key].LUTdependents)):
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

                doneBool = False
                if(exists == True):
                    tempNum= colConnections[iterator]

                    if tempNum not in self.newMap.values():
                        self.newMap [tempLUT_index] = tempNum
                        colConnections.remove(self.newMap [tempLUT_index])
                        self.indicesComp.remove(tempLUT_index)
                        doneBool = True
                    else:
                        colConnections.remove(tempNum)
               
                if(doneBool == False):
                    for term in colConnections:
                        tempNum = term

                        if tempNum not in self.newMap.values():
                            self.newMap [tempLUT_index] = tempNum
                            colConnections.remove(self.newMap [tempLUT_index])
                            self.indicesComp.remove(tempLUT_index)
                            doneBool = True
                            break
                        else:
                            colConnections.remove(tempNum)

                if(len(colConnections) == 0) and doneBool == False:
                    return False

        return True

    def mapAppropriately(self):

        self.indicesComp = [*range(0,self.numLUT_used,1)][:]
        self.newMap = {}

    
        while(len(self.indicesComp) > 0):
            # for key in self.indicesComp :
            key = self.indicesComp[0]
            tempLUT = self.LUTdict[key]
       
            if(len(tempLUT.dep2me) > 0 and len(tempLUT.LUTdependents)>0):
                tempOut = self.inputAndOuputConnections(key)
                # print(tempOut)
                # input("Pause 1")
                if (tempOut == False):
                    return False

            elif(len(tempLUT.dep2me) > 0 ):
                tempOut = self.outputConnections(key)
                # print(tempOut)
                # input("Pause 2")
                # print(len(self.indicesComp))
                if (tempOut == False):
                    return False
            elif (len(tempLUT.LUTdependents)>0):   
                tempOut = self.inputConnections(key)
                # print(tempOut)
                # input("Pause 3")

                if (tempOut == False):
                    return False   

            else:
                self.newMap[key] = key
                self.indicesComp.remove(key)

        return True

    def assignVal(self, numLUT, LUTsize, auxFun, allFunc, fpga, fullyBool, inputsDict):
        self.numLUT = numLUT
        self.LUTinputs = LUTsize
        self.numLUT_used = 0
        self.inputsDict = inputsDict
        self.outputDict = self.findOutputDict()
        self.LUTconnections_used = np.zeros((numLUT, numLUT))
        self.fullyBool = True
        if(not fullyBool):
            self.fullyBool = False
            self.LUT_connections_MAT = self.convertLUTconnections_toMat(fpga)
        self.LUTdict = {}   
        self.function2LUT={}
        self.assignAuxFun(auxFun)
        self.assignMainFun(allFunc)
        self.partialConfig = False
        
        
        if(not fullyBool):
            a = self.mapAppropriately()
            if(a == True):
                self.partialConfig = True
        
        self.findNumberConnections()
        
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

    def termBreak(self, function, functionName):
        div = []
        quot = []
        strTemp = "F"+str(functionName)
        tempFunction = list(function)[:]

        dependent = 0
        iterator = 0
        prevLUT = -1
        dependentArr = []

        while(len(tempFunction) > (self.LUTinputs - dependent)):

            if(iterator > 0):
                dependent = 1

            skip = False
            wireDepend = []
            mainFunction = []
            currentLiterals = 0

            for i in range(0, len(tempFunction)):
                mainFunction.append(tempFunction[i])
                numLiterals = self.countLiterals(div, quot, mainFunction)
    
                if(numLiterals > self.LUTinputs-dependent):
                    mainFunction[len(mainFunction)-1] = ''
                else:
                    currentLiterals = numLiterals
                    tempFunction[i] = ''

            # removing all the empty list element
            tempFunction = [s for s in tempFunction if s != '']
            mainFunction = [s for s in mainFunction if s != '']

            # finding all the wire dependencies to the LUT
            b = set()
            b.add("".join(mainFunction))
            b = list(b)
            wireDepend = [s for s in b if s != ""]

            mainFunction = ["".join(mainFunction)]
        
            for key in self.LUTdict.keys():
                if self.LUTdict[key].quotient == mainFunction:
                    skip = True
                    # Updating for next LUT
                    dependentArr = [key]

            # Updating the current LUT 
            if skip is False:
                iterator = iterator + 1
                self.LUTdict[self.numLUT_used] = LUT_object(1, mainFunction, 0)
                
                if(len(tempFunction) > 0):
                    dependent2me =[self.numLUT_used + 1]
                else:
                    dependent2me = []


                self.LUTdict[self.numLUT_used].dependencies(dependentArr, wireDepend,dependent2me)

                # sanity check
                for j in dependentArr:
                    if(self.numLUT_used not in self.LUTdict[j].dep2me):
                        self.LUTdict[j].dep2me.append(self.numLUT_used)


                # Updating for next LUT
                dependentArr = [self.numLUT_used]
                self.numLUT_used = self.numLUT_used + 1  

        self.function2LUT[strTemp] = self.numLUT_used -1

        if len(tempFunction) > 0:
            leave = False
            tempFunction = "".join(tempFunction)
            depL = self.numLUT_used - 1
        else:
            leave = True

        return tempFunction, leave, depL

    def assignAuxFun(self, auxFun):
        
        mainDivisor = []
        mainQuotient = []

        for i in range(0, len(auxFun),):

            dependent = 0
            iterator = 0
            prevLUT = -1
            dependentArr = []
            leaveNow = False
            strTemp = "F"+str(i+1)
            tempFunction = auxFun[i].remainder[:]

            while(len(tempFunction) > 0 ):
                if(iterator > 0):
                    dependent = 1
                
                wireDepend = []
                mainFunction = []
                currentLiterals = 0

                for i in range(0, len(tempFunction)):
                    if(len(tempFunction[i]) >= self.LUTinputs-dependent):
                        t, leaveNow, depL = self.termBreak(tempFunction[i], i+1)
                    
                        if(leaveNow is True):
                            break
                        else:
                            leaveNow = False
                            tempFunction[i] = t
                            dependentArr = [depL]

                    mainFunction.append(tempFunction[i])
                    numLiterals = self.countLiterals(mainDivisor, mainQuotient, mainFunction)
                    if(numLiterals > self.LUTinputs-dependent):
                        mainFunction[len(mainFunction)-1] = ""
                    else:
                        currentLiterals = numLiterals
                        tempFunction[i] =""

                if(leaveNow is True):
                    break

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

                # sanity check
                for j in dependentArr:
                    if(self.numLUT_used not in self.LUTdict[j].dep2me):
                        self.LUTdict[j].dep2me.append(self.numLUT_used)

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
        
        if "1" in tempUnion:
            tempUnion.discard("1")
      
        # print(tempUnion)
        # input ("Pause3")
        return len(tempUnion)

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
            

            if(len(divisor) > 0 or len(remainder)>0 ):
                dependent2me = [self.numLUT_used+1]
            else:
                dependent2me = []

            self.LUTdict[self.numLUT_used] = LUT_object(mainDivisor, mainQuotient, mainRemainder)
            self.LUTdict[self.numLUT_used].dependencies(dependentArr, wireDepend, dependent2me)

            for j in dependentArr:
                if(self.numLUT_used not in self.LUTdict[j].dep2me):
                    self.LUTdict[j].dep2me.append(self.numLUT_used)
            
            # Updating for next LUT
            dependentArr = [self.numLUT_used]
            self.numLUT_used = self.numLUT_used + 1
    

        self.function2LUT[name] = self.numLUT_used - 1

    def assignMainFun(self, allFunctions):
        for i in range(0, len(allFunctions)):
        
            if(len(allFunctions[i].divisor) == 1 and allFunctions[i].divisor[0] == "1" and len(allFunctions[i].remainder) == 0):
                lutTemNum = self.function2LUT[(allFunctions[i].quotient[0])[0]]
                # self.LUTdict[lutTemNum].dep2me.append(int(round((self.outputDict[lutTemNum]-len(self.inputsDict))/self.LUTinputs)))
            else:
                self.findNumLiteral(allFunctions[i].functionName, allFunctions[i].divisor, allFunctions[i].quotient, allFunctions[i].remainder)
        
    # Prints all information of the LUT
    def printEverything(self):

        lutNUM = int(input("Which LUT would you like to inspect from 0 - "+str(self.numLUT_used - 1)+"? \nIf -1 entered then all LUT assignments will be displayed\n"))

        func2LUT_values = list(self.function2LUT.values())
        func2LUT_keys = list(self.function2LUT.keys())
   

        
        if(lutNUM>-1 and (lutNUM<self.numLUT_used or lutNUM <self.numLUT)):

            if(lutNUM >= self.numLUT_used and lutNUM < self.numLUT):
                print("LUT "+str(lutNUM))
                print("UNASSIGNED LUT")

            else:
                key = lutNUM
                # LUT number
                if(self.fullyBool == False and self.partialConfig == True):
                    k = self.newMap.keys()
                    v = self.newMap.values()
                    indexConcern = v.index(key)
                    myKey = k[indexConcern]
                    print("LUT "+str(key))
                    LUT_temp = self.LUTdict[myKey]
                else:
                    print("LUT "+str(key))
                    LUT_temp = self.LUTdict[key]

                functionPrinted = 0

                # print function
                print("Function")

                tempLUT = LUT_temp

                if key in func2LUT_values:
                    indChoice = func2LUT_values.index(key)
                    print(str(func2LUT_keys[indChoice]) +" = ", end="")

                if LUT_temp.divisor == 1 :
                    for i in range(0, len(tempLUT.quotient)):
                        tempTerm = tempLUT.quotient[i]

                        for c in tempTerm:
                            if c.isupper() or c.isdigit():
                                print(c, end="")
                            else:
                                print("~"+c.upper(), end="")
                        
                        if(i != len(tempLUT.quotient)-1):
                            print("+", end = "")
                else:                
                    for j in range(0, len(LUT_temp.divisor)):
                        if j != 0:
                            print("+", end = "")
                        print("(" + LUT_temp.quotient[j]+")" , end="")
                        for c in LUT_temp.divisor[j]:
                            if(c.isupper() or c.isdigit()):
                                print(c, end="")
                            else:
                                print("~"+c.upper(), end="")

                        functionPrinted = 1
            
                if LUT_temp.remainder != 0:
                    if(len(LUT_temp.remainder) != 0 ):
                        if(functionPrinted == 1):
                            print("+", end="")
                        # print("+".join(LUT_temp.remainder), end="")

                        for i in range(0, len(tempLUT.remainder)):
                            tempTerm = tempLUT.remainder[i]

                            for c in tempTerm:
                                if c.isupper() or c.isdigit():
                                    print(c, end="")
                                else:
                                    print("~"+c.upper(), end="")   
                            if(i != len(tempLUT.remainder)-1):
                                print("+", end = "")

                # if (len(LUT_temp.LUTdependents) > 0):
                #     for j in LUT_temp.LUTdependents:
                #         print(" + L"+str(j)m , end="")
                    
                print("\n")
        
        else:

            for key in self.LUTdict.keys():
                # LUT number
                if(self.fullyBool == False and self.partialConfig == True):
                    myKey = self.newMap[key]
                    print("LUT "+str(myKey))
                    LUT_temp = self.LUTdict[key]
                else:
                    print("LUT "+str(key))
                    LUT_temp = self.LUTdict[key]

                functionPrinted = 0

                # print function
                print("Function")
                tempLUT = LUT_temp

                if key in func2LUT_values:
                    indChoice = func2LUT_values.index(key)
                    print(str(func2LUT_keys[indChoice]) +" = ", end="")

                if LUT_temp.divisor == 1 :
                    for i in range(0, len(tempLUT.quotient)):
                        tempTerm = tempLUT.quotient[i]

                        for c in tempTerm:
                            if c.isupper() or c.isdigit():
                                print(c, end="")
                            else:
                                print("~"+c.upper(), end="")
                        
                        if(i != len(tempLUT.quotient)-1):
                            print("+", end = "")
                else:                
                    for j in range(0, len(LUT_temp.divisor)):
                        if j != 0:
                            print("+", end = "")
                        print("(" + LUT_temp.quotient[j]+")", end="")
                        for c in LUT_temp.divisor[j]:
                            if(c.isupper() or c.isdigit()):
                                print(c, end="")
                            else:
                                print("~"+c.upper(), end="")
                        functionPrinted = 1
                
                

                if LUT_temp.remainder != 0:
                    if(len(LUT_temp.remainder) != 0 ):
                        if(functionPrinted == 1):
                            print("+", end="")
                        # print("+".join(LUT_temp.remainder), end="")

                        for i in range(0, len(tempLUT.remainder)):
                            tempTerm = tempLUT.remainder[i]

                            for c in tempTerm:
                                if c.isupper() or c.isdigit():
                                    print(c, end="")
                                else:
                                    print("~"+c.upper(), end="")   
                            if(i != len(tempLUT.remainder)-1):
                                print("+", end = "")

                # if (len(LUT_temp.LUTdependents) > 0):
                #     for j in LUT_temp.LUTdependents:
                #         print(" + L"+str(j))
                    
                print("\n")

            if(self.numLUT > self.numLUT_used):
                for i in range(self.numLUT_used, self.numLUT):
                    print("LUT "+str(i))
                    print("UNASSIGNED LUT")

    def printHighLevel_info(self):

        key_list=list(self.function2LUT.keys())
        val_list=list(self.function2LUT.values())


        for key in self.LUTdict.keys():

            if(self.fullyBool == False and self.partialConfig == True):
                myKey = self.newMap[key]
                print("LUT "+str(myKey))
                LUT_temp = self.LUTdict[key]
            else:
                print("LUT "+str(key))
                LUT_temp = self.LUTdict[key]

            LUT_temp = self.LUTdict[key]
            functionPrinted = 0


            # print function
            print("Function")
            tempLUT = LUT_temp

            if LUT_temp.divisor == 1 :
                for i in range(0, len(tempLUT.quotient)):
                    tempTerm = tempLUT.quotient[i]

                    for c in tempTerm:
                        if c.isupper() or c.isdigit():
                            print(c, end="")
                        else:
                            print("~"+c.upper(), end="")
                    
                    if(i != len(tempLUT.quotient)-1):
                        print("+", end = "")
            else:                
                for j in range(0, len(LUT_temp.divisor)):
                    if j != 0:
                        print("+", end = "")
                    print("(" + LUT_temp.quotient[j]+")" , end="")
                    for c in LUT_temp.divisor[j]:
                        if(c.isupper() or c.isdigit()):
                            print(c, end="")
                        else:
                            print("~"+c.upper(), end="")
                    functionPrinted = 1
            
            

            if LUT_temp.remainder != 0:
                if(len(LUT_temp.remainder) != 0 ):
                    if(functionPrinted == 1):
                        print("+", end="")
                    # print("+".join(LUT_temp.remainder), end="")

                    for i in range(0, len(tempLUT.remainder)):
                        tempTerm = tempLUT.remainder[i]

                        for c in tempTerm:
                            if c.isupper() or c.isdigit():
                                print(c, end="")
                            else:
                                print("~"+c.upper(), end="")   
                        if(i != len(tempLUT.remainder)-1):
                            print("+", end = "")
                
            print("\n")

            # LUT dependencies
            print("Dependent on the following LUTs:")
            print(LUT_temp.LUTdependents)

            print("LUTS dependent on this LUT:")
            print(LUT_temp.dep2me)

            # Wire dependencies
            print("Dependent on the following wires:")
            tempSet = set()
            for t in LUT_temp.wireDependents:
                for c in t:
                    tempSet.add(c.upper())

            print(",".join(list(tempSet)))

            #Print function name
            print("Function Output: ", end="")

            if (key in val_list):
                ind = val_list.index(key)
                print(key_list[ind])              
            else:
                print("Intermediate output")

            print("\n\n")

        if(self.numLUT > self.numLUT_used):
                for i in range(self.numLUT_used, self.numLUT):
                    print("LUT "+str(i))
                    print("UNASSIGNED LUT")

 
