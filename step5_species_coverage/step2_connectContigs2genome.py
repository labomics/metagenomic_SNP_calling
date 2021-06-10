#!/usr/bin/python

father = dict()
genome_len = dict()
contig_len = dict()
mapp = {}
with open("../keyFiles/genomeInfo.txt","r") as inpf:
    for line in inpf:
        line = line.strip()
        genome,contig,length,description = line.split("\t")
        contig_len[contig] = int(length)
        father[contig] = genome
        genome_len[genome] = genome_len.get(genome,0)+int(length)
	#print genome_len[genome]
with open("../keyFiles/data.list","r") as inpf:
    for line in inpf:
        sites = dict()
        bases = dict()
        sitesUniq = dict()
        basesUniq = dict()
        line = line.strip()
        sample,type = line.split("\t")
        infile = "./contigCoverage1/%s.coverage.txt"%sample
        with open(infile,"r") as inpf2:
            for record in inpf2:
                record = record.strip()
                array = record.split(" ")
                if len(array) == 7:
                    genome = father[array[0]]
                    sites[genome] = sites.get(genome,0) + int(array[4])
                    bases[genome] = bases.get(genome,0) + int(array[5])

        outfile = "./genomeCoverage/%s.coverage.txt"%sample
        with open(outfile,"w") as outpf:
            outpf.write("#genome,width,depth,curSites,curBases,genome_len[genome]\n")
            for genome in genome_len.keys():
                curSites = sites.get(genome,0)
                curBases = bases.get(genome,0)
                width = float(curSites)/genome_len[genome]
                if width < 0.4:
                    outpf.write("")
                else:
                    depth = float(curBases)/sites[genome]
                    outpf.write("%s %s %s %s %s %s"%(genome,width,depth,curSites,curBases,genome_len[genome]))
                    outpf.write("\n")

