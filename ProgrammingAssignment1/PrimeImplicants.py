import pdb
import os

def row_to_term(row):
    """Convert a binary string to a term for SOP."""
    return ''.join([f'{var}' if val == '1' else f'~{var}' if val == '0' else '' for var, val in zip('ABCD', row)])

def row_to_pos_term(row):
    """Convert a binary string to a term for canonical POS."""
    return ''.join([f'~{var}' if val == '1' else f'{var}' if val == '0' else '' for var, val in zip('ABCD', row)])

def count_literals(term):
    """Count the number of literals in a term."""
    return term.count('A') + term.count('B') + term.count('C') + term.count('D')

def dec_to_bin(dec_num, num_vars):
    """Convert a decimal number to a binary string of length num_vars."""
    return format(dec_num, f'0{num_vars}b')


def generate_all_binary_combinations(num_vars):
    """Generate all possible binary combinations of given length."""
    return [dec_to_bin(i, num_vars) for i in range(2**num_vars)]

def get_inverse_sop_terms(binary_combinations, num_vars):
    """Get the iSOP terms."""
    all_combinations = set(generate_all_binary_combinations(num_vars))
    original_set = set(binary_combinations)
    inverse_set = all_combinations - original_set
    return [row_to_term(row) for row in inverse_set]

def get_inverse_pos_terms(binary_combinations):
    """Get the iPOS terms."""
    return [row_to_pos_term(row) for row in binary_combinations]

def bit_diff_count(a, b):
    """Count the number of differing bits between two binary strings."""
    return sum([av != bv for av, bv in zip(a, b)])
    
def covers(minterm, prime_implicant):
    """Check if the prime implicant covers the minterm."""
    return all([(a == '-' or a == b) for a, b in zip(prime_implicant, minterm)])

def covers2(minterm, prime_implicant):
    numberX_min = minterm.count('-')
    numberX_PI = prime_implicant.count('-')
    minimumX = min([numberX_min, numberX_PI])
    checkSum = 0
    for i in range(0, len(minterm)):
        if(minterm[i] == '-' and prime_implicant[i] == '-'):
            checkSum = checkSum + 1
        if((minterm[i] != '-' and prime_implicant[i] != '-' and minterm[i] != prime_implicant[i]) or (prime_implicant[i] == 'x' or minterm[i] == 'x')):
            return False
    if(checkSum == minimumX):
        return True
    else: 
        return False
def removeRepeated(all_prime_implicants):
    """Remove repeated prime implicants"""
    all_prime_implicants = list(all_prime_implicants)
    new_prime_implicants = list(all_prime_implicants)
    for index1 in range(0,len(all_prime_implicants)):
        for index2 in range(index1+1, len(all_prime_implicants)):
            if(covers2(all_prime_implicants[index1], all_prime_implicants[index2])):
                if(all_prime_implicants[index1].count('-') >all_prime_implicants[index2].count('-')):
                    added = all_prime_implicants[index1]
                    added2 = ""
                    removed = all_prime_implicants[index2]
                    all_prime_implicants[index2] = 'x'
    
                elif(all_prime_implicants[index1].count('-')<all_prime_implicants[index2].count('-')):
                    added = all_prime_implicants[index2]
                    added2 = ""
                    removed = all_prime_implicants[index1]
                    all_prime_implicants[index1] = 'x'
                else:
                    added = all_prime_implicants[index2]
                    added2 = all_prime_implicants[index1]
                    removed = ""
                    
                if(added not in new_prime_implicants):
                    new_prime_implicants.append(added)
                if(added2 !="" and added2 not in new_prime_implicants):
                    new_prime_implicants.append(added2)
                if (removed in new_prime_implicants):
                    new_prime_implicants.remove(removed)
            
                
                
    return set(new_prime_implicants)
    
def find_all_prime_implicants(binary_combinations):
    prime_implicants = set(binary_combinations)
    all_prime_implicants = set()

    while True:
        groups = {}
        for term in prime_implicants:
            num_ones = term.count('1')
            if num_ones not in groups:
                groups[num_ones] = [term]
            else:
                groups[num_ones].append(term)

        new_prime_implicants = set()
        combined_terms = set()

        keys = sorted(groups.keys())
        for i in range(len(keys) - 1):
            for term1 in groups[keys[i]]:
                for term2 in groups[keys[i + 1]]:
                    diff_count = bit_diff_count(term1, term2)
                    if diff_count == 1:
                        combined_term = ''.join(['-' if a != b else a for a, b in zip(term1, term2)])
                        new_prime_implicants.add(combined_term)
                        combined_terms.add(term1)
                        combined_terms.add(term2)

        all_prime_implicants.update(prime_implicants)
        prime_implicants = new_prime_implicants
        
        if not new_prime_implicants:
            break
           
    all_prime_implicants2 = removeRepeated(all_prime_implicants)
   
    return all_prime_implicants2

def simplify_prime_implicants(prime_implicants):
    changes = True
    prev_implicants = prime_implicants.copy()

    while changes:
        changes = False
        new_implicants = set()
        marked = set()

        for pi1 in prev_implicants:
            for pi2 in prev_implicants:
                if pi1 != pi2 and bit_diff_count(pi1, pi2) == 1:
                    changes = True
                    new_pi = ''.join(['-' if a != b else a for a, b in zip(pi1, pi2)])
                    new_implicants.add(new_pi)
                    marked.add(pi1)
                    marked.add(pi2)

        for pi in prev_implicants:
            if pi not in marked:
                new_implicants.add(pi)

        prev_implicants = new_implicants

    return prev_implicants
    
def removeEssential(prime_implicant, essential_prime_implicants):
    PI_non = set()
    
    for term in prime_implicant:
        if term not in essential_prime_implicants:
            PI_non.add(term)
    
    return PI_non
    
def findBinaryCovered(simplified, binary_combinations):
    arr = [0] * len(binary_combinations)
    listSimp = list(simplified)
    listBinary = list(binary_combinations)
    
    for i in range(0,len(binary_combinations)):
        for PI in listSimp:
            if covers2(binary_combinations[i], PI):
                arr[i] = 1
                break;
                
    return arr           
            
            
def findPI_non(binaryComb, PI_non):
   
    PI_nonList = list(PI_non)
    works =[0]*len(PI_nonList)
    binaryComb = list(binaryComb)
    for i in range(0, len(PI_nonList)):
        if covers2(binaryComb, PI_nonList[i]):
            works[i] = 1
     
    maxCountDashes = -1    
    for i in range(0, len(PI_nonList)):
        if(works[i] == 1):
            numDashes = PI_nonList[i].count('-')
            if numDashes > maxCountDashes:
                maxCountDashes = numDashes
                idealPI = PI_nonList[i]
                
                
    return idealPI
                
    
def simplify_prime_implicants2(prime_implicant, essential_prime_implicants, binary_combinations):
    simplified = set(essential_prime_implicants)
    PI_non = removeEssential(prime_implicant, essential_prime_implicants)
    
    #find all the binary combinations that are covered by the essential
    coveredArr = findBinaryCovered(simplified, binary_combinations)
 
    done = False
    while not done:
        if 0 in coveredArr:
            index0 = coveredArr.index(0)
            # newPI = findPI_non(binary_combinations[index0], PI_non)
            print(index0)
            print(PI_non)
            print(simplified)
            print(binary_combinations)
            print(coveredArr)
            input("pause")
            simplified.add(newPI)
            #find all the binary combinations that are covered by the essential
            coveredArr = findBinaryCovered(simplified, binary_combinations)
        else:
            done = True
    
    return simplified
    


def get_minimal_cover(binary_combinations, prime_implicants):
    """Get the minimal cover for the given minterms and prime implicants."""
    coverage = {minterm: [] for minterm in binary_combinations}

    for pi in prime_implicants:
        for minterm in binary_combinations:
            if covers(minterm, pi):
                coverage[minterm].append(pi)

    minimal_cover = []
    while coverage:
        pi_cover_count = {pi: sum([pi in coverage[minterm] for minterm in coverage]) for pi in prime_implicants}
        max_cover_pi = max(pi_cover_count, key=pi_cover_count.get)
        minimal_cover.append(max_cover_pi)
        to_delete = []
        for minterm in coverage:
            if covers(minterm, max_cover_pi):
                to_delete.append(minterm)
        for m in to_delete:
            del coverage[m]

    return minimal_cover
def get_essential_prime_implicants(binary_combinations, prime_implicants):
    """Get the essential prime implicants from the given set of prime implicants."""
    
    # different method
    essenPI = list();

    for minTerm in binary_combinations:
        checkSum = 0
        for PI in prime_implicants:
            covered = covers(minTerm, PI)
            checkSum = checkSum + int(covered)                           
            if(checkSum>1):
                break
            if(covered):
                tempPI = PI       
    
        if(checkSum == 1 and tempPI not in essenPI):
            essenPI.append(tempPI)

    return set(essenPI)

def numOnsetMinMax(binaryComb, numInputs):
    onsetMin = len(binaryComb)
    onsetMax = (2**(numInputs)) - onsetMin
    
    return onsetMin, onsetMax



def findMinMaxTerms(binary_combinations, numInputs):
    n = numInputs - 1
    arrMin = [-1] * len(binary_combinations)
    arrMax = []
    
    for i in range(0,len(binary_combinations)):
        counter = n
        sum = 0
        it = 0
        binary = binary_combinations[i]
        while(counter >= 0):
            sum = sum + (int(binary[it])*(2**counter))
            counter = counter - 1
            it = it + 1
            
        arrMin[i] = sum
    
    allPoss = [*range(0, (2**(n+1)), 1)]
    
    for i in allPoss:
        if i not in arrMin:
            arrMax.append(i)

    return arrMin, arrMax        



def truth_table_to_canonical():
    num_vars = int(input("Enter number of variables (max 4 for this example): "))
    if num_vars > 4:
        print("Supports up to 4 variables only.")
        return
    elif num_vars == 0:
        print("Number of variables cannot be zero.")
        return
        

    # SOP Calculation
    print(f"Enter decimal numbers (space seperated) that represent combinations of {'ABCD'[:num_vars]} resulting in an output of 1:")
    decimal_numbers = list(map(int, input().split(' ')))
    # decimal_numbers = [1,  6, 7, 11, 12, 13, 15]
    
    binary_combinations = [dec_to_bin(dec, num_vars) for dec in decimal_numbers]
    
   
    
    all_prime_implicants = find_all_prime_implicants(binary_combinations)
    essential_prime_implicants = get_essential_prime_implicants(binary_combinations, all_prime_implicants)
    simplified_prime_implicants= simplify_prime_implicants2(all_prime_implicants, essential_prime_implicants, binary_combinations)
    # simplified_prime_implicants = simplify_prime_implicants(all_prime_implicants)

    sop_terms = [row_to_term(row) for row in binary_combinations]
    canonical_sop = ' | '.join(sop_terms)

    prime_implicants_terms = [row_to_term(row) for row in all_prime_implicants]
    prime_implicants_sop = ' , '.join(prime_implicants_terms)

    simplified_terms = [row_to_term(row) for row in simplified_prime_implicants]
    simplified_sop = ' | '.join(simplified_terms)

    isop_terms = get_inverse_sop_terms(binary_combinations, num_vars)
    canonical_isop = ' | '.join(isop_terms)

    
    # iPOS Calculation based on 1-output terms
    ipos_terms = get_inverse_pos_terms(binary_combinations)
    canonical_ipos = ' & '.join(ipos_terms)


    num_literals_original = sum([count_literals(term) for term in sop_terms])
    num_literals_simplified = sum([count_literals(term) for term in simplified_terms])
 
    
    minimal_prime_implicants = get_minimal_cover(binary_combinations, all_prime_implicants)
    minimal_terms = [row_to_term(row) for row in minimal_prime_implicants]
    minimal_sop = ' | '.join(minimal_terms)
    num_literals_minimal = sum([count_literals(term) for term in minimal_terms])
    # all_prime_implicants = find_all_prime_implicants(binary_combinations)
    
    # simplified_prime_implicants= simplify_prime_implicants2(all_prime_implicants, essential_prime_implicants, binary_combinations)
    
    simplified_prime_implicants = simplify_prime_implicants(all_prime_implicants)
    essential_terms = [row_to_term(row) for row in essential_prime_implicants]
    essential_sop = ' , '.join(essential_terms)
     
    onsetMin, onsetMax = numOnsetMinMax(binary_combinations, num_vars)
    
    arrMin, arrMax = findMinMaxTerms(binary_combinations, num_vars)
    
    
    ## finding minimal POS
    binaryComb_max = [dec_to_bin(dec, num_vars) for dec in arrMax]
    all_prime_implicants_MAX = find_all_prime_implicants(binaryComb_max)
    essential_prime_implicants_MAX = get_essential_prime_implicants(binaryComb_max, all_prime_implicants_MAX)
    simplified_prime_implicants_MAX = simplify_prime_implicants2(all_prime_implicants_MAX, essential_prime_implicants_MAX, binaryComb_max)
    pos_terms = [row_to_pos_term(row) for row in simplified_prime_implicants_MAX]
    minimal_pos = ' & '.join(pos_terms)
    
    pos_terms = [row_to_pos_term(row) for row in binaryComb_max]
    canonical_pos = ' & '.join(pos_terms)
     
    print(f"\nCanonical SOP: {canonical_sop}")
    print(f"\nInverse SOP (iSOP): {canonical_isop}")
    print(f"\nCanonical POS: {canonical_pos}")
    print(f"\nInverse POS (iPOS): {canonical_ipos}")
    print(f"Prime Implicants: {prime_implicants_sop}")
    print(f"\nEssential Prime Implicants: {essential_sop}")
    
    print(f"Simplified SOP: {simplified_sop}")
    print(f"Number of saved literals (Prime Implicants): {num_literals_original - num_literals_simplified}")
    print(f"\nMinimal SOP: {minimal_sop}")
    print(f"\nMinimal POS: {minimal_pos}")
    print(f"Number of saved literals (Minimal): {num_literals_original - num_literals_minimal}")
    print(f"Number of onset minterms: {onsetMin}")
    print(f"Number of onset maxterms: {onsetMax}")
    print(f"Following are the minterms:\n {arrMin}")
    print(f"Following are the maxterms:\n {arrMax}")
    
    
def readFile():
    print("Here are the files in this directory, choose the right one!\n")
    i = 1
    dir = []
    for dirnames in os.listdir():
        print(str(i)+") "+ dirnames+"\n")
        dir.append(dirnames)
        i = i+1
    
    fileNum = int(input("Which file do you want to open? "))
    
    if(fileNum<1 or fileNum >= i):
        print("Invalid choice\n")
        exit()
    
    f = open(dir[fileNum-1], "r")
    Lines = f.readlines()
    
    count = 0
    
    binary_combinations = []
    numInputs = -1
    
    # only looks at one output logic with at most 4 inputs
    for line in Lines:
        count += 1
        if(line[0] == "0" or line[0] == "1"):
            index0 = line.index(" ")
            if line[index0+1]== "1":
                strBin = line[0:index0]
                binary_combinations.append(strBin)
        elif(line[0:3] == ".i "):
            numInputs = int(line[3])
           
    
   
    all_prime_implicants = find_all_prime_implicants(binary_combinations)
    essential_prime_implicants = get_essential_prime_implicants(binary_combinations, all_prime_implicants)
    simplified_prime_implicants= simplify_prime_implicants2(all_prime_implicants, essential_prime_implicants, binary_combinations)
    # simplified_prime_implicants = simplify_prime_implicants(all_prime_implicants)

    sop_terms = [row_to_term(row) for row in binary_combinations]
    canonical_sop = ' | '.join(sop_terms)

    prime_implicants_terms = [row_to_term(row) for row in all_prime_implicants]
    prime_implicants_sop = ' , '.join(prime_implicants_terms)

    simplified_terms = [row_to_term(row) for row in simplified_prime_implicants]
    simplified_sop = ' | '.join(simplified_terms)

    isop_terms = get_inverse_sop_terms(binary_combinations, numInputs)
    canonical_isop = ' | '.join(isop_terms)

    
    # iPOS Calculation based on 1-output terms
    ipos_terms = get_inverse_pos_terms(binary_combinations)
    canonical_ipos = ' & '.join(ipos_terms)


    num_literals_original = sum([count_literals(term) for term in sop_terms])
    num_literals_simplified = sum([count_literals(term) for term in simplified_terms])
    
    
    minimal_prime_implicants = get_minimal_cover(binary_combinations, all_prime_implicants)
    minimal_terms = [row_to_term(row) for row in minimal_prime_implicants]
    minimal_sop = ' | '.join(minimal_terms)
    num_literals_minimal = sum([count_literals(term) for term in minimal_terms])
    
    simplified_prime_implicants = simplify_prime_implicants(all_prime_implicants)
    essential_terms = [row_to_term(row) for row in essential_prime_implicants]
    essential_sop = ' , '.join(essential_terms)
    
    onsetMin, onsetMax = numOnsetMinMax(binary_combinations, numInputs)
    arrMin , arrMax = findMinMaxTerms(binary_combinations, numInputs)
    
    
    
    ## finding minimal POS
    binaryComb_max = [dec_to_bin(dec, numInputs) for dec in arrMax]
    all_prime_implicants_MAX = find_all_prime_implicants(binaryComb_max)
    essential_prime_implicants_MAX = get_essential_prime_implicants(binaryComb_max, all_prime_implicants_MAX)
    simplified_prime_implicants_MAX = simplify_prime_implicants2(all_prime_implicants_MAX, essential_prime_implicants_MAX, binaryComb_max)
    pos_terms = [row_to_pos_term(row) for row in simplified_prime_implicants_MAX]
    minimal_pos = ' & '.join(pos_terms)
    
    pos_terms = [row_to_pos_term(row) for row in binaryComb_max]
    canonical_pos = ' & '.join(pos_terms)
    
    
        
    print(f"\nCanonical SOP: {canonical_sop}")
    print(f"\nInverse SOP (iSOP): {canonical_isop}")
    print(f"\nCanonical POS: {canonical_pos}")
    print(f"\nInverse POS (iPOS): {canonical_ipos}")
    print(f"Prime Implicants: {prime_implicants_sop}")
    print(f"\nEssential Prime Implicants: {essential_sop}")
    
    print(f"Simplified SOP: {simplified_sop}")
    print(f"Number of saved literals (Prime Implicants): {num_literals_original - num_literals_simplified}")
    print(f"\nMinimal SOP: {minimal_sop}")
    print(f"Number of saved literals (Minimal): {num_literals_original - num_literals_minimal}")
    print(f"\nMinimal POS: {minimal_pos}")
    print(f"Number of onset minterms: {onsetMin}")
    print(f"Number of onset maxterms: {onsetMax}")
    print(f"Following are the minterms:\n {arrMin}")
    print(f"Following are the maxterms:\n {arrMax}")
    
    
    
def readFunction():
    num_vars = int(input("Enter number of variables (max 4 for this example): "))
    if num_vars > 4:
        print("Supports up to 4 variables only.")
        return
    elif num_vars == 0:
        print("Number of variables cannot be zero.")
        return
        
    function = input("Enter logic with A being the MSb, and D being the LSb and Y as the output\n")
    
  
    
    terms = function.split("+")
    binaryComb = []
    vecTemp = ["A", "B", "C", "D"]
    
    
    for i in range(0,len(terms)):
        stringBin = list("----")
        stringFocus = terms[i]
        neg = False
        for j in range(0,len(stringFocus)):
            if(stringFocus[j] == "a" or stringFocus[j] == "A"):
                if(neg):
                    stringBin[0] = '0'
                    neg = False
                else:
                    stringBin[0] = '1'
            elif(stringFocus[j] == "b" or stringFocus[j] == "B"):
                if(neg):
                    stringBin[1] = '0'
                    neg = False
                else:
                    stringBin[1] = '1'
            elif(stringFocus[j] == "c" or stringFocus[j] == "C"):
                if(neg):
                    stringBin[2] = '0'
                    neg = False
                else:
                    stringBin[2] = '1'
                    
            elif(stringFocus[j] == "d" or stringFocus[j] == "D"):
                if(neg):
                    stringBin[3] = '0'
                    neg = False
                else:
                    stringBin[3] = '1'
            elif (stringFocus[j] =="~"):
                neg = True
                
                
        stringBin = stringBin[0:num_vars]        
        numofDashes = stringBin.count("-")
        stringBinOriginal = stringBin[0:num_vars]
        
        if(numofDashes == 0):
            string2add = "".join(stringBin)
            binaryComb.append(string2add)
        else:
            totalPoss = 2**(numofDashes)
            
            
            for i in range(0,totalPoss):
                counter = 0
                stringBinTemp= stringBinOriginal[0:num_vars]
                for j in range(0,numofDashes):
                    index1 = stringBinTemp.index("-")
                    temp = format(i, '#06b')
                    stringBinTemp[index1] = temp[6-numofDashes+j]
                
                string2add = "".join(stringBinTemp)
                binaryComb.append(string2add)   
        
    binaryComb = list(removeRepeated(binaryComb))
        
    binary_combinations   = binaryComb;
    
    all_prime_implicants = find_all_prime_implicants(binary_combinations)
    essential_prime_implicants = get_essential_prime_implicants(binary_combinations, all_prime_implicants)
    simplified_prime_implicants= simplify_prime_implicants2(all_prime_implicants, essential_prime_implicants, binary_combinations)

    sop_terms = [row_to_term(row) for row in binary_combinations]
    canonical_sop = ' | '.join(sop_terms)

    prime_implicants_terms = [row_to_term(row) for row in all_prime_implicants]
    prime_implicants_sop = ' , '.join(prime_implicants_terms)

    simplified_terms = [row_to_term(row) for row in simplified_prime_implicants]
    simplified_sop = ' | '.join(simplified_terms)

    isop_terms = get_inverse_sop_terms(binary_combinations, num_vars)
    canonical_isop = ' | '.join(isop_terms)

    
    # iPOS Calculation based on 1-output terms
    ipos_terms = get_inverse_pos_terms(binary_combinations)
    canonical_ipos = ' & '.join(ipos_terms)


    num_literals_original = sum([count_literals(term) for term in sop_terms])
    num_literals_simplified = sum([count_literals(term) for term in simplified_terms])
    
    
    minimal_prime_implicants = get_minimal_cover(binary_combinations, all_prime_implicants)
    minimal_terms = [row_to_term(row) for row in minimal_prime_implicants]
    minimal_sop = ' | '.join(minimal_terms)
    num_literals_minimal = sum([count_literals(term) for term in minimal_terms])
    
    simplified_prime_implicants = simplify_prime_implicants(all_prime_implicants)
    essential_terms = [row_to_term(row) for row in essential_prime_implicants]
    essential_sop = ' , '.join(essential_terms)
    
    onsetMin, onsetMax = numOnsetMinMax(binary_combinations, num_vars)
    arrMin , arrMax = findMinMaxTerms(binary_combinations, num_vars)
    
    
    
    ## finding minimal POS
    binaryComb_max = [dec_to_bin(dec, num_vars) for dec in arrMax]
    all_prime_implicants_MAX = find_all_prime_implicants(binaryComb_max)
    essential_prime_implicants_MAX = get_essential_prime_implicants(binaryComb_max, all_prime_implicants_MAX)
    simplified_prime_implicants_MAX = simplify_prime_implicants2(all_prime_implicants_MAX, essential_prime_implicants_MAX, binaryComb_max)
    pos_terms = [row_to_pos_term(row) for row in simplified_prime_implicants_MAX]
    minimal_pos = ' & '.join(pos_terms)
    
    pos_terms = [row_to_pos_term(row) for row in binaryComb_max]
    canonical_pos = ' & '.join(pos_terms)
    
    
        
    print(f"\nCanonical SOP: {canonical_sop}")
    print(f"\nInverse SOP (iSOP): {canonical_isop}")
    print(f"\nCanonical POS: {canonical_pos}")
    print(f"\nInverse POS (iPOS): {canonical_ipos}")
    print(f"Prime Implicants: {prime_implicants_sop}")
    print(f"\nEssential Prime Implicants: {essential_sop}")
    
    print(f"Simplified SOP: {simplified_sop}")
    print(f"Number of saved literals (Prime Implicants): {num_literals_original - num_literals_simplified}")
    print(f"\nMinimal SOP: {minimal_sop}")
    print(f"Number of saved literals (Minimal): {num_literals_original - num_literals_minimal}")
    print(f"\nMinimal POS: {minimal_pos}")
    print(f"Number of onset minterms: {onsetMin}")
    print(f"Number of onset maxterms: {onsetMax}")
    print(f"Following are the minterms:\n {arrMin}")
    print(f"Following are the maxterms:\n {arrMax}")
        
        
   
            
                
       
    
    

if __name__ == "__main__":

    choice = int(input("Command line input minterms(1) or PLA File(2) or input function(3)\n"))
    
    if choice == 1:
        truth_table_to_canonical()
    elif choice == 2:
        readFile()
    elif choice == 3:
        readFunction()
    else:
        print("Invalid input\n")
  

