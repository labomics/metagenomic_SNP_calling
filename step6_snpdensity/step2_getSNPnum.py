#!/usr/bin/python
import gzip
import re
import sys
import os
samtoolsVcf = "../step5_mergeVCF/SNPs_majorspecies/"
if not os.path.exists(samtoolsVcf):
    print 'not found path'
    exit()
species_set = set()
parent = dict()
with open("../keyFiles/fitSpecies",'r') as inpf:
    for line in inpf:
        species_set.add(line.split(" ")[0])
with open("../keyFiles/genomeInfo.txt",'r') as inpf:
    for line in inpf:
        line = line.strip()
        genome,contig = line.split("\t")[:2]
        parent[contig] = genome
with open("../keyFiles/data.list",'r') as inpf:
    for line in inpf:
        line = line.strip()
        sample,type = line.split("\t")
        vcfFile = "%s/%s.vcf.gz"%(samtoolsVcf,sample)
        result = dict()
        with gzip.open(vcfFile,'r') as inpf2:
            for line2 in inpf2:
                line2 = line2.strip()
                if re.match("#",line2):
                    continue
                tmpArray = line2.split("\t")
                contig = tmpArray[0]
                genome = parent[contig]
                result[genome] = result.get(genome,0) + 1
        outPath = "snpNum1"
        if not os.path.exists(outPath):
            os.mkdir(outPath)
        outfile = "%s/%s.result.txt"%(outPath,sample)
        with open(outfile,'w') as outpf:
            for sp in result.keys():
                outpf.write("%s\t%s\n"%(sp,result.get(sp,0)))
        print sample
    

