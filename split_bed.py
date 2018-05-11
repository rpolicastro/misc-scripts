#!/usr/bin/env python3.6

import os
import argparse
import pandas as pd
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-b','--bedFile', help='bed file to split', required=True)
parser.add_argument('-g','--geneListDirectory', help='directory containing gene list(s) in tab delimited format (without column headers)', required=True)
parser.add_argument('-o','--outputDirectory', help='directory to output split bed file(s)', required=True)
parser.add_argument('--includeAll', help='whether to create a separate bed file with genes not in the list(s)', action='store_false')
args = parser.parse_args()

class splitBed(object):
    
    def loadBed(self, bedFile):
        if not os.path.isfile(bedFile):
            sys.exit('could not find bed file')
        with open(bedFile) as b:
            filtered = [x.rstrip().split('\t') for x in b if x.lower().startswith('chr')]
        self.bed = pd.DataFrame(filtered)
    
    def loadGeneLists(self, geneListDirectory):
        if not [os.path.isdir(geneListDirectory)]:
            sys.exit('could not find gene list directory: ' + geneListDirectory)
        gene_lists = [x for x in os.listdir(geneListDirectory) if x.endswith('.txt') or x.endswith('.tsv')]
        if len(gene_lists) == 0:
            sys.exit('could not find gene lists in directory: ' + geneListDirectory)
        self.gene_lists = {x[:-4]:list(pd.read_table(os.path.join(geneListDirectory,x), header=None, sep='\t')[0]) for x in gene_lists}
        
    def splitBed(self, includeAll=False):
        self.matches = {}
        for key,values in self.gene_lists.items():
            genes = '(' + '(\\.\\d)?|'.join(values) + ')'
            self.matches[key] = self.bed[self.bed.iloc[:][3].str.contains(genes)]
        if includeAll:
            self.include_all = True
            listed_genes = [] 
            [listed_genes.extend(values) for key,values in self.gene_lists.items()]
            genes = '(' + '(\\.\\d)?|'.join(listed_genes) + ')'
            self.unmatched = self.bed[~self.bed.iloc[:][3].str.contains(genes)]
        
    def exportFiles(self, outputDir):
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        [value.to_csv(os.path.join(outputDir, key + '.bed'), sep='\t', header=False, index=False) for key,value in self.matches.items()]
        if self.include_all:
            self.unmatched.to_csv(os.path.join(outputDir, 'unmatched.bed'), sep='\t', header=False, index=False)

if __name__ == '__main__':
    bed = splitBed()
    bed.loadBed(bedFile=args.bedFile)
    bed.loadGeneLists(geneListDirectory=args.geneListDirectory)
    bed.splitBed(includeAll=args.includeAll)
    bed.exportFiles(outputDir=args.outputDirectory)