import csv

# Game Object

# Game index

# Match CSV ID

# Team names

# Two arrays for each teams score

# Time outs

# Who won

# Third game?

# Score to win

def parse_data(path_to_file):
	with open(path_to_file, 'rb') as csvfile:
		datareader = csv.reader(csvfile, delimiter=',')
		for i, row in enumerate(datareader):
			for j, cell in enumerate(row):
				print('i: ' + str(i) + ', j: ' + str(j) + ' has cell: ' + cell)


parse_data("/Users/tommyserrino/volleyballdir/DataDirectory/8a51d027-4fbf-4030-b1af-0f5f7a5bdbed.csv")