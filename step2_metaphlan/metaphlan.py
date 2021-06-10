#!/usr/bin/python
import sys
import os
import re
f_num = sys.argv[1]
list_file = "list%s.txt"%f_num
with open(list_file,"r") as inpf:
    for line in inpf:
        line = line.strip()
        if(re.match("#",line)):
            continue
        sample,type = line.split('\t')
        line = sample
        file1 = "%s_1P.fq.gz"%line
        file2 = "%s_2P.fq.gz"%line
        print "processing %s..."%line
        metaphlan_dir = "/public1/home/yingxm/liupu/liver/software/biobakery-metaphlan2-f1dcf3958459"
        out_dir = "/public1/home/yingxm/liupu/liver/step3_metaphlan2/result"
        fastq_dir = "/public1/home/yingxm/liupu/liver/step1_classifyData/filteredData1"
        command = "export PATH=/export/home/yingxm/bin/:$PATH && /bin/bash -c '/export/python/bin/python2.7  %s/metaphlan2.py --input_type fastq --nproc 6 --mpa_pkl %s/db_v20/mpa_v20_m200.pkl --bowtie2db  %s/db_v20/mpa_v20_m200 --bowtie2out %s/%s.bowtie2out.txt  <(zcat %s/%s  %s/%s) > %s/%s.result.txt' " %(metaphlan_dir, metaphlan_dir, metaphlan_dir, out_dir, line, fastq_dir, file1, fastq_dir, file2, out_dir, line)
        os.system(command)


                


