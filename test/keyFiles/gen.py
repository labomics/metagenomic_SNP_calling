#!/usr/bin/python
import glob
import gzip
import re
genomes = []
with open('genomes.list','r') as inpf:
    for line in inpf:
        line = line.strip()
        genomes.append(line)

fnaPath = '/root/lp/liver/metagenomic_SNP_calling/test/ref/fna'
for genome in genomes:
    fna = glob.glob('%s/%s*'%(fnaPath,genome))[0]
    with gzip.open(fna,'r') as inpf:
        for line in inpf:
            line = line.strip()
            if re.match('>',line):
                contig = line.split(' ')[0]
                contig = contig.replace('>','')
                des = ' '.join(line.split(' ')[1:])
                print '%s\t%s\t%s'%(genome,contig,des)


