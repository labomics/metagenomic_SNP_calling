#!/usr/bin/python
import gzip
import re
import sys
import os

samtoolsVcf = "/root/data/liver/downsample/step4_filtersam"
varscanVcf = "/root/data/liver/downsample/step3_vsoutput"

outpath = 'step5_merge'
if not os.path.exists(outpath):
    os.mkdir(outpath)

listfile = "list%s.txt"%sys.argv[1]
with open(listfile,'r') as inpf:
    for line in inpf:
        line = line.strip()
        sample = line
        samvcf = "%s/%s.vcf.gz"%(samtoolsVcf,sample)
        varvcf = "%s/%s.vcf.gz"%(varscanVcf,sample)
        set1 = set()
        set3 = set()
        samFreq = {}
        varFreq = {}
        ntFreq = {}
        print sample
        with gzip.open(samvcf,'r') as inpf2:
            for line2 in inpf2:
                line2 = line2.strip()
                if re.match("#",line2):
                    continue
                tmpArray = line2.split("\t")
                contig = tmpArray[0]
                ref_f,ref_r,alt_f,alt_r = re.search('DP4=(\d+),(\d+),(\d+),(\d+)',line2).groups()
                altReads = int(alt_f) + int(alt_r)
                totalReads = int(ref_f) + int(ref_r) + altReads
                if altReads < 4:
                    continue
                strandBias = float(alt_f)/altReads
                if strandBias < 0.1 or strandBias > 0.9:
                    continue
                DPR = tmpArray[-1].split(":")[-1].split(",")
                DPR = [int(x) for x in DPR]
                freq = float(max(DPR[1:]))/sum(DPR)
                pos = tmpArray[1]
                iden = "%s_%s"%(contig,pos)
                set1.add(iden)
                samFreq[iden] = freq

        tmpVarfreq = {}
        tmpVarBias = {}
        tmpVarBiasArray = {}
        tmpVarReads2 = {}
        tmpVaridens = set()
        print 'read var file'
        with gzip.open(varvcf,'r') as inpf3:
            for line3 in inpf3:
                line3 = line3.strip()
                if re.match("Chrom",line3):
                    continue
                tmpArray = line3.split("\t")
                contig = tmpArray[0]
                pos = int(tmpArray[1])
                iden = "%s_%s"%(contig,pos)
                tmpVaridens.add(iden)
                reads2plus = int(tmpArray[-3])
                reads2minus = int(tmpArray[-2])
                reads2 = int(tmpArray[5])
                freq = float(tmpArray[6].replace("%",""))/100
                if tmpVarfreq.get(iden,'null') == 'null':
                    tmpVarfreq[iden] = freq
                    tmpVarBias[iden] = float(reads2plus)/(int(reads2plus)+int(reads2minus))
                    tmpVarBiasArray[iden] = [reads2plus, reads2minus]
                    tmpVarReads2[iden] = reads2
                else:
                    if tmpVarfreq[iden] < freq:
                        tmpVarfreq[iden] = freq
                    reads2plus += tmpVarBiasArray[iden][0]
                    reads2minus += tmpVarBiasArray[iden][1]
                    tmpVarBias[iden] = float(reads2plus)/(int(reads2plus)+int(reads2minus))
                    tmpVarBiasArray[iden] = [reads2plus, reads2minus]
                    tmpVarReads2[iden] += reads2
        print 'filter var'
        for iden in tmpVaridens:
            if tmpVarBias[iden] < 0.1 or tmpVarBias[iden] > 0.9:
                continue
            if tmpVarfreq[iden] < 0.2:
                continue
            if tmpVarReads2[iden] < 4:
                continue
            if iden in set1:
                set3.add(iden)
        varFreq = tmpVarfreq

        samFormat = "./step5_merge/%s.vcf.gz"%(sample)
        print "%s sam"%sample
        with gzip.open(samFormat,'w') as outpf:
            with gzip.open(samvcf,'r') as inpf2:
                for line2 in inpf2:
                    line2 = line2.strip()
                    if re.match("#",line2):
                        outpf.write("%s\n"%line2)
                        continue
                    tmpArray = line2.split("\t")
                    contig = tmpArray[0]
                    pos = tmpArray[1]
                    iden = "%s_%s"%(contig,pos)
                    if iden in set3:
                        outpf.write("%s\t%s\t%s\n"%(line2,samFreq[iden],varFreq[iden]))
        with open('./step5_merge/%s.result.txt'%sample,'w') as outpf:
            for iden in set3:
                outpf.write("%s\t%s\t%s\n"%(iden,samFreq[iden],varFreq[iden]))




