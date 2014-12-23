import xlsxwriter

import sys
import urllib.request
from os import makedirs
from os import system
from os import listdir
from os.path import isfile, join, exists

if len(sys.argv) < 3:
	print('\nUsage: python uniprot.py -fileIn -fileOut\n')
	sys.exit()

def printFolder():
	files = [ f for f in listdir('./') if isfile(join('./',f))]
	print('\nFolder Contains: \n')
	for item in files:
		print(item)
	pause = input('Press any key...')

sheetName = str(sys.argv[2]) + '.xlsx'
referenceName = str(sys.argv[1])

def getGeneOntologyFromUniprot(url): # returns a string with gene ontologies for a given url (which has a gene name in the query)
	result = []
	request = urllib.request.Request(url)#, data)
	contact = "kino6052@colorado.edu" # Please set your email address here to help us debug in case of problems.
	request.add_header('Kirill Novik', 'Python %s' % contact)
	response = urllib.request.urlopen(request)
	info = response.read(2000)
	info = info.decode("utf-8")
	info = info.split('\n')[1]
	#info = info.split()[0]
	return info;

# returns a list of gene ontology terms

def openReference(fname): # opens a file with gene names we want to put into UniProt
	result = []
	file = open(fname, 'r')
	for line in file:
		result.append(line)
	file.close()
	return result
# returns a list of genes

## Function that generates a list of filenames we want to work with

def fileList(list):
	f = []
	for (dirpath, dirnames, filenames) in walk("."):
		f.extend(filenames)
		break
	for item in f:
		if item.find(".txt") != -1:
			list.append(item[:-4])

def goCollector(doc):
	file = open(doc, "r")
	goList = []
	for line in file:
		if line.find("GO;") != -1:
			goList.append(line.split()[3:])
	file.close()
	return goList

def writeExcelFile(worksheet, rowNum, column_1, column_2):
	worksheet.write(rowNum, 0, column_1) # first is row, then , then value
	worksheet.write(rowNum, 1, column_2) # first is row, then , then value

def main(fname):
	## Creating an XLSX file
	workbook = xlsxwriter.Workbook(fname)
	worksheet = workbook.add_worksheet()

	genes = []
	fileList(genes)
	print(genes)
	counter = 0;
	for gene in genes:
		goList = []
		goString = ""
		goList = goCollector(gene + ".txt")
		for item in goList:
			item = " ".join(item)
			goString += item;
		writeExcelFile(worksheet, counter, gene, str(goString))
		counter += 1
	print()

def createExcelFile(fname, reference):
	## Creating the Result Folder
	if not exists('result'):
		makedirs('result')
	## Creating an XLSX file
	workbook = xlsxwriter.Workbook('./result/' + fname)
	worksheet = workbook.add_worksheet()
	referenceList = openReference(reference)
	counter = 0;
	for gene in referenceList:
		worksheet.write(counter, 0, gene.split()[0]) # first is row, then , then value
		geneOntology = getGeneOntologyFromUniprot('http://www.uniprot.org/uniprot/?query=' + str(gene.split()[0]) + '&format=tab&column=id')
		worksheet.write(counter, 1, geneOntology.split()[0]) # first is row, then , then value
		worksheet.write(counter, 2, geneOntology.split()[1]) # first is row, then , then value
		worksheet.write(counter, 3, geneOntology.split()[2])
		worksheet.write(counter, 4, geneOntology.split()[3])
		worksheet.write(counter, 5, geneOntology.split()[4])
		counter += 1
		print('\n' + str(gene) + ': %' + str(100*counter/len(referenceList)) + '\n')
		print(geneOntology + '\n')
	workbook.close()
# void

printFolder()
createExcelFile(sheetName, referenceName)
