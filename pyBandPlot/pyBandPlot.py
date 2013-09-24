"""
pyBandPlot.py

Author: Daniel Burrill
Date Created: September 23, 2013
Date Last Modified: September 23, 2013

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
        
        # csv File Name Should be Formatted
        
    return formatDict

# Main
if __name__ == '__main__':
    
    # Load Format File
    paramDict = loadFormat(formFile)    
    
    # Load csv Data
    bandData = pylab.transpose(pylab.loadtxt(paramDict['csvfile'],
                                             delimiter=','))
    
    # Plot csv Data
    for index,row in enumerate(bandData):
        # If not Header Row or excluded
        if (index != 0) and (index not in paramDict['bandexcl']):
            pylab.plot(row,antialiased=True)
            
    # Plot Line at Fermi Energy
    pylab.hlines(paramDict['fenergy'],
                 paramDict['xlim'][0],
                 paramDict['xlim'][1],
                 linestyles='dashed')
    
    # Remove X Axis
    graph = pylab.gca()
    graph.axes.get_xaxis().set_visible(False)
    
    # Add X Axis Characters
    for index,sp in enumerate(paramDict['sploc']):
        # Vertical Line
        graph.vlines(sp,paramDict['ylim'][0],paramDict['ylim'][1])
        # X Axis Label
        graph.text(sp,paramDict['ylim'][0]-0.75,
                      paramDict['splab'][index],
                      fontdict=fontDictionary)
            
    # Adjustments to Plot & Show
    pylab.xlim(paramDict['xlim'])
    pylab.ylim(paramDict['ylim'])
    pylab.ylabel('Energy (eV)',fontdict=fontDictionary)
    pylab.show()