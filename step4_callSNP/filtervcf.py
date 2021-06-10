#########################################################################
# File Name: filtervcf.py
#########################################################################
#!/usr/bin/python
from __future__ import division
import gzip
import re
import glob
import sys
import os

outpath = 'step4_filtersam'
if not os.path.exists(outpath):
    os.mkdir(outpath)

vcfannotate = "/root/data/software/vcftools-vcftools-581c231/src/perl/vcf-annotate"
rawVcfPath = "/root/data/liver/step2_savedBams"
newVcfPath = "/root/data/liver/step4_filtersam"
listFile = "list%s.txt"%sys.argv[1]

def freqFilter(sraID):
    file = "%s/%s.dp.vcf.gz"%(newVcfPath, sraID)
    outfile = "%s/%s.vcf.gz"%(newVcfPath, sraID)
    with gzip.open(outfile,"w") as outpf:
        with gzip.open(file,"r") as inpf:
            for line in inpf:
                line = line.strip()
                if re.match("#",line):
                    outpf.write(line+"\n")
                    continue
                array = line.split("\t")
                info = array[7]
                dp = 0
                alt = 0
                for item in info.split(";"):
                    if re.match("DP=",item):
                        dp = int(item.split("=")[1])
                    if re.match("DP4=",item):
                        dp4_array = item.split("=")[1].split(",")
                        alt = int(dp4_array[2])+int(dp4_array[3])
                        if alt/dp >= 0.2:
                            outpf.write(line+"\n")



def dpFilter(sraID):
    file = "%s/%s.vcf.gz"%(rawVcfPath, sraID)
    outfile = "%s/%s.dp.vcf.gz"%(newVcfPath, sraID)
    command = "zcat %s | %s -H -f +/d=10/a=4/Q=15/q=10/ | gzip -c > %s" %(file,vcfannotate, outfile)
    os.system(command)


with open(listFile,"r") as inpf:
    for line in inpf:
        line = line.strip()
        sample = line
        dpFilter(sample)
        freqFilter(sample)

