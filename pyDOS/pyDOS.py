"""
pyDOS.py

Author: Daniel Burrill
Date Created: August 2, 2013
Date Last Modified: August 5, 2013

Description:
 Meant to grab DOS data from vasprun.xml file. Outputs to csv format. Utilizes python XML support.
"""

# Imports
import xml.etree.ElementTree as ET

# Variables
fileName = 'vasprun.xml'		# Name of input file

energy = []			# Array of k-point weights
TDOS = []			# Array of band eigenvalues
ionCont = []			# Array of Ion Data
LDOSCont = []			# Total LDOS
LPDOSCont = []			# Localized Partial DOS

outFile = 'DOSOut.csv'		# Name of output file

# Functions
def DOSInfo(inFile):

    # Containers
    energy = []			# Array of k-point weights
    TDOS = []			# Array of band eigenvalues
    
    # Open file to parse with XML
    tree = ET.parse(inFile)

    # Load Root (modeling)
    root = tree.getroot()
               
    # Populate Energy & TDOS Container
    # Find DOS container
    nodeCalculation = root.find('calculation')
    nodeDOS = nodeCalculation.find('dos')
    nodeTotal = nodeDOS.find('total')
    nodeArray = nodeTotal.find('array')
    nodeSet = nodeArray.find('set')
    nodeSetSpin = nodeSet.find('set')
    
    for DOSVal in nodeSetSpin.findall('r'):
        dmyStrCont = DOSVal.text.split()
	energy.append(dmyStrCont[0])
        TDOS.append(dmyStrCont[1])
        
    # Shift Fermi Energy to Zero Point
    # Find Fermi Energy
    iNode = nodeDOS.find('i')
    fermiEnergy = float(iNode.text.strip())

    # Shift by Fermi Energy
    for index,energyVal in enumerate(energy):
	energy[index] = str(float(energyVal) - float(fermiEnergy))

    return energy,TDOS
    
def PDOSInfo(inFile):
    # Containers
    ionCont = []		# Array of Ion Data
    
    # Open file to parse with XML
    tree = ET.parse(inFile)

    # Load Root (modeling)
    root = tree.getroot()
               
    # Populate Energy & TDOS Container
    # Find PDOS container
    nodeCalculation = root.find('calculation')
    nodeDOS = nodeCalculation.find('dos')
    nodePartial = nodeDOS.find('partial')
    nodeArray = nodePartial.find('array')
    nodeSet = nodeArray.find('set')
    
    for Ion in nodeSet.findall('set'):
	nodeSetSpin = Ion.find('set')
	dmyEnergyList = []
	
	for PDOSVal in nodeSetSpin.findall('r'):
	    dmyStrCont = PDOSVal.text.split()
	    dmyValCont = []
	    
	    for value in dmyStrCont:
		dmyValCont.append(value)
		
	    dmyEnergyList.append(dmyValCont)
	    
	ionCont.append(dmyEnergyList)
        
    # Shift Fermi Energy to Zero Point
    # Find Fermi Energy
    iNode = nodeDOS.find('i')
    fermiEnergy = float(iNode.text.strip())

    # Shift by Fermi Energy
    # Shift only the first column
    for index1,ion in enumerate(ionCont):
	for index2,energyData in enumerate(ion):
	    energyData[0] = str(float(energyData[0])-fermiEnergy)

    return ionCont
	
def getAtomTypeList(inFile):
    # Containers
    atomTypeCont = []		# Array of Ion Data
    
    # Open file to parse with XML
    tree = ET.parse(inFile)

    # Load Root (modeling)
    root = tree.getroot()
               
    # Populate Atom Type Container
    nodeAtomInfo = root.find('atominfo')
    nodeArray = nodeAtomInfo.find('array')
    nodeSet = nodeArray.find('set')
    
    for atom in nodeSet.findall('rc'):
	iterator1 = 0
	
	for atomVal in atom.findall('c'):
	    if (iterator1 == 1):
		atomTypeCont.append(atomVal.text.strip())
	    else:
		iterator1 = 1
		
    return atomTypeCont
    
def sum(inList):
    total = 0.0000
    
    for value in inList:
	total = total + float(value.strip())
	
    return total 
    
# Main Loop
if (__name__ == '__main__'):

    # Get Band Information


##### DOS #####
    energy,TDOS = DOSInfo(fileName)

    # Open outFile
    oFile = open(outFile, 'w')

    # Print Header
    oFile.write('# Energy (eV), Total DOS \n')

    # Save eigs to outFile
    for index,energyVal in enumerate(energy):
	    
        # Create String from line
        tempString = energyVal + ',' + TDOS[index] + '\n'

        # Write Band to File
        oFile.write(tempString)

    # Close oFile
    oFile.close()
    
##### PDOS #####
    ionCont = PDOSInfo(fileName)

# Save PDOS to outFiles
    for index1,ion in enumerate(ionCont):
	# Open outFile
        oFile = open('PDOSData' + str(index1+1) + '.csv', 'w')

        # Print Header
        oFile.write('# Energy (eV), s, py, pz, px, dxy, dyz, dz2, dxz, dx2 \n')
	    
	    
	for index2,energyData in enumerate(ion):
	    tmpString = ''
	    for index3,data in enumerate(energyData):
		if (index3 == len(energyData)-1):
		    tmpString = tmpString + data + '\n'
		else:
		    tmpString = tmpString + data + ','
		    
	    oFile.write(tmpString)
	    
	oFile.close()
	
##### LDOS #####
    # Place Holder Container - Labels atom type for positions in atomTypeCont
    placeCont = []

    # Create List of atom types
    atomTypeCont = getAtomTypeList(fileName)

    # Populate LDOS
    for index,ion in enumerate(ionCont):
	# Check to see if atom type is already in LDOS
	if (atomTypeCont[index] in placeCont):
	    atomPos = placeCont.index(atomTypeCont[index])
	    
	    for index2,energy1 in enumerate(LDOSCont[atomPos]):
		LDOSCont[atomPos][index2][1] = str(float(energy1[1]) + sum(ion[index2][1:]))

		# S orbitals
		LPDOSCont[atomPos][index2][1] = str(float(LPDOSCont[atomPos][index2][1]) + float(ion[index2][1]))

		# P Orbitals
		LPDOSCont[atomPos][index2][2] = str(float(LPDOSCont[atomPos][index2][2]) + sum(ion[index2][2:5]))

		# D Orbitals
		LPDOSCont[atomPos][index2][3] = str(float(LPDOSCont[atomPos][index2][3]) + sum(ion[index2][5:]))
		
	else:
	    placeCont.append(atomTypeCont[index])
	    
	    dmyLDOS = []
	    dmyLPDOS = []
	    for index2,energy1 in enumerate(ion):
		dmyLDOS.append([energy1[0],str(sum(energy1[1:]))])
		dmyLPDOS.append([energy1[0],ion[index2][1],str(sum(ion[index2][2:5])),str(sum(ion[index2][5:]))])

	    LDOSCont.append(dmyLDOS)
	    LPDOSCont.append(dmyLPDOS)
	    
    # Sort LDOS & LPDOS such that lowest atom type number is first
    for index,value in enumerate(placeCont):
	lowVal = int(value)
	lowInd = index
	dmyHolder = 0	

	for index2,value2 in enumerate(placeCont[index:]):
	    if (int(value2) < lowVal):
		lowVal = int(value2)
		lowInd = index2
		
	# Swap
	dmyHolder = LDOSCont[lowInd]
	LDOSCont[lowInd] = LDOSCont[index]
	LDOSCont[index] = dmyHolder
	dmyHolder = LPDOSCont[lowInd]
	LPDOSCont[lowInd] = LPDOSCont[index]
	LPDOSCont[index] = dmyHolder
	placeCont[lowInd] = str(value)
	placeCont[index] = str(lowVal)

    # Output
    for index1,atomType in enumerate(LDOSCont):
	# Open outFile
        oFile = open('LDOSData' + str(placeCont[index1]) + '.csv', 'w')
	o2File = open('LPDOSDATA' + str(placeCont[index1]) + '.csv', 'w')

        # Print Header
        oFile.write('# Atomtype Number: ' + placeCont[index1] + ' \n')
	oFile.write('# Energy (eV), LDOS \n')
	o2File.write('# Atomtype Number: ' + placeCont[index1] + ' \n')
	o2File.write('# Energy (eV), S Orbital, P Orbital, D Orbital \n')
	    
	    
	for index2,energyData in enumerate(atomType):
	    tmpString = ''
	    tmpString2 = ''
	    for index3,data in enumerate(energyData):
		if (index3 == len(energyData)-1):
		    tmpString = tmpString + data + '\n'
		else:
		    tmpString = tmpString + data + ','

	    for index3,data in enumerate(LPDOSCont[index1][index2]):
		if (index3 == len(LPDOSCont[index1][index2])-1):
		    tmpString2 = tmpString2 + data + '\n'
		else:
		    tmpString2 = tmpString2 + data + ','
		    
	    oFile.write(tmpString)
	    o2File.write(tmpString2)
	    
	oFile.close()
	o2File.close()
	
	
