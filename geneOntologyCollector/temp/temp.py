inFile = open('temp.txt', 'r')
outFile = open('tempResult.txt', 'w')

for line in inFile:
	if line.find('P:') != -1:
		start = line.find('P:')
		stop = start + line[start:].find(';')
		outFile.write(line[start:stop] + '\n')
	else:
		outFile.write("P:unknown\n")

inFile.close()
outFile.close()
