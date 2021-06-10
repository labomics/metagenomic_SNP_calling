
#!/usr/bin/python
import sys
import os
import re

index_path = "/root/data/liver/step5_ref/allRef.fna.gz"
fa_index = "/root/data/liver/step5_ref/allRef.fna"
savedBam = "/root/data/liver/savedBams"
picard_path = "/root/data/liver/software/picard-tools-1.119"
dataPath = '/root/data/liupu/liver/step1_classifyData/filteredData'

list_no  = sys.argv[1]
list_file = "list%s.txt"%list_no

outpath = 'output'
if not os.path.exists(outpath):
    os.mkdir(outpath)
outpath1 = 'savedBams'
if not os.path.exists(outpath1):
    os.mkdir(outpath1)

with open(list_file,"r") as inpf:
    for line in inpf:
        line = line.strip()
        if re.match("#",line):
            continue
        line = line.split("\t")[0]
        file1 = "%s/%s_1P.fq.gz"%(dataPath, line)
        file2 = "%s/%s_2P.fq.gz"%(dataPath, line)
        print("processing %s..."%line)
        bwa_command = "bwa  mem -t 24 -M -R \'@RG\\tID:%s\\tSM:%s\\tLB:library1\' %s %s %s > step2_output/%s.sam" %(line, line, index_path, file1, file2, line)
        #for uniq mapping
        samtools_command0 = "samtools view -q 1 -bS step2_output/%s.sam -o \
        step2_output/%s.uniq.bam"%(line,line)

        samtools_command2 = "samtools sort -m 1000M -o step2_output/%s.uniq.sorted.bam -T %s.sorted step2_output/%s.uniq.bam" %(line, line, line)

        bamfile = "step2_output/%s.uniq.sorted.bam"%line

        picard_command = "java -Xmx16g -jar %s/MarkDuplicates.jar \
        TMP_DIR=/root/data/liver/step6_callSNP/TMP \
        MAX_FILE_HANDLES_FOR_READ_ENDS_MAP=500  VALIDATION_STRINGENCY=LENIENT REMOVE_DUPLICATES=TRUE \
        INPUT=%s OUTPUT=step2_output/%s.uniq.sorted.picard.bam METRICS_FILE=step2_output/%s_metrics.txt" %(picard_path, bamfile, line, line)
        samtools_command5 = "samtools mpileup -ugf %s -t DP,DPR  %s | bcftools call -vmO z -V\
        indels -o step2_output/%s.vcf.gz"%(fa_index,"step2_output/%s.uniq.sorted.picard.bam"%line,line)
        deleteCommand = "mv step2_output/%s.uniq.sorted.picard.bam step2_savedBams/; mv step2_output/%s.vcf.gz step2_savedBams; rm  step2_output/%s.*"%(line,line,line)
        samtools_command3 = "samtools index step2_savedBams/%s.uniq.sorted.picard.bam"%line
        print(bwa_command)
        os.system(bwa_command)
        print(samtools_command0)
        os.system(samtools_command0)
        print(samtools_command2)
        os.system(samtools_command2)
        print(picard_command)
        os.system(picard_command)
        print(samtools_command5)
        os.system(samtools_command5)
        print(deleteCommand)
        os.system(deleteCommand)
        print(samtools_command3)
        os.system(samtools_command3)
