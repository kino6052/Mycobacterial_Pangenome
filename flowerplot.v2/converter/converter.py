import sys
from os import system
from os import listdir
from os.path import isfile, join

files = [ f for f in listdir('./') if isfile(join('./',f)) and '.fa' in f and 'database' not in f ]

outFile = open('tuberculosis.fa', 'w')

for i in files:
	if 'tuberculosis' in i:
		print(i)
		inFile = open(i, 'r')

for line in inFile:
	substitute = line.find('KEP')
	if substitute != -1:
		line = line[0:substitute] + 'TUB' + line[substitute+3:]
	outFile.write(line)

outFile.close()
inFile.close()

