## UNIQUE GENE SUPERSET MAKER
##
## CREATED: 01/09/2015. 
## PURPOSE: TO MAKE A FILE CONTAINING A TABLE WITH NUMBERS CORRESPONDING 
## TO THE NUMBER OF GENES CONTAINED IN M. VACCAE BUT NOT IN THE ORGANISMS 
## (IN EVERY POSSIBLE COMBINATION) IT IS COMPARED AGAINST.
## (I.E. [ORGANISMS AGAINST M. VACCAE]           [# GENES]
##       ('2', '3', '9', '10', '16', '17', '19') 285
##       ('2', '3', '9', '10', '16', '18', '19') 280
##
## REFERENCE: http://rosettacode.org/wiki/Power_set#Python
##
## OUTPUT: TXT FILE
##
## USER GUIDE: 
## 
## ALGORITHM: 
##

from itertools import chain, combinations

## TO DO:
## - FUNCTION THAT READS INPUT AND MAKES A LIST OF GENOME FILES
def input(fileLoc): # (M) return list of genome files
    file = open(fileLoc, 'r')
    return file
## - FUNCTION THAT CREATES A SUPERSET FROM THE ELEMENTS IN A LIST
def superset(list): # (M) return a list with all possible subsets
    return chain.from_iterable(combinations(list,r)\
                                for r in range(len(list)+1))
## - FUNCTION THAT CREATES A DICTIONARY WITH gene SETS (VALUE) FOR EVERY SET IN A SUPERSET (KEY)
def geneSet(organism):
    geneSet = set([])
    for line in input('./input/genomes/' + str(organism)):
        line = line.split()
        if 'EJZ' in line[0]:
            geneSet.add(line[0])
        if 'EJZ' in line[1]:
            geneSet.add(line[1])
    return geneSet
            

def supersetDict(superset, dictionary): # (M) return a dictionary with gene sets for every organism set in a superset
    supersetDict = {}
    for s in superset:
        supersetDict[s] = set([])
        for element in s:
            supersetDict[s] = supersetDict[s].union(dictionary[element])
    return supersetDict
## - FUNCTION THAT CREATES A REFERENCE SET
def referenceSet(fileLoc): # (M) return a set of M. vaccae genes 
    referenceSet = set([])
    for line in input(fileLoc):
        if 'EJZ' in line:
            referenceSet.add(line[1:9])
    return referenceSet
## - FUNCTION THAT OUPUTS THE AMOUNT OF UNIQUE GENES
def uniqueGeneNumber(supersetDict, referenceSet): # (M) return the number of genes
    resultDict = {}
    for set in supersetDict:
        diffSet = referenceSet - supersetDict[set]
        resultDict[set] = len(diffSet)
    return resultDict
## - FUNCTION THAT CREATES THE OUTPUT FILE
def output(fileLoc): # (M) void
    file = open(fileLoc, 'w')
    return file
## - ERROR HANDLING

def main():
    testList = [1, 2, 3, 4, 5, 6, 7, 9]
    supSet = superset(testList)
    refSet = referenceSet('./input/mvaccae.fa')
    genomeDict = {}
    for i in testList:
        genomeDict[i] = geneSet(i)
    ssDict = supersetDict(supSet, genomeDict)
    gNum = uniqueGeneNumber(ssDict, refSet)
    result = output('./output/uniqueGeneSuperset.txt')
    for i in gNum:
        result.write(str(i) + '\t' + str(gNum[i]) + '\n')
    result.close()
    
main()