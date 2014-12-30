######################################################################
## FILE: 		UNIPROT.VER3.PY                                     ##
## DESCRIPTION:	THIS FILE GENERATES AN EXCEL FILE CONTAINING GO     ##
## PFAM, AND INTERPRO TERMS FROM UNIPROT FOR UNIQUE GENE FILES      ##
######################################################################

import sys
import urllib.request
import xlsxwriter
import collections
from os import makedirs
from os import system
from os import listdir
from os.path import isfile, join, exists

url = 'http://www.uniprot.org/uniprot/?query=CAC30414&format=tab&columns=go'
referenceName = sys.argv[1]
workBook = referenceName[0:-4]+'.xlsx'

if len(sys.argv) < 1:
	print('\nUsage: python uniprot.ver4.py -gene_list_file \n')
	sys.exit()
	
def getUniprotText(url): ## returns a text
	result = []
	request = urllib.request.Request(url)
	contact = "kino6052@colorado.edu" # Please set your email address here to help us debug in case of problems.
	request.add_header('Kirill Novik', 'Python %s' % contact)
	response = urllib.request.urlopen(request)
	info = response.read(2000)
	info = info.decode("utf-8")
	return info;
# returns text

#returns array of GO terms, unorganized
def goCollecter(url): #?query=[geneID]&format=tab&columns=go
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)
	i = response.read(1000)
	i = i.decode("utf-8")
	i = i[i.find("\n")+1:].split(';')
	return i;

#returns protein name and ORFname	
def nameCollector(url): #?query=[geneID]&format=tab
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)
	i = response.read(1000)
	i = i.decode("utf-8")
	i = i[i.find('\n'):].split('\t')[3:5]
	return i;
	
#returns interpro and pfam data
def domainCollector(url): #?query=[geneID]&format=txt
	interPro = []
	pFam = []
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)
	i = response.read(3000)
	i = i.decode("utf-8")
	numInterpro = i.count('InterPro;')
	a = 0
	for a in range(numInterpro):
		start = i.replace('InterPro;','XX',a).find('InterPro;')
		interPro.append(i[start:].split(';')[2].split('\n')[0])
		a += 1
	numPfam = i.count('Pfam')
	b = 0
	for b in range(numPfam):
		start = i.replace('Pfam','XX',b).find('Pfam')
		pFam.append(i[start:].split(';')[2].split('\n')[0])
		b += 1
	domTuple = collections.namedtuple('Domain', ['i','p'])
	info = domTuple(interPro, pFam)
	return info
	
def openReference(fname): # opens a file with gene names we want to put into UniProt
	result = []
	file = open(fname, 'r')
	for line in file:
		result.append(line)
	file.close()
	return result
## returns a list of genes

def createWorkbook(fname, reference):
	## Creating an text file
	workbook = xlsxwriter.Workbook(fname)
	worksheet = workbook.add_worksheet()
	referenceList = openReference(reference)
	counter = 0;
	for gene in referenceList:
		worksheet.write(counter, 0, gene.split()[0]) # first is row, then , then value
		names = nameCollector('http://www.uniprot.org/uniprot/?query=' + str(gene.split()[0]) + '&format=tab')
		worksheet.write(counter, 1, names[0])
		worksheet.write(counter, 2, names[1])
		domains = domainCollector('http://www.uniprot.org/uniprot/?query=' + str(gene.split()[0]) + '&format=txt')
		worksheet.write(counter, 3, str(domains.i))
		worksheet.write(counter, 4, str(domains.p))
		goTerms = goCollecter('http://www.uniprot.org/uniprot/?query=' + str(gene.split()[0]) + '&format=tab&columns=go')
		c = 0
		while c < len(goTerms):
			worksheet.write(counter, 5+c, goTerms[c])
			c += 1
		counter += 1;
		print(str(gene) + ': %' + str(100*counter/len(referenceList)))
	workbook.close()
## void

createWorkbook(workBook, referenceName) 
