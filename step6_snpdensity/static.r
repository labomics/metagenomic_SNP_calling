setwd('~/major/Documents/liver/steq14_speciesDensity')
library('qvalue')

densityTable = read.table("densityMatrix.txt", header = F, row.names = 1)


curTable = densityTable
noNone0_1 = rowSums(curTable[,1:114]>-1)
noNone0_2 = rowSums(curTable[,115:237]>-1)
name1 = names(which(noNone0_1 > 10))
name2 = names(which(noNone0_2 > 10))

subNames = intersect(name1,name2)

res_wilcox <- sapply(X = subNames,FUN = function(x) {
  wilcox.test(x=as.numeric(curTable[x,which(curTable[x,1:114]>-1)]), y=as.numeric(curTable[x,which(curTable[x,115:237]>-1)+114]),paired = F)
})
sig_microbes <- NULL
sm <- NULL
for(i in colnames(res_wilcox)){
  if(!is.na(res_wilcox[3,i][[1]]) & res_wilcox[3,i][[1]] < 1){
    sm <- c(sm,i)
    sig_microbes <- c(sig_microbes,res_wilcox[3,i][[1]])
  }
}
myresult = cbind(sm,sig_microbes,qvalue_truncp(sig_microbes)$qvalues)
colnames(myresult) = c('genome','pvalue','qvalue')
write.table(file='result.txt',myresult,row.names = F,col.names=T,quote = FALSE,sep="\t")

