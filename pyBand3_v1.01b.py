"""
pyBand3.py

Author: Daniel Burrill
Date Created: June 13, 2013
Date Last Modified: August 14, 2013

v1.01b
- Added manual input & output filename
- Fixed bug in hybrid section

v1.01a
- Added UI support
- Added Header
- Fixed Minor Bugs

Description:
 Meant to grab kpoint data from vasprun.xml file to help with
 band structure calculations on systems using hybrid functionals.
 Outputs to csv format. Utilizes python XML support.
"""

# Imports
import xml.etree.ElementTree as ET

# Variables
version = 1.01                  # PyBand3 Version

weights = []			# Array of k-point weights
eigs = []			# Array of band eigenvalues
occ = []			# Array of band occupancies

# Functions
def UIFunc():
    '''
    UIFunc

    Handles UI
    '''

    print "pyBand3 v" + str(version) + "\n"
    print "Author: Daniel J. Burrill \n"
    print "Choose Type of Functional:"
    print "1) Hybrid"
    print "2) GGA \n"
    
    funcType = raw_input('--> ')
    fileName = raw_input('Enter Input XML File Name (w/ extension): ')
    outFile = raw_input('Enter Output File Name (w/o extension): ')

    return funcType, fileName, outFile

def bandInfo(inFile, funcType):

    # Containers
    weights = []		# Array of k-point weights
    eigs = []			# Array of band eigenvalues
    occ = []			# Array of band occupancies
    
    # Open file to parse with XML
    tree = ET.parse(inFile)

    # Load Root (modeling)
    root = tree.getroot()

    # Populate Weight Container
    # Find Kpoints container
    kpoints = root.find('kpoints')

    for varray in kpoints.findall('varray'):
        if (varray.get('name') == 'weights'):
            for weight in varray.findall('v'):
                weights.append(weight.text.strip())
                
    # Populate Eigenvalue and Occupancy Containers
    # Find Eigenvalues & Occupancies
    nodeCalculation = root.find('calculation')
    nodeEigenvalue = nodeCalculation.find('eigenvalues')
    nodeArray = nodeEigenvalue.find('array')
    nodeSet = nodeArray.find('set')
    nodeSetSpin = nodeSet.find('set')

    for kpoint in nodeSetSpin.findall('set'):
        dmyContEnergy = []
        dmyContOcc = []
        
        for eigenEnergy in kpoint.findall('r'):
            dmyStrCont = eigenEnergy.text.split()
            dmyContEnergy.append(dmyStrCont[0])
            dmyContOcc.append(dmyStrCont[1])

        eigs.append(dmyContEnergy)
        occ.append(dmyContOcc)

    # Remove K-Points with Non-Zero Weight
    if (int(funcType) == 1):
        zeroString = '0.00000000'
        weightSwitch = False

        while (weightSwitch == False):
            for index,weight in enumerate(weights):
                if (weight != zeroString):
                    eigs.pop(index)
                    occ.pop(index)
                    weights.pop(index)
                    break
                elif (index == len(weights)-1):
                    weightSwitch = True
                    break

    # Shift Fermi Energy to Zero Point
    fermiEnergy = float(eigs[1][1])

    # Find Fermi Energy
    for index,kpt in enumerate(eigs):
        for index2,energy in enumerate(kpt):
            if (float(energy) > float(fermiEnergy)) and (float(occ[index][index2]) > 0):
                fermiEnergy = float(energy)
                            
    # Shift by Fermi Energy
    for index,kpt in enumerate(eigs):
        for index2,energy in enumerate(kpt):
            eigs[index][index2] = str(float(energy) - float(fermiEnergy))

    return eigs,occ,weights
    
# Main Loop
if (__name__ == '__main__'):
    # Start UI
    funcType,fileName,outFile = UIFunc()

    # Get Band Information
    eigs,occ,weights = bandInfo(fileName,funcType)

    # Open outFile
    oFile = open(outFile + '.csv', 'w')

    # Print Header
    headerStr = '# kpt #,'

    for bandNum in range(len(eigs[0])):
        if (bandNum == len(eigs[0])-1):
            headerStr = headerStr + 'Band # ' + str(bandNum+1) + ', \n'
        else:
            headerStr = headerStr + 'Band # ' + str(bandNum+1) + ','

    oFile.write(headerStr)

    # Save eigs to outFile
    for index,kpt in enumerate(eigs):
            
        # Create String from line
        tempString = str(index+1) + ','
            
        for index2,energy in enumerate(kpt):

            # If last element print and start new line
            if (index2 == len(kpt)-1):
                tempString = tempString + energy + '\n'
            # Else normal print with comma
            else:
                tempString = tempString + energy + ','

        # Write Band to File
        oFile.write(tempString)

    # Close oFile
    oFile.close()
                
