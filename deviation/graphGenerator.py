import xlsxwriter
from os import walk

## Open the file with the results
file = open('result.txt', 'r')

## Creating an XLSX file
workbook = xlsxwriter.Workbook('UniqueGenes.xlsx')
worksheet = workbook.add_worksheet()


## Creating the list with the files in the directory
result = open('graph.txt', 'w')
l_init = 1
sum_genes = 0
count = 0

for line in file:
	length = len(line.split()[:-1])
	
	# Length must stay the same in order to add up the gene counts
	if length == l_init:
		sum_genes += int(line.split()[-1])
	
	# Writing the results out if the length increases by 1 
	if length > l_init:
		worksheet.write(length-1, 0, length-1)
		worksheet.write(length-1, 1, sum_genes/count) 
		print(length-1)
		print(sum_genes/count)
		
		# Reinitialize the variables
		l_init = length
		sum_genes = 0
		count = 0
		sum_genes += int(line.split()[-1])
	
	# Writing the last result out
	if length == 19:
		worksheet.write(19, 0 , 19)
		worksheet.write(19, 1, int(line.split()[-1]))
		print(length)
		print(int(line.split()[-1]))
		
	count += 1
