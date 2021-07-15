cp Ref.fna Ref1.fna
samtools faidx Ref.fna
gzip Ref.fna
bwa index Ref.fna.gz
mv Ref1.fna Ref.fna
