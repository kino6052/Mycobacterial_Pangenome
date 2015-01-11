import xlsxwriter
import math

## Creating an XLSX file
#workbook = xlsxwriter.Workbook('StandardDeviation.xlsx')
#worksheet = workbook.add_worksheet()

## Standard deviation
def s_deviation(list):
	## The average
	average = 0
	for element in list:
		average += int(element)
	average = average/len(list)
	
	##For each element we have to find the difference raised to the power of 2
	s_dev = 0
	for element in list:
		s_dev += (int(element) - average)**2
	s_dev = math.sqrt(s_dev/len(list))
	return s_dev, average
		
## A dictionary with results
def make_dic(file):
	file_name = open(file, 'r')
	dictionary = {}
	counter = 1
	for i in file_name:
		tuple_element = i.split()[:-1]
		if len(tuple_element) != counter:
			counter += 1
		if counter not in dictionary:
			dictionary[counter] = []
			dictionary[counter].append(i.split()[-1])
		else:
			dictionary[counter].append(i.split()[-1])
	return dictionary

## Averages
def averages(dictionary):
	result = []
	avg = 0
	for key in dictionary:
		for element in dictionary[key]:
			avg += int(element)
		avg = avg/len(dictionary[key])
		result.append(avg)
	return result

def main():
	deviation_file = open('deviations.txt', 'w')
	avgs_file = open('averages.txt', 'w')
	dic = make_dic('result.txt')
	
	for key in dic:
		data = s_deviation(dic[key])
		deviation_file.write(str(data[0])+ '\n')
		avgs_file.write(str(data[1]) + '\n')
	
	deviation_file.close()
	avgs_file.close()

main()
