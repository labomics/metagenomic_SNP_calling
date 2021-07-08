 #!/usr/bin/python
import sys
import os
import qc5end
import gzip
import time
import re
def cutHead(sample):
    fromFile = "%s/%s.fastq.gz"%(datadir, sample)
    toFile = "%s/%s.qc5.fastq.gz"%(outdir, sample)   
    print "getting cutting length of head of %s..."%fromFile
    cutlen = qc5end.getFilterPos(fromFile)
    print time.strftime('%Y-%m-%d %H:%M:%S')
    print "cutting head of %s..."%fromFile
    command = "java -jar -Xms8g %s SE -threads 48 -phred33   %s %s HEADCROP:%s"%(trimmomatic,fromFile,toFile, cutlen)
    os.system(command)


listfile = "%s.txt"%sys.argv[1]
datadir = sys.argv[2]
outdir = sys.argv[3]
#datadir = "/root/data/liver/step1_classifyData/mergedData"
#outdir = "/root/data/liver/step1_classifyData/filteredData3"
trimmomatic = "/root/data/software/Trimmomatic-0.39/trimmomatic-0.39.jar"

with open(listfile,"r") as inpf:
    for line in inpf:
        line = line.strip()
	if re.match('#',line):
            continue
        file,type = line.split("\t")
        line = file
        print("start analysis %s..."%line)
        file1 = "%s_1"%line
        file2 = "%s_2"%line
        cutHead(file1)
        cutHead(file2)
        basein = "%s/%s_1.qc5.fastq.gz"%(outdir, line)
        baseout = "%s/%s.fq.gz"%(outdir, line)
        #the seconde input file will be determined automatically
        command = "java -jar -Xms8g %s PE -threads 48 -phred33 -basein %s \
                -baseout %s ILLUMINACLIP:20mer.fa:1:0:7 TRAILING:20 \
                SLIDINGWINDOW:5:10 MINLEN:45 AVGQUAL:20 " %(trimmomatic,
                        basein,baseout,)
        print("start trimmomatic pipeline...")
        os.system(command)
        del_command = "rm %s/%s*qc5*" %(outdir, line)
        os.system(del_command)

