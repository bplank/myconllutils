#!/usr/bin/python3

""" 
Author: Barbara Plank
Date:   August 2011

Description: This script extracts sentences from a CoNLL file
of specific length

Options: specify minimun and maximum sentence length to extract

"""
import sys
from conll.Conll07Reader import Conll07Reader
from optparse import OptionParser

def main():
    usage = "usage: %prog [options] FILE"

    parser = OptionParser(usage=usage)
    parser.add_option("--minLen", dest="minLen",default=0,type="int",
                  help="extract sentences that have a minimum length")
    parser.add_option("--maxLen", dest="maxLen",
                  help="extract sentences up to this length",type="int")


    (options, args) = parser.parse_args()

    if len(args) < 1:
        print("Argument missing!")
        parser.print_help()
        exit(-1)
    
    file1 = args[0]

    reader1 = Conll07Reader(file1)

    instances1 = reader1.getInstances()
    
    for i in instances1:
        if i.getSentenceLength() > options.minLen:
            if options.maxLen and i.getSentenceLength() <= options.maxLen:
                print(i)
            else:
                print(i)

main()
