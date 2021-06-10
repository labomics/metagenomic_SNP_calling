#!/usr/bin/python
import sys
import gzip
import re
import numpy as np
def getFilterPos(input):
    
    bigTable = dict()
    if re.search("gz$",input):
        myopen = gzip.open
    else:
        myopen = open
    seqLength = 100000

    with myopen(input,"r") as inpf:
        tmpflag = 0
        for line in inpf:
            tmpflag += 1
            line = inpf.next()
            line = line.strip()
            if len(line) < seqLength:
                seqLength = len(line)

            if tmpflag == 1:
               for i in range(len(line)):
                   bigTable[i] = dict()
                   for base in 'ATGCN':
                       bigTable[i][base] = 0

            i = 0
            try:
                for base in line:
                    if bigTable.get(i,'null') == 'null':
                        bigTable[i] = dict()
                    #bigTable[i][base] += 1
                    bigTable[i][base] = bigTable[i].get(base,0) + 1
                    i += 1
            except  Exception,e:
                print line
                print e
                print 'File error!! Detect something strange in fastq file, please check it'
                exit()
            line = inpf.next()
            line = inpf.next()
    #print(bigTable)
    
    upLimit = dict()
    lowLimmit = dict()
    for base in ['A','T','G','C']:
        curList = list()
        #for pos in bigTable.keys():
        for pos in range(seqLength):
            curList.append(bigTable[pos].get(base,0))
        arr = np.array(curList)
        aver = arr.mean()
        std = arr.std()
        upL = aver+std*2
        lowL = aver-std*2
        upLimit[base] = upL
        lowLimmit[base] = lowL
    #for pos in bigTable.keys():
    for pos in range(seqLength):
        curDict = bigTable[pos]
        flag = 1
        for base in ['A','T','G','C']:
            if curDict[base] > upLimit[base] or curDict[base] < lowLimmit[base]:
                flag = 0
                print "%s %s %s %s %s"%(pos, base, curDict[base], upLimit[base],
                        lowLimmit[base])
        if flag == 1:
            print pos
            return pos
            break
if __name__ == '__main__':
    getFilterPos(sys.argv[1])
