#!/usr/bin/python
#python getGCForPRJ.py > mappedGCForPRJ.txt
#change name to getAllGCFid.py
import subprocess
import os
import re
inpf = open("./mappedstrains.txt","r")
for line in inpf:
    line = line.strip()
    line = line.split("\t")[1]
    line2 = line.replace("_unclassified","")
#    p = subprocess.Popen("grep "+line+" ./taxonomy.txt", shell=True,)
    if re.match("GC",line2) or re.match("PRJ",line2):
        print line+"\t"+line2
    else:
        p = os.popen("grep "+line2+"\| ./taxonomy.txt").readlines()
        str = p[0]
        strain = p[0].split("|")[-1].replace("t__","")
        strain = strain.strip()
        print line+"\t"+strain
inpf.close()
