## GENE OVERLAP ANALYSIS
## CREATED: 11/24/2014. 
## PURPOSE: TO IDENTIFY SHARED GENES BETWEEN DIFFERENT SPECIES
## REFERENCE: HERE IS THE REFERENCE TO THE BIOPYTHON TUTORIAL IMPLEMENTED HERE: http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec95
## OUTPUT: EXCEL FILE WITH NUMBER OF GENES SHARED IN DIFFERENT COMBINATIONS OF ORGANISMS, AND THE LIST OF THESE GENES
## USER GUIDE: 
## 	-USER MUST PLACE THIS SCRIPT INSIDE THE FOLDER WITH BLASTP.EXE, MAKEBLASTDB.EXE ALONGSIDE WITH THE GENOMES HE/SHE WANTS TO ANALYSE
##  -USER MUST RUN THE SCRIPT WITH PROPER PARAMETERS FROM THE TERMINAL TO ANALYSE THE GENOMES
## ALGORITHM: 
## 	1. TRANSFORM THE NAMES OF FASTA FILES INTO THE FORM OF CONSECUTIVE NATURAL NUMBERS
##  2. MAKE A DICTIONARY WITH KEYS BEING THE ORGANISMS AND THE VALUES BEING ALL THE PEPTIDES CORRESPONDING TO THAT ORGANISM
##	3. MAKE A DATABASE OF ALL ORGANISMS IN THE FOLDER
##	4. BLAST EVERY PROTEOME AGAINST THE DATABSE AND MAP IT TO A DICTIONARY
## 	5. ADD THE REST OF THE PROTEINS TO THE MAP DICTIONARY 
##  6. CONVERT THE MAP DICTIONARY IN A GROUP OF SETS FOR EVERY ORGANISM
##	--7. FORM THE SUPERSET AND SUBTRACT IT FROM THE UNION
##	8. OUTPUT THE RESULT IN EITHER TXT OR EXCEL FORMAT

## MAKE SURE THERE IS NO SUCH EXCEPTION THAT WHEN ONE PROTEIN MATCHES THE OTHER AND THIS OTHER MATCHES THE THIRD ONE, THE FIRST ONE IS NOT MATCHING THE THIRD ONE
## MAKE MAPPING INDECES TO BE BASED ON THE NUMBER

import sys
from os import system
from os import listdir
from os.path import isfile, join

## 01. FUNCTIONS

## TO DO: Write test functions to check necessary files in the folder

## Ask user to provide genomes to build database
files = [ f for f in listdir('./') if isfile(join('./',f)) and '.fa' in f and 'database' not in f ]

def concatFile(genomeFlag):
	outputFile = open('database.fa', 'w')
	for num in genomeFlag:
		num = int(num)
		tempFile = open(files[num-1], 'r')
		for line in tempFile:
			outputFile.write(line)	
	outputFile.close()

def choseGenomes():
	print(str(files) + '\n')
	number = 1
	for organism in files:
		print(str(number) + ' ' + organism + '\n')
		number += 1
	genomeFlag = input("\n\nPlease Provide a Combination of Space Separated Numbers (eg. 1 2 3 4): ")
	genomeFlag = genomeFlag.split(' ')
	return genomeFlag

def makeDB():	system("makeblastdb.exe -in database.fa -out database -dbtype prot")

def runBLAST(genomeFlag):
	eval = input("Choose E-value: ")
	for num in genomeFlag:
		num = int(num)
		print("Running BLAST...")
		system("blastp.exe -query " + files[num-1] + " -out " + str(num) + " -db database -evalue " + str(eval) + " -outfmt 6")		

def mapping(genomeFlag):
	newId = {}
	counter = 0
	for num in genomeFlag:
		print('Number ' + num + ' is being processed...')
		inFile = open(num, 'r')
		for line in inFile:
			idPair = line.split("\t")
			newIdSize = len(newId)
			if newIdSize != 0:
				found = 0 ## variable that checks wether we found what we were looking for
				for i in range(newIdSize):
					if idPair[0] in newId[i] or idPair[1] in newId[i]:
						newId[i].add(idPair[0])
						newId[i].add(idPair[1])
						found = 1
						break
				if found == 0:
					newId[counter] = set([idPair[0],idPair[1]])
					counter+=1
				found = 0
			else:
				newId[counter] = set([idPair[0],idPair[1]])
				counter += 1
		inFile.close()
	return newId

def overlap(newId):
	overlap = {}
	for gene in newId:
		overlapSet = [] ## creating a sorted list for all organisms that overlap
		for oldId in newId[gene]:
			trilogon = oldId[0:3]
			if trilogon not in overlapSet:
				overlapSet.append(trilogon)
		overlapSet.sort()
		if str(overlapSet) not in overlap:
			overlap[str(overlapSet)] = 1
		else:
			overlap[str(overlapSet)] += 1
	return overlap

def output(result):
	outputFile = open('result.txt', 'w')
	for item in result:
		outputFile.write(str(item) + '\t' + str(len(item)) + '\t' + str(result[item]) + '\n')
	outputFile.close()
	print('Done')

def stage01():
	print("\n\nSTAGE 1: Making a Database...\n\n")
	genomeFlag = choseGenomes()
	concatFile(genomeFlag)
	makeDB()

def stage02():
	print("\n\nSTAGE 2: BLAST...\n\n")
	genomeFlag = choseGenomes()
	runBLAST(genomeFlag)

def stage03():
	print("\n\nSTAGE 3: Mapping...\n\n")
	genomeFlag = choseGenomes()
	newId = mapping(genomeFlag)
	result = overlap(newId)
	output(result)

## 02. MAIN

def main(): 
	choice = int(input("INPUT\n\n\t1, If you want to run from beginning\n\n\t2, if you want to run BLAST w/o making a database\n\n\t3, if you want to find the intersection of BLASTed results\n\n"))
	if choice == 1:
		stage01()
		stage02()
		stage03()
	if choice == 2:
		stage02()
		stage03()
	if choice == 3:
		stage03()

main()
