"""
pyGeom.py

Author: Daniel Burrill
Date Created: August 13, 2013
Date Last Modified: August 13, 2013

v1.00
- Wrote base script

Description:
 Grabs the geometry distortions from the vasprun.xml and outputs
 to an .xyz file for animation.
"""

# Imports
import xml.etree.ElementTree as ET

# Variables
version = 1.00                  # PyBand3 Version
#fileName = 'vasprun.xml'	# Name of input file

calcCont = []			# Array of Geometry Distortions
atomTypeCont = []               # Array of Atom Types

outFile = 'geomOut.xyz'		# Name of output file

# Functions
def UIFunc():
    '''
    UIFunc

    Handles UI
    '''

    print "pyGeom v" + str(version) + "\n"
    print "Author: Daniel J. Burrill \n"

    fileName = raw_input('Enter Input Filename (w/ extension): ')

    return fileName

def geomInfo(inFile):

    # Containers
    calcCont = []		# Array of Geometry Distortions
    atomTypeCont = []           # Array of Atom Types
    
    # Open file to parse with XML
    tree = ET.parse(inFile)

    # Load Root (modeling)
    root = tree.getroot()

    # Populate calcCont
    for calculation in root.findall('calculation'):
        # Dummy Containers
        distDmy = []            # Distortion Container
        
        structure = calculation.find('structure')
        crystal = structure.find('crystal')

        # Add Lattice Basis
        for varray in crystal.findall('varray'):
            if (varray.get('name') == 'basis'):
                basisDmy = []
                for v in varray.findall('v'):
                    basisDmy.append(v.text.split())

                distDmy.append(basisDmy)

        # Add Atom Positions
        for varray in structure.findall('varray'):
            if (varray.get('name') == 'positions'):
                posDmy = []
                for v in varray.findall('v'):
                    posDmy.append(v.text.split())

                distDmy.append(posDmy)

        # Append to calcCont
        calcCont.append(distDmy)

    # Populate atomTypeCont
    atomInfo = root.find('atominfo')

    for atomArray in atomInfo.findall('array'):
        if (atomArray.get('name') == 'atoms'):
            atomSet = atomArray.find('set')

            for rc in atomSet.findall('rc'):
                atomTypeCont.append(rc.find('c').text.strip())
    

    return calcCont,atomTypeCont
    
# Main Loop
if (__name__ == '__main__'):
    # Start UI
    fileName = UIFunc()

    # Get Geometry Information
    calcCont,atomTypeCont = geomInfo(fileName)

    # Open outFile
    oFile = open(outFile, 'w')

    # Output to XYZ File
    for index,distCont in enumerate(calcCont):
        # Print Header for Each Distortion
        oFile.write(str(len(distCont[1])) + '\n')           # Number of Atoms
        oFile.write('Distortion ' + str(index) + '\n')      # Distortion Number

        for index2,atomPos in enumerate(distCont[1]):
            lat1 = [float(distCont[0][0][0])*float(atomPos[0]),
                    float(distCont[0][0][1])*float(atomPos[0]),
                    float(distCont[0][0][2])*float(atomPos[0])]
            lat2 = [float(distCont[0][1][0])*float(atomPos[1]),
                    float(distCont[0][1][1])*float(atomPos[1]),
                    float(distCont[0][1][2])*float(atomPos[1])]
            lat3 = [float(distCont[0][2][0])*float(atomPos[2]),
                    float(distCont[0][2][1])*float(atomPos[2]),
                    float(distCont[0][2][2])*float(atomPos[2])]

            xPos = lat1[0]+lat2[0]+lat3[0]
            yPos = lat1[1]+lat2[1]+lat3[1]
            zPos = lat1[2]+lat2[2]+lat3[2]

            oFile.write(atomTypeCont[index2] + '\t' + str(xPos) + '\t' + str(yPos) + '\t' + str(zPos) + '\n')

    # Close oFile
    oFile.close()
                
