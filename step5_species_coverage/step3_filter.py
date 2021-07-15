#!/usr/bin/python
import re
import sys
coverpath = "/root/lp/liver/steq10_species_coverage/genomeCoverage"
diabetes_species = dict()
normal_species = dict()
diabetes_list = dict()
normal_list = dict()
genomeList = set()
with open("../keyFiles/data.list",'r') as inpf:
    for line in inpf:
        line = line.strip()
        sample,type = line.split("\t")
        coverInfo = "%s/%s.coverage.txt"%(coverpath,sample)
        with open(coverInfo,'r') as inpf2:
            for line2 in inpf2:
                line2 = line2.strip()
                if re.match("#",line2):
                    continue
                tmparray = line2.split(" ")
                genome = tmparray[0]
                genomeList.add(genome)
                uniqDepth = float(tmparray[-2])/float(tmparray[-3])
                uniqWidth = float(tmparray[-3])/float(tmparray[-1])
                if uniqDepth>=10 and uniqWidth>=0.4:
                    if type == 'Y':
                        diabetes_species[genome] = diabetes_species.get(genome,0) + 1
                        if diabetes_list.get(genome,'haha') == 'haha':
                            diabetes_list[genome] = list()
                        diabetes_list[genome].append(sample)
                    if type == 'N':
                        normal_species[genome] =   normal_species.get(genome,0) + 1
                        if normal_list.get(genome,'haha') == 'haha':
                            normal_list[genome] = list()
                        normal_list[genome].append(sample)
for genome in genomeList:
    if diabetes_species.get(genome,0)>19 and normal_species.get(genome,0)>19:
        print "%s %d %d"%(genome,diabetes_species[genome],normal_species[genome])
        with open("./datalist/%s.data.list"%genome,'w') as outpf:
            for sample in diabetes_list[genome]:
                outpf.write("%s\t%s\n"%(sample,'Y'))
            for sample in normal_list[genome]:
                outpf.write("%s\t%s\n"%(sample,'N'))
