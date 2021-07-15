#!/usr/bin/python

import os
import re
from subprocess import Popen, PIPE
import sys

def get_contigs_old(bam):
    print "get contigs of %s..."%bam
    header, err = Popen([samtools,"view","-H",bam], stdout=PIPE, stderr=PIPE).communicate()
    if err != "":
        raise Exception(err)
    # Extract contigs from header and convert contigs to integers
    contigs = {}
    for x in re.findall("@SQ\WSN:(?P<chrom>[A-Za-z0-9_.]*)\WLN:(?P<length>[0-9]+)", header):
        contigs[x[0]] = int(x[1])
    return contigs
def get_contigs_new():
    contigs = {}
    with open('/root/lp/liver/metagenomic_SNP_calling/test/keyFiles/contigs.txt','r') as inpf:
        for line in inpf:
            line = line.strip()
            contig,length = line.split("\t")
            contigs[contig] = int(length)
    return contigs
def coverage(bam, outfile):
    # Check to see if file exists
    if os.path.isfile(bam) == False:
        raise Exception("Bam file does not exist")
    contigs = get_contigs_new()
    with open(outfile,"w") as outpf:
        coverage_dict = {}
        for c in contigs.keys():
            command = "samtools depth -r %s %s | awk '{sum+=$3;cnt++}END{print cnt \"\t\" sum}'" % ( c, bam)
            coverage_dict[c] = {}
            contig_info = Popen(command, stdout=PIPE, shell = True).communicate()[0].strip()
            #print contig_info
	    if(contig_info != ''):
                sites, bases = map(int, contig_info.split("\t"))
                breadth = sites / float(contigs[c])
                depth_hit = bases / float(sites)
                depth_genome = bases / float(contigs[c])
                result = "%s %s %s %s %s %s %s"%(c,breadth,depth_hit,depth_genome,sites,bases,contigs[c])
            else:
                result = "%s 0 0 0" %c
            outpf.write(result)
            outpf.write("\n")

list_no = sys.argv[1]
list_file = "../list%s.txt"%list_no
bamPath = "/root/lp/liver/metagenomic_SNP_calling/test/callSNP/savedBams"
cwd = "/root/lp/liver/metagenomic_SNP_calling/test/species_coverage"

if __name__ == '__main__':
    with open(list_file,"r") as inpf:
        for line in inpf:
            line = line.strip()
            if re.match("#",line):
                continue
            sample,type = line.split("\t")
            line = sample
            bamfile = "%s/%s.uniq.sorted.picard.bam"%(bamPath,line)
            print 'samtools index...'
            sm_command = "samtools index %s"%( bamfile)
            os.system(sm_command)
            print "caculate uniq coverage..."
            coverage(bamfile, "%s/%s.coverage.txt"%(cwd,line))
