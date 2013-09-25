"""
pyBandPlot.py

Author: Daniel Burrill
Date Created: September 23, 2013
Date Last Modified: September 25, 2013

v1.01
- Added DOS Functionality

v1.00
- Initial Build

Description:
 Provides plotting automation for the creation of bandstructure
 graphs. Changes to the graph can be made through the format.txt
 file. Format file only looks for special keywords, all else is
 ignored.
 
 Input files should be csv files formatted by pyBand3 for best
 results.
"""

# Imports
import pylab

# Variables
formFile = 'format.txt'
dosInc = False

# Font Dictionary
fontDictionary = {'horizontalalignment':'center',
                  'fontsize':16}

# Functions
def loadFormat(fileName):
    # Variables
    formatDict = {}
    
    fFile = open(fileName,'r')
    
    # Put all format data into dictionary
    for line in fFile:
        # Skip Empty Lines
        if (line != '\n'):
            data = line.strip('\n').split('=')
            formatDict[data[0].lower()] = data[1]
        
    # Format data in dictionary for desired use
    for element in formatDict:
        # X Limits
        if (element == 'xlim'):
            data2 = formatDict[element].split(',')
            formatDict[element] = (float(data2[0]),float(data2[1]))
        
        # Y Limits
        if (element == 'ylim'):
            data2 = formatDict[element].split(',')
            formatDict[element] = (float(data2[0]),float(data2[1]))
        
        # Fermi Energy
        if (element == 'fenergy'):
            formatDict[element] = float(formatDict[element])
        
        # Exclusion of Bands
        if (element == 'bandexcl'):
            dataCont = []
            data2 = formatDict[element].split(',')
            
            for value in data2:
                # Account for Ranges
                if (':' in value):
                    rangeStr = value.split(':')
                    dataCont.extend(range(int(rangeStr[0]),int(rangeStr[-1])+1))
                else:
                    dataCont.append(int(value))
                    
            formatDict[element] = dataCont
        
        # Special Locations
        if (element == 'sploc'):
            dataCont = []
            data2 = formatDict[element].split(',')
            
            for value in data2:
                dataCont.append(float(value))
                    
            formatDict[element] = dataCont
        
        # Special Labels
        if (element == 'splab'):
            dataCont = []
            data2 = formatDict[element].split(',')
            
            for value in data2:
                dataCont.append(value)
                    
            formatDict[element] = dataCont
            
        ### DOS ###
        # Data Labels
        if (element == 'doslab'):
            dataCont = []
            data2 = formatDict[element].split(',')
            
            for value in data2:
                dataCont.append(value)
                    
            formatDict[element] = dataCont
            
        # DOS Colors
        if (element == 'doscol'):
            dataCont = []
            data2 = formatDict[element].split(',')
            
            for value in data2:
                dataCont.append(value)
                    
            formatDict[element] = dataCont
        
        # csv File Name Should be Formatted
        
    return formatDict

# Main
if __name__ == '__main__':
    
    # Load Format File
    paramDict = loadFormat(formFile)    
    
    # Load csv Data
    bandData = pylab.transpose(pylab.loadtxt(paramDict['csvfile'],
                                             delimiter=','))
     
    # Check for DOS Data                                                                                 
    if ('doscsvfile' in paramDict):
        dosData = pylab.transpose(pylab.loadtxt(paramDict['doscsvfile'],
                                                delimiter=','))
        dosInc = True
    
    # Plot csv Data
    for index,row in enumerate(bandData):
        # If DOS Included
        if (dosInc == True):
            bandGraph = pylab.subplot(1,2,1)
        # If not Header Row or excluded
        if (index != 0) and (index not in paramDict['bandexcl']):
            pylab.plot(row,antialiased=True,lw=1.5)
            
    # Plot Line at Fermi Energy
    pylab.axhline(paramDict['fenergy'],linestyle='dashed',color='black')
    
    # Remove X Axis
    graph = pylab.gca()
    graph.axes.get_xaxis().set_visible(False)
    
    # Add X Axis Characters
    for index,sp in enumerate(paramDict['sploc']):
        # Vertical Line
        graph.vlines(sp,paramDict['ylim'][0],paramDict['ylim'][1])
        # X Axis Label
        graph.text(sp,paramDict['ylim'][0]-0.65,
                      paramDict['splab'][index],
                      fontdict=fontDictionary)
            
    # Adjustments to Band Plot
    pylab.xlim(paramDict['xlim'])
    pylab.ylim(paramDict['ylim'])
    pylab.ylabel('Energy (eV)',fontdict=fontDictionary)
    
    # DOS Plot
    if (dosInc == True):
        dosGraph = pylab.subplot(1,2,2)
        
        # Plot if not Header
        for index,row in enumerate(dosData[1:]):
            pylab.plot(row,dosData[0],antialiased=True,label=paramDict['doslab'][index+1],lw=1.5,c=paramDict['doscol'][index])
                
        # Adjust DOS Graph
        dosGraph.axes.get_yaxis().set_visible(False)
        pylab.ylim(paramDict['ylim'])
        pylab.xlabel('DOS',fontdict=fontDictionary)
        pylab.legend()
        pylab.tight_layout()
        
        # Plot Line at Fermi Energy
        pylab.axhline(paramDict['fenergy'],linestyle='dashed',color='black')
    
    pylab.show()