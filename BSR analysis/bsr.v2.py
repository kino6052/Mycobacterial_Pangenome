## SCORE RATIO ANALYSIS
## CREATED: 10/21/2014. Influenced by "Pangenome Structure of Escherichia coli" by Rasco, 2008 Journal of Bacteriology
## PURPOSE: TO IDENTIFY UNIQUE GENES IN M. VACCAE
## REFERENCE: HERE IS THE REFERENCE TO THE BIOPYTHON TUTORIAL IMPLEMENTED HERE: http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec95
## OUTPUT FORMAT:PROTEIN	ALIGNMENT	SCORE

import sys
import urllib
import time

# command line arguments
if len(sys.argv) < 2:
	print('\nUsage: python bsr.py -protein_name(or file_name.txt) -protein_from_list -w')
	sys.exit()

if '.txt' in sys.argv[1]:
	# input
	inputFile = open(str(sys.argv[1]), 'rt')

	# make a list of protein names obtained from the file
	proteinList = []
	
	# start from a non-starting protein
	nonstart = 0;
	
	for line in inputFile:
		if len(line) > 9:
			print("Input Error: use a single column of ensembl ids")
		else: 
			if len(sys.argv) >= 3:
				protein = str(line.split()[0])
				if protein == sys.argv[2]:
					nonstart = 1;
				if nonstart:
					proteinList.append(protein)
			else:
				protein = str(line.split()[0])
				proteinList.append(protein)
	inputFile.close()
	print('\nfile is processed\n')

else:
	proteinList = [str(sys.argv[1])]

# output
if len(sys.argv) > 3 and sys.argv[3] == 'w':
	outputFile = open('unique.txt', 'w')
	outputFile2 = open('output.txt', 'w')
else:
	outputFile = open('unique.txt', 'a')
	outputFile2 = open('output.txt', 'a')

# import modules for NCBI Blast service.
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

print("\nBSR ANALYSIS:\n")

# list iterrator
proteinState = 0

# main cycle
while(True):
	try:
		for protein in proteinList[proteinState:]:
			print(str(protein) + "\t")
			outputFile2.write(str(protein) + "\t")
			print('Analysis in progress...\n')
			
			# blastp result handle
			result_handle = NCBIWWW.qblast("blastp", "nr", protein)

			# read the result handle
			blast_record = NCBIXML.read(result_handle) #read is for 1 object and parse is for multiple (iterator)

			E_VALUE_THRESH = 0.04 #specifiying the main sorting parameter

			# retrieve data from the xml
			reference = 0
			query = 0
			for alignment in blast_record.alignments:
				
				#find the name of the organism in the alignment
				title = alignment.title
				title_start = title.find('[')
				title_stop = title.find(']')
				title = title[title_start+1:title_stop]
				
				#find REF and QUE
				for hsp in alignment.hsps:
					if "vaccae" in str(alignment.title):
						reference = hsp.score
						print("REF: " + str(title) + ", SCORE: " + str(hsp.score) + ", BIT SCORE: " + str(hsp.bits) + "\n")
						break
					if "Mycobacterium" in str(alignment.title):
						query = hsp.score
						print("QUE: " + str(title) + ", SCORE: " + str(hsp.score) + ", BIT SCORE: " + str(hsp.bits) + "\n")
						outputFile2.write(str(alignment.title) + '\t')
						break
				
				# quit the loop as soon as we find first QUE
				if query != 0:
					break
			
			#result
			if reference != 0:
				result = query/reference
				proteinState += 1
			else:
				proteinState += 1
				break
			print("Score Ratio (" + str(sys.argv[0]) + "_" + str(protein) + "): " + str(result) + "\n\nDone\n")
			outputFile2.write(str(result) + '\n')
			if result < 0.4:
				print(str(protein) + " is unique.\n")
				outputFile.write(str(protein) + '\t' + str(alignment.title) + '\t' + str(result) + '\n')
				outputFile.write(str(alignment.title) + '\t' + str(result) + '\n')
			result_handle.close()
		if (protein == proteinList[-1]):
			outputFile.close()
			outputFile2.close()
			break
	except urllib.error.URLError or urllib.error.TimeoutError:
		time.sleep(10)
	print('\nDone')
