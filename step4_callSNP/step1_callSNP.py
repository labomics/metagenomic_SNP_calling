
#!/usr/bin/python
import sys
import os
import re

index_path = "/root/lp/liver/metagenomic_SNP_calling/test/ref/Ref.fna.gz"
fa_index = "/root/lp/liver/metagenomic_SNP_calling/test/ref/Ref.fna"
savedBam = "/root/lp/liver/metagenomic_SNP_calling/test/callSNP/savedBams"
output = "/root/lp/liver/metagenomic_SNP_calling/test/callSNP/output"
picard_path = "/root/lp/liver/software/picard-tools-1.119"
dataPath = '/root/lp/liver/metagenomic_SNP_calling/test/clean_data'

list_no  = sys.argv[1]
list_file = "../list%s.txt"%list_no


with open(list_file,"r") as inpf:
    for line in inpf:
        line = line.strip()
        if re.match("#",line):
            continue
        line = line.split("\t")[0]
        file1 = "%s/%s_1P.fq.gz"%(dataPath, line)
        file2 = "%s/%s_2P.fq.gz"%(dataPath, line)
        print("processing %s..."%line)
        bwa_command = "bwa  mem -t 24 -M -R \'@RG\\tID:%s\\tSM:%s\\tLB:library1\' %s %s %s > %s/%s.sam" %(line, line, index_path, file1, file2, output, line)
        #for uniq mapping
        samtools_command0 = "samtools view -q 1 -bS %s/%s.sam -o \
        %s/%s.uniq.bam"%(output,line,output,line)

        samtools_command2 = "samtools sort -m 1000M -o %s/%s.uniq.sorted.bam -T %s.sorted %s/%s.uniq.bam" %(output, line, line, output, line)

        bamfile = "%s/%s.uniq.sorted.bam"%(output,line)

        picard_command = "java -Xmx16g -jar %s/MarkDuplicates.jar \
        TMP_DIR=/root/data/liver/step6_callSNP/TMP \
        MAX_FILE_HANDLES_FOR_READ_ENDS_MAP=500  VALIDATION_STRINGENCY=LENIENT REMOVE_DUPLICATES=TRUE \
        INPUT=%s OUTPUT=%s/%s.uniq.sorted.picard.bam METRICS_FILE=%s/%s_metrics.txt" %(picard_path, bamfile, output, line, output, line)
        samtools_command5 = "samtools mpileup -ugf %s -t DP,DPR  %s | bcftools call -vmO z -V\
        indels -o %s/%s.vcf.gz"%(fa_index,"%s/%s.uniq.sorted.picard.bam"%(output,line),output,line)
        deleteCommand = "mv %s/%s.uniq.sorted.picard.bam %s/; mv %s/%s.vcf.gz %s; rm  %s/%s.*"%(output,line,savedBam,output,line,savedBam,output,line)
        samtools_command3 = "samtools index %s/%s.uniq.sorted.picard.bam"%(savedBam,line)
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
