fileIn = open("pieChart.txt", "r")
fileCCOut = open("CellCompartment.txt", "w")
fileBPOut = open("BiologicalProcess.txt", "w")
fileMFOut = open("MolecularFunction.txt", "w")
dictCC = {}
dictBP = {}
dictMF = {}

for line in fileIn:
	## First Column
	CC = line.split("\t")[0]
	BP = line.split("\t")[1]
	MF1 = line.split("\t")[2]
	MF2 = line.split("\t")[3]
	MF3 = line.split("\t")[4]
	MF4 = line.split("\t")[5]
	MF5 = line.split("\t")[6]
	MF6 = line.split("\t")[7]
	MF7 = line.split("\t")[8]

	
	if  CC not in dictCC:
		dictCC[CC] = 1;
	else:
		dictCC[CC] +=1;
		
	if  BP not in dictBP:
		dictBP[BP] = 1;
	else:
		dictBP[BP] +=1;
	
	if  MF1 not in dictMF:
		dictMF[MF1] = 1;
	else:
		dictMF[MF1] +=1;
	
	if  MF2 not in dictMF:
		dictMF[MF2] = 1;
	else:
		dictMF[MF2] +=1;

	if  MF3 not in dictMF:
		dictMF[MF3] = 1;
	else:
		dictMF[MF3] +=1;
		
	if  MF4 not in dictMF:
		dictMF[MF4] = 1;

	else:
		dictMF[MF4] +=1;
		
	if  MF5 not in dictMF:
		dictMF[MF5] = 1;
	else:
		dictMF[MF5] +=1;
		
	if  MF6 not in dictMF and MF6 != "":
		dictMF[MF6] = 1;
	else:
		dictMF[MF6] +=1;
	
	if  MF7 not in dictMF:
		dictMF[MF7] = 1;
	else:
		dictMF[MF7] +=1;
				
print(dictMF)
for entry in dictCC:
	fileCCOut.write(str(entry) + "\t" + str(dictCC[entry]) + "\n")
for entry in dictBP:
	fileBPOut.write(str(entry) + "\t" + str(dictBP[entry]) + "\n")
for entry in dictMF:
	fileMFOut.write(str(entry) + "\t" + str(dictMF[entry]) + "\n")
	
fileIn.close()
fileCCOut.close()
fileBPOut.close()
fileMFOut.close()		
