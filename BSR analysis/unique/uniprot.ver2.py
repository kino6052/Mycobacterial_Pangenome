import urllib.request
import xlsxwriter

url = 'http://www.uniprot.org/blast/?query=KOUTG6'
sheetName = 'uniqueGeneAccessions.xlsx'
referenceName = '162UniqueGenes.txt'

def getGeneOntologyFromUniprot(url): # returns a string with gene ontologies for a given url (which has a gene name in the query)
	result = []
	request = urllib.request.Request(url)#, data)
	contact = "kino6052@colorado.edu" # Please set your email address here to help us debug in case of problems.
	request.add_header('Kirill Novik', 'Python %s' % contact)
	response = urllib.request.urlopen(request)
	info = response.read(2000)
	info = info.decode("utf-8")
	info = info.split('\n')[1]
	info = info.split()[0]
	#for i in info.split('; '):
	#	result.append(i);
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

def createExcelFile(fname, reference):
	## Creating an XLSX file
	workbook = xlsxwriter.Workbook(fname)
	worksheet = workbook.add_worksheet()
	
	referenceList = openReference(reference)
	counter = 0;
	for gene in referenceList:
		worksheet.write(counter, 0, gene.split()[0]) # first is row, then , then value
		geneOntology = getGeneOntologyFromUniprot('http://www.uniprot.org/uniprot/?query=' + str(gene.split()[0]) + '&format=tab&column=id')
		worksheet.write(counter, 1, geneOntology) # first is row, then , then value
		counter += 1
		#for item in geneOntologyList:
		#	columnCounter += 1
		#	worksheet.write(rowCounter, columnCounter, item) # first is row, then , then value
		#rowCounter += 1
		print(str(gene) + ': %' + str(100*counter/len(referenceList)))
	workbook.close()
# void

getGeneOntologyFromUniprot(url)
#createExcelFile(sheetName, referenceName) 
