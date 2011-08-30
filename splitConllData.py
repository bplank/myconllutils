#!/usr/bin/python3

from optparse import OptionParser
import sys
import math

""" 
Author: Barbara Plank
Date:   August 2011

Description: Given a CoNLL 2007 file, this script splits it into N
folds (default is 10).

Options: size of fold 

"""
def getNumSents(filename):
    FILEIN = open(filename,"r")
    count = 0
    for line in FILEIN:
        lineList = line.split("\t")
        if len(lineList) == 1:
            count = count + 1
    FILEIN.close()
    print(count)
    return count

def splitData(filename,folds):
    FILEIN = open(filename,"r")

    lines = FILEIN.readlines()
    totalSents = getNumSents(filename)

    print("Total sentences: {}".format(totalSents))
    
    if totalSents < folds:
        print("Error: fewer sentences than folds!")
        sys.exit(-1)
    
    perFold = math.ceil(totalSents/folds)
    print("Per fold: {}".format(perFold))
    numInst=0
    fold=0
    FILEOUT = open(filename+".f"+str(fold),"w")
    linenum=0
    for line in lines:
        linenum+=1
        lineList = line.split("\t")
        
        FILEOUT.write(line)
        
        if len(lineList) ==1:
            numInst +=1
            if numInst > 0 and numInst % perFold == 0:
                print("Fold {} created.".format(fold))
                fold +=1
                FILEOUT.close()

                # if we are not at last
                if linenum < len(lines):
                    FILEOUT = open(filename+".f"+str(fold),"w")

            
        
        
    FILEIN.close()
    FILEOUT.close()


def main():    
    usage = "usage: %prog [options] FILE"

    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--folds", dest="numFolds",default=10,type="int",
                  help="number of folds (default: 10)")

    (options, args) = parser.parse_args()

    if len(args) == 1:
        folds = options.numFolds
        filename = args[0]
        print("Split file into {} folds.".format(folds))
        
        splitData(filename,folds)
        
    else:
        print("Please provide a CoNLL file!")
        parser.print_help()
        sys.exit(-1)

main()
