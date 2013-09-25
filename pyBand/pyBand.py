"""
pyBand.py

Author: Daniel Burrill
Date Created: June 10, 2013
Date Last Modified: June 10, 2013

Description:
 Meant to grab kpoint data from OUTCAR file to help with band structure calculations on systems using hybrid functionals.
"""

# Variables
fileName = 'OUTCAR'
fileCont = []
catchStr = ' k-points in reciprocal lattice and weights: K-Points '
dataCont = []
switch = False
outFile = 'output'

# Functions
def getFileData(fFileName):
	# Open File
	fFile = open(fFileName,'r')

	return fFile

# Main Loop
if (__name__ == '__main__'):

	# Format catchStr to catchLine
	catchLine = catchStr.split()

	# Get Data Lines from File
	fileCont = getFileData(fileName)

	# Parse Through fileCont Looking for catchStr
	for line in fileCont:
		# Remove White Space Padding
		line = line.strip()

		# Separate Words by Spaces
		line = line.split()

		# Stop Recording if End of Block is Reached
		if (line == []) and (switch == True):
			switch = False

		# Record Lines in Specified Zone
		if (switch == True):
			# Set Weight Factor to Zero
			line[3] = '0'
			dataCont.append(line)

		# Check line Against catchLine
		if (catchLine == line) and (switch == False):
			switch = True

	# Close fileCont and Open outFile
	fileCont.close()
	oFile = open(outFile, 'w')

	# Save dataCont to outFile
	for line in dataCont:
		# Create String from line
		tempString = ''

		for index,element in enumerate(line):
		    if (index == len(line)-1):
			tempString = tempString + element + '\n'
		    else:
			tempString = tempString + element + '\t'

		oFile.write(tempString)

	# Close oFile
	oFile.close()
		
