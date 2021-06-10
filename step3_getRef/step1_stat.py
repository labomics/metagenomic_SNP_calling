#!/usr/bin/python
#python stat.py result/ >species.txt
import re
import sys
import glob

def onefile(path,level):
    IN = open(path,"r")
    prefix = level+"__"
    result1 = dict()
    for line in IN:
        if re.match("#",line):
            continue
        line = line.strip()
        lastname = line.split("\t")[0].split("|")[-1]
        score = line.split("\t")[-1]
        if re.match(prefix,lastname):
            species = lastname.replace(prefix,"")
            result1[species] = score
#	    print species
        else:
            continue
    return result1


if __name__ == "__main__":
    path = sys.argv[1]
    filename = glob.glob(path+"/*.result.txt")
    collection = []
    for file in filename:
        #print file
        file = file.strip()
        result1 = onefile(file,"s")
        collection += result1.keys()
    count = dict()
    for item in collection:
        if item in count.keys():
            count[item] += 1
        else:
            count[item] = 1
    
    count2 = sorted(count.items(),lambda x,y:cmp(x[1],y[1]),reverse=True)
    for i in range(0,len(count2)):
            print count2[i][0],"\t",count2[i][1]



