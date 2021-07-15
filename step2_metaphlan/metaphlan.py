#!/usr/bin/python
import sys
import os
import re

list_file = "../list1.txt"
#metaphlan_dir = "/root/lp/liver/software/biobakery-metaphlan2-f1dcf3958459"
#out_dir = "./"
#fastq_dir = "/root/lp/liver/metagenomic_SNP_calling/test"

metaphlan_dir = sys.argv[1]
out_dir = sys.argv[2]
fastq_dir = sys.argv[3]
with open(list_file,"r") as inpf:
    for line in inpf:
        line = line.strip()
        if(re.match("#",line)):
            continue
        sample,type = line.split('\t')
        line = sample
        file1 = "%s_1P.fq.gz"%line
        file2 = "%s_2P.fq.gz"%line
        print("processing %s..."%line)
        command = "bash -c 'python %s/metaphlan2.py --input_type fastq --nproc 6 --mpa_pkl %s/db_v20/mpa_v20_m200.pkl --bowtie2db  %s/db_v20/mpa_v20_m200 --bowtie2out %s/%s.bowtie2out.txt  < <(zcat %s/%s  %s/%s) > %s/%s.result.txt' " %(metaphlan_dir, metaphlan_dir, metaphlan_dir, out_dir, line, fastq_dir, file1, fastq_dir, file2, out_dir, line)
        os.system(command)


                


