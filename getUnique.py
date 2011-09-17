#!/usr/bin/python3

""" 
Author: Barbara Plank
Date:   September 2011

Description: Extract unique sentences from a CoNLL file

"""
import sys
from conll.Conll07Reader import Conll07Reader
from optparse import OptionParser

def main():
    usage = "usage: %prog FILE"

    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()

    if len(args) < 1:
        print("Argument missing!")
        parser.print_help()
        exit(-1)
    
    file1 = args[0]

    reader1 = Conll07Reader(file1)

    instances1 = reader1.getInstances()

    sents = {} 
    
    for i in instances1:
        s = " ".join(i.getSentence())
        if not s in sents:
            sents[s] = s
            print(i)

main()
