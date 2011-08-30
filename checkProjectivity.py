#!/usr/bin/python3

""" 
Author: Barbara Plank
Date:   July 27, 2011

Description: Check projectivity of dependency trees in CoNLL file 
(% of sentences and relations)

"""
import sys

if len(sys.argv) != 2:
    print("Error: specify a CoNLL file!\nUsage: {0} {1}".format(sys.argv[0],"FILE"))
else:
    filename = sys.argv[1]
    FILE = open(filename,"r")
        
    instance = {}
    wordid=1
    instances = []

    while True:
        l = FILE.readline()
        if not l:
            break

        l = l.strip()
        lineList = l.split("\t")
       
        if len(lineList) > 1:
            instance[wordid] = int(lineList[6])
            wordid = wordid+1
        else:
            instances.append(instance)
            instance = {}
            wordid=1


    countProjective=0
    countNonProjective=0
    
    countProjectiveRelation=0
    countNonProjectiveRelation=0

    for instance in instances:
        isProjective=True
        pos=0
        wordid=pos+1
        #print("instance: {}".format(instance))

        for edge in instance:
            i = instance[edge]
            j = edge

            if j < i:
                i,j=j,i
            for k in range(i+1,j):
                headk = instance[k]
                if i <= headk <= j or j <= headk <= i:
                    projEdge = True
                    countProjectiveRelation+=1
                else:
                    #print("non-projective")
                    #print("{} <= {} <= {} ? ".format(i,headk,j))
                    isProjective=False
                    countNonProjectiveRelation+=1
                    
                
        if isProjective:
            countProjective+=1
        else:
            countNonProjective+=1

    print("============= Summary =================")
    print("** Sentences: **")
    print("num projective: {} (sentences)".format(countProjective))
    print("num non-projec: {}".format(countNonProjective))
    print("Non-projective: {}%".format(countNonProjective/(countProjective+countNonProjective)*100))
    print("** Relations: **")
    print("num projective: {} (from all relations, also non-scoring)".format(countProjectiveRelation))
    print("num non-projec: {}".format(countNonProjectiveRelation))
    print("Non-projective: {}%".format(countNonProjectiveRelation/(countProjectiveRelation+countNonProjectiveRelation)*100))
