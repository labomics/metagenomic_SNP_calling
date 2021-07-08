#coding=utf-8
#########################################################################
# File Name: varscan.py
#########################################################################

#!/usr/bin/python
import os
import sys
bam_path = "/root/data/liver/savedBams"
varscan_path = "/root/data/liver/software"
picard_path = "/root/data/liver/software/picard-tools-1.119"
ref = "/root/data/liver/step5_ref/allRef.fna"
listNo = sys.argv[1]
with open('list%s.txt'%listNo,'r') as inpf:
    for line in inpf:
        line = line.strip()
        sample = line
        bam = "%s/%s.uniq.sorted.picard.bam"%(bam_path,sample)
        command1 = "samtools mpileup -f %s %s > step2_output/%s.mpileup" %(ref,bam,sample)
        command2 = "java -jar %s/VarScan.v2.3.9.jar pileup2snp step2_output/%s.mpileup --min-coverage 10 \
        --p-value 0.05 --min-avg-qual 15 --min-reads2 4 --min-var-freq 0.2 |gzip -c > step2_output/%s.vcf.gz"%(varscan_path,sample,sample)
        command3 = "rm step2_output/%s.mpileup"%sample
        print(command1)
        os.system(command1)
        print(command2)
        os.system(command2)
        print(command3)
        os.system(command3)

