import csv

# Game Object

# Game index

# Match CSV ID

# Team names

# Two arrays for each teams score

# Time outs

# Who won

def who_won(path_to_file):
	with open(path_to_file, 'rb') as csvfile:
		datareader = csv.reader(csvfile, delimiter=',')
		for i, row in enumerate(datareader):
			if i < 3:
				continue
			if i > 4:
				break	
			for j, cell in enumerate(row):
				if j < 21:
					continue
				if j > 21:
					break
				print('i: ' + str(i) + ', j: ' + str(j) + ' has cell: ' + cell)

# Third game?

# Score to win

def parse_data(path_to_file):
	with open(path_to_file, 'rb') as csvfile:
		datareader = csv.reader(csvfile, delimiter=',')
		for i, row in enumerate(datareader):
			if i != 3 and i != 4:
				continue
			for j, cell in enumerate(row):
				if j < 7 or j > 21:
					continue
				print('i: ' + str(i) + ', j: ' + str(j) + ' has cell: ' + cell)



parse_data("/Users/tommyserrino/volleyballdir/DataDirectory/8a51d027-4fbf-4030-b1af-0f5f7a5bdbed.csv")
who_won("/Users/tommyserrino/volleyballdir/DataDirectory/8a51d027-4fbf-4030-b1af-0f5f7a5bdbed.csv")