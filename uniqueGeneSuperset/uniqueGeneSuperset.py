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

## TO DO:
## - FUNCTION THAT READS INPUT AND MAKES A LIST OF GENOME FILES
def input(): # (M) return list of genome files
## - FUNCTION THAT CREATES A SUPERSET FROM THE ELEMENTS IN A LIST
def superset(): # (M) return a list with all possible subsets
## - FUNCTION THAT CREATES A DICTIONARY WITH gene SETS (VALUE) FOR EVERY SET IN A SUPERSET (KEY)
def supersetDict(): # (M) return a dictionary with gene sets for every organism set in a superset
## - FUNCTION THAT CREATES A REFERENCE SET
def referenceSet(): # (M) return a set of M. vaccae genes 
## - FUNCTION THAT OUPUTS THE AMOUNT OF UNIQUE GENES
def uniqueGeneNumber(): # (M) return the number of genes
## - FUNCTION THAT CREATES THE OUTPUT FILE
def output(): # (M) void
## - ERROR HANDLING