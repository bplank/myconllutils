import sys
class Conll07Reader:
    ### read Conll 2007 data
    ### http://nextens.uvt.nl/depparse-wiki/DataFormat

    def __init__(self,filename):
        self.filename = filename
        self.startReading()

    def startReading(self):
        self.FILE = open(self.filename,"r")

    def getNext(self):
        # return next instance or None

        line = self.FILE.readline()

        line = line.strip()
        lineList = line.split("\t")

        ids = []
        form = []
        lemma = []
        cpos = []
        pos = []
        feats = []
        head = []
        deprel = []
        phead = []
        pdeprel = []

        if len(lineList) == 10:
            # contains all cols, also phead/pdeprel
            while len(lineList) == 10:
                ids.append(int(lineList[0]))
                form.append(lineList[1])
                lemma.append(lineList[2])
                cpos.append(lineList[3])
                pos.append(lineList[4])
                feats.append(lineList[5])
                head.append(int(lineList[6]))
                deprel.append(lineList[7])
                phead.append(lineList[8])
                pdeprel.append(lineList[9])

                line = self.FILE.readline()
                line = line.strip()
                lineList = line.split("\t")
        elif len(lineList) == 8:
            while len(lineList) == 8:
                ids.append(lineList[0])
                form.append(lineList[1])
                lemma.append(lineList[2])
                cpos.append(lineList[3])
                pos.append(lineList[4])
                feats.append(lineList[5])
                head.append(int(lineList[6]))
                deprel.append(lineList[7])
                phead.append("_")
                pdeprel.append("_")

                line = self.FILE.readline()
                line = line.strip()
                lineList = line.split("\t")
        elif len(lineList) > 1:
            raise Exception("not in right format!")


        if len(form) > 0: 
            return DependencyInstance(ids,form,lemma,cpos,pos,feats,head,deprel,phead,pdeprel)
        else: 
            return None


    def getInstances(self):
        instance = self.getNext()

        instances = []
        while instance:
            instances.append(instance)

            instance = self.getNext()
        return instances 

    def getSentences(self):
        """ return sentences as list of lists """
        instances = self.getInstances()
        sents = []
        for i in instances:
            sents.append(i.form)
        return sents

   


class DependencyInstance:
    
    def __init__(self, ids, form, lemma, cpos, pos, feats, headid, deprel, phead, pdeprel):
        self.ids = ids
        self.form = form
        self.lemma = lemma
        self.cpos = cpos
        self.pos = pos
        self.feats = feats
        self.headid = headid
        self.deprel = deprel
        self.phead = phead
        self.pdeprel = pdeprel       
        
    def __str__(self):
        s = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\n"
        sout = ""
        for i in range(len(self.form)):
            sout += s.format(self.ids[i],self.form[i],self.lemma[i],self.cpos[i],self.pos[i],self.feats[i],self.headid[i],self.deprel[i],self.phead[i],self.pdeprel[i])
        return sout

    def __repr__(self):
        return self.__str__()

    def equalForm(self,instance):
        for f1,f2 in zip(self.form,instance.form):
            if f1 != f2:
#            if f1 != "<num>" and f2 != "<num>" and f1 != f2:
                return False
        return True
    
    def equalHeads(self,instance):
        for f1,f2 in zip(self.headid,instance.headid):
            if f1 != f2:
                return False
        return True

    def equalLabels(self,instance):
        for f1,f2 in zip(self.deprel,instance.deprel):
            if f1 != f2:
                return False
        return True

    def equalHeadsAndLabels(self,instance):
        return self.equalHeads(instance) and self.equalLabels(instance)
    
    def getSentenceLength(self):
        return len(self.form)

    def getSentence(self):
        return self.form

    def getLemmaTriples(self):
        return self.getTriples(self.lemma)

    def getFormTriples(self):
        return self.getTriples(self.form)

    def getTriples(self,wordform):
        triples = {}
        for i in range(len(wordform)):
            r = self.deprel[i]
            w_d = wordform[i].replace(" ","")
            hid = self.headid[i]
            if hid != 0:
                w_h = wordform[hid-1].replace(" ","")
            else:
                w_h = '<root-LEMMA>'
            triple = "{} {} {}".format(r,w_h,w_d)
            triples[triple] = triples.get(triple,0) + 1
        #triples = self._addExtendedTriples(triples,wordform)
        return triples

    # def _addExtendedTriples(self,triples,wordform):
    #     """ add r(A,C) for every triple r(A,B) prep(B,C) """
    #     """ e.g. comp(centinaia,di) + prep(di,feriti) => comp(centinaia,feriti) """
    #     for i in range(len(wordform)):
    #         r = self.deprel[i]
    #         w_C = wordform[i].replace(" ","")
    #         hid = self.headid[i]-1 
    #         if hid != 0:
    #             w_B = wordform[hid].replace(" ","")
    #         else:
    #             w_B = '<root-LEMMA>!'
    #         if r == "prep" and hid != 0:
    #             hid_B = self.headid[hid]-1
    #             w_A = wordform[hid_B].replace(" ","")
    #             r_new = self.deprel[hid]
    #             triple = "{} {} {}".format(r_new,w_A,w_C)
    #             triples[triple] = triples.get(triple,0) + 1

    #     #TODO
    #     """ add r(A,C) for every pair of dependecy triples r(A,B) cnj(B,C) """
    #    return triples

    def getAllLemmaTriples(self):
        return self.getAllTriples(self.lemma)

    def getAllFormTriples(self):
        return self.getAllTriples(self.form)

    def getAllTriples(self,wordform):
        """ also returns counts of parts of relation """
        triples = self.getTriples(wordform)
        actualtriples = triples.copy()
        for triple in actualtriples:
            try:
                r,w_h,w_d = triple.split(" ")

                #triple_r_w1 = "{} {} _".format(r,w_h)
                triple_r_w1 = "{} {}  ".format(r,w_h)
                triples[triple_r_w1] = triples.get(triple_r_w1,0) + 1

                # Gertjan
                #triple_w2 = "_ _ {}".format(w_d)
                #triples[triple_w2] = triples.get(triple_w2,0) + 1

                #triple_w2x = "{} _ {}".format(r,w_d)
                triple_w2x = "{}   {}".format(r,w_d)
                triples[triple_w2x] = triples.get(triple_w2x,0) + 1

                # Lin:
                #triple_r = "{} _ _".format(r)
                #triples[triple_r] = triples.get(triple_r,0) +1

            except ValueError:
                print("Error when splitting triples: {}".format(triple))
                sys.exit(-1)
        return triples



