#!/usr/bin/python
import re
import gzip
import sys
samples = list()
groups = {}
datalistpath = '/public1/home/yingxm/liupu/liver/steq11_filterSpecies/datalist1'
with open('list_pbs/list%s.txt'%sys.argv[1],'r') as inpf:
    for line in inpf:
        line = line.strip()
        sample,type = line.split(" ")
        samples.append(sample)
        groups[sample] = type
pos2gene = {}
genomes = set()
with open("../keyFiles/all.gene.list.txt",'r') as inpf:
    for line in inpf:
        line = line.strip()
        genome,contig,left,right,gene = line.split("\t")
        genomes.add(genome)
        if pos2gene.get(contig,'null') == 'null':
            pos2gene[contig] = {}
        for i in range(int(left),int(right)+1):
            pos2gene[contig][i] = gene

genomeValidSamples = {}
for genome in genomes:
    datalist = "%s/%s.data.list"%(datalistpath,genome)
    with open(datalist,'r') as inpf:
        for line in inpf:
            line = line.strip()
            sample,type = line.split("\t")
            if genomeValidSamples.get(genome,'null') == 'null':
                genomeValidSamples[genome] = set()
            genomeValidSamples[genome].add(sample)

contig2genome = {}
with open("../keyFiles/genomeInfo.txt",'r') as inpf:
    for line in inpf:
        line = line.strip()
        genome,contig = line.split("\t")[:2]
        contig2genome[contig] = genome
for sample in samples:
    print sample
    oldVcf = "/public1/home/yingxm/liupu/liver/step5_mergeVCF/%s.vcf.gz"%sample
    newVcf = "./SNPs_majorspecies/%s.vcf.gz"%sample
    with gzip.open(newVcf,'w') as vcfOut:
        with gzip.open(oldVcf,'r') as inpf:
            for line in inpf:
               line = line.strip()
               if re.match("#",line):
                   vcfOut.write("%s\n"%line)
                   continue
               tmpArray = line.split("\t")
               freq_bcftools,freq_varscan = tmpArray[-2],tmpArray[-1]
               if float(freq_bcftools)>=0.5 and float(freq_varscan)>=0.5:
                   contig = tmpArray[0]
                   genome = contig2genome[contig]
                   if genome not in genomes:
                       continue
                   vcfOut.write("%s\n"%line)
