#!/usr/bin/python
#python getStrain.py result/ >mappedstrain.txt
import sys
import glob
import re

inpf = open("./species_name_bigger_than_3one.txt","r")
bigdict = dict()
for line in inpf:
    line = line.strip()
    bigdict[line] = dict()

inpf.close()
path = sys.argv[1]
filename = glob.glob(path+"/*.result.txt")
for file in filename:
    inpf = open(file,"r")
    scoredict = dict()
    for line in inpf:
        if re.match("#",line):
            continue
        line = line.strip()
        lastname = line.split("\t")[0].split("|")[-1]
        score = line.split("\t")[-1]
        if re.match("t__",lastname):
            speciesname = line.split("\t")[0].split("|")[-2]
            if not re.match("s__",speciesname):
                continue
            lastname = lastname.replace("t__","")
            speciesname = speciesname.replace("s__","")
            if speciesname in bigdict.keys():
                if speciesname not in scoredict.keys():
                    scoredict[speciesname] = dict()
                    scoredict[speciesname]["score"] = score
                    scoredict[speciesname]["strain"] = lastname
                else:
                    if scoredict[speciesname]["score"] < score:
                        scoredict[speciesname]["score"] = score
                        scoredict[speciesname]["strain"] = lastname
    for key in scoredict.keys():
        if not bigdict[key]=={}:
            if scoredict[key]["strain"] in bigdict[key].keys():
                bigdict[key][scoredict[key]["strain"]] += 1
            else:
                bigdict[key][scoredict[key]["strain"]] = 1
        else:
            bigdict[key][scoredict[key]["strain"]] = 1
    inpf.close()
print bigdict

for key in bigdict.keys():
#    print key
    print key+"\t",
    if not bigdict[key] == {}:
        tmp = sorted(bigdict[key].items(),lambda x,y:cmp(x[1],y[1]),reverse=True)
        print tmp[0][0]
        #print tmp
    else:
        print key




 







