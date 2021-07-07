# metagenomic_SNP_calling
## Overview
This framework contains quality control, identification of the microorganisms in the samples, construction of reference genomes, SNP calling and some subsequent statistical analysis.
## Pre-requisites
This part requires Trimmomatic, MetaPhlAn2.0, bwa, Samtools, picard, bcftools, VarScan2, vcftools installed. Check
## Flowchart
<img src="flowchart.png" width = "300" height = "429" alt="" align=center />

## Basic Usage

step1_qc performs quality control with a file contains sample name, datadir and outdir needed.
step2_metaphlan *

### Example
`python step1_qc/trimmomatic.py filepath/filename datadir outdir`
