#coding=utf-8
#########################################################################
# File Name: varscan.py
#########################################################################

#!/usr/bin/python
import os
import sys
bam_path = "/root/lp/liver/metagenomic_SNP_calling/test/callSNP/savedBams"
varscan_path = "/root/lp/liver/software"
ref = "/root/lp/liver/metagenomic_SNP_calling/test/ref/Ref.fna"
output = "/root/lp/liver/metagenomic_SNP_calling/test/callSNP/voutput"
listNo = sys.argv[1]

with open('../list%s.txt'%listNo,'r') as inpf:
    for line in inpf:
        line = line.strip()
        sample = line.split("\t")[0]
        bam = "%s/%s.uniq.sorted.picard.bam"%(bam_path,sample)
        command1 = "samtools mpileup -f %s %s > %s/%s.mpileup" %(ref,bam,output,sample)
        command2 = "java -jar %s/VarScan.v2.3.9.jar pileup2snp %s/%s.mpileup --min-coverage 10 \
        --p-value 0.05 --min-avg-qual 15 --min-reads2 4 --min-var-freq 0.2 |gzip -c > %s/%s.vcf.gz"%(varscan_path,output,sample,output,sample)
        command3 = "rm %s/%s.mpileup"%(output,sample)
        print(command1)
        os.system(command1)
        print(command2)
        os.system(command2)
        print(command3)
        os.system(command3)

