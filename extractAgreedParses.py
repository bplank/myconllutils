#!/usr/bin/python3

""" 
Author: Barbara Plank
Date:   August 2011

Description: Given two CoNLL 2007 files, this script extracts the
dependency parses the two systems agree upon.

Options: specify minimun and maximum sentence length to extract

"""
import sys
from conll import Conll07Reader
from optparse import OptionParser

def main():
    usage = "usage: %prog [options] FILE1 FILE2"

    parser = OptionParser(usage=usage)
    parser.add_option("--minLen", dest="minLen",default=0,type="int",
                  help="extract sentences that have a minimum length")
    parser.add_option("--maxLen", dest="maxLen",
                  help="extract sentences up to this length",type="int")


    (options, args) = parser.parse_args()

    if len(args) < 2:
        print("Arguments missing!")
        parser.print_help()
        exit(-1)
    
    file1 = args[0]
    file2 = args[1]

    reader1 = Conll07Reader(file1)
    reader2 = Conll07Reader(file2)

    instances1 = reader1.getInstances()
    instances2 = reader2.getInstances()
    
    for i in instances1:
        if i.getSentenceLength() > options.minLen:
            for j in instances2:
                if not i.equalForm(j):
                    continue
                elif i.equalHeadsAndLabels(j):
                    if options.maxLen:
                        if i.getSentenceLength() <= options.maxLen:
                            print(i)
                    else:
                        print(i)
                    break
                
 
main()
