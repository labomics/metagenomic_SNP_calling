#!/usr/bin/python
import re
import sys
snpInfoPath = "./snpNum"
coverageInfoPath = "/public1/home/yingxm/liupu/liver/step5_species_coverage/genomeCoverage"
listPath = "../datalist"
density_table = dict()
allsamples = list()
genomeSet = set()
with open("../keyFiles/data.list","r") as inpf:
    for line in inpf:
        line = line.strip()
        sample = line.split("\t")[0]
        allsamples.append(sample)
        snpInfo = "%s/%s.result.txt"%(snpInfoPath,sample)
        genome_snpCount = dict()
        with open(snpInfo,"r") as inpf2:
            for line2 in inpf2:
                line2 = line2.strip()
                genome, snpCount = line2.split("\t")[:2]
                genome_snpCount[genome] = snpCount
                genomeSet.add(genome)
        coverageInfo = "%s/%s.coverage.txt"%(coverageInfoPath,sample)
        with open(coverageInfo,"r") as inpf3:
            for line3 in inpf3:
                if re.match("#",line3):
                    continue
                line3 = line3.strip()
                array = line3.split(" ")
                genome,sites = array[0],array[3]
                density = float(genome_snpCount.get(genome,0))/float(sites)
                #if genome not in density_table.keys():
                if density_table.get(genome,'null') == 'null':
                    density_table[genome] = dict()
                density_table[genome][sample] = density
#for genome in density_table.keys():
for genome in genomeSet:
    datalist = "%s/%s.data.list"%(listPath,genome)
    sampleSet=  set()
    with open(datalist,'r') as inpf:
        for line in inpf:
            line = line.strip()
            sample,type = line.split("\t")
            sampleSet.add(sample)
    print genome,
    for sample in allsamples:
        if sample not in sampleSet:
            print -1,
        else:
            #if sample in density_table[genome].keys():
            if density_table[genome].get(sample, 'null') == 'null':
                print 0,
            else:
                print density_table[genome][sample],
    print ""
