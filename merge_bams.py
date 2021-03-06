#!/usr/bin/env python3.6

import os
import sys
import argparse
import subprocess as sp

parser = argparse.ArgumentParser()
parser.add_argument('-b','--bamDirectory', required=True, help='directory containing sorted bam files')
parser.add_argument('-o','--outputDirectory', required=True, help='directory to putput merged bam files')
parser.add_argument('-i','--uniqueIdentifiers', required=True, help='identifiers in file names to signify which files to merge', nargs='+')
parser.add_argument('-p','--processors', required=True, help='processors for samtools index')
args = parser.parse_args()

class mergeBams(object):
    
    def __init__(self, bamDir, outputDir, identifiers, processors):
        self.bam_directory, self.output_directory = bamDir, outputDir
        self.identifiers = identifiers
        self.processors = processors
        
        if not os.path.isdir(self.bam_directory):
            sys.exit(self.bam_directory + ' is not a valid directory')
        else:
            os.chdir(self.bam_directory)
            
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        if len(identifiers) < 1:
            sys.exit('please include unique identifiers for files to merge')
    
    def merge(self):
        bams = [x for x in os.listdir() if x.endswith('.bam')]
        if len(bams) == 0:
            sys.exit('no bam files found')
        for i in self.identifiers:
            matches = [x for x in bams if i in x]
            if len(matches) == 0:
                sys.exit('no bam files found for identifier: ' + i)
            sp.call(' '.join(['samtools merge', matches[0][:-4] + '_merged.bam', ' '.join(matches)]), shell=True)
    
    def indexBams(self):
        bams = [x for x in os.listdir() if x.endswith('merged.bam')]
        if len(bams) == 0:
            sys.exit('no merged bams found')
        [sp.call(' '.join(['samtools index -@', self.processors, bam]), shell=True) for bam in bams]
    
    def moveBams(self):
        bams = [x for x in os.listdir() if x.endswith('merged.bam') or x.endswith('merged.bam.bai')]
        [os.rename(x, os.path.join(self.output_directory, x)) for x in bams]

if __name__ == '__main__':
    merge = mergeBams(bamDir = args.bamDirectory,
                      outputDir = args.outputDirectory,
                      identifiers = args.uniqueIdentifiers,
                      processors = args.processors)
    merge.merge()
    merge.indexBams()
    merge.moveBams()
        