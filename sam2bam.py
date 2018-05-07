#!/usr/bin/env python3.6

import os
import subprocess as sp
import argparse as ap
import sys

parser = ap.ArgumentParser()
parser.add_argument('-p', '--processors', default=1, help='number of processors')
parser.add_argument('-s', '--samDirectory', required=True, help='directory containing sam files')
parser.add_argument('-o', '--outputDirectory', required=True, help='directory where bam and index files will be moved')
args = parser.parse_args()

class sam2bam(object):
    
    def __init__(self, samDir, processors):
        if not os.path.isdir(samDir):
            sys.exit(samDir + ' is not a valid directory')
        os.chdir(samDir)
        self.processors = processors
    
    def makeBams(self):
        sams = [x for x in os.listdir(os.getcwd()) if x.lower().endswith('.sam')]
        if len(sams) == 0:
            sys.exit('no sam files found')
        [sp.call(' '.join(['samtools view -@', self.processors, '-b', sam, '>', sam[:-4] + '.bam']), shell=True) for sam in sams]
        
    def sortBams(self):
        bams = [x for x in os.listdir(os.getcwd()) if x.endswith('.bam')]
        if len(bams) == 0:
            sys.exit('no bam files found')
        [sp.call(' '.join(['samtools sort -@', self.processors, bam, '-o', bam[:-4] + '_sorted.bam']), shell=True) for bam in bams]

    def indexBams(self):
        bams = [x for x in os.listdir(os.getcwd()) if x.endswith('sorted.bam')]
        if len(bams) == 0:
            sys.exit('no sorted bams found')
        [sp.call(' '.join(['samtools index -@', self.processors, bam]), shell=True) for bam in bams]
    
    def moveBams(self, outputDir):
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        bams = [x for x in os.listdir(os.getcwd()) if x.endswith('.bam') or x.endswith('.bai')]
        [os.rename(bam, os.path.join(outputDir,bam)) for bam in bams]

if __name__ == '__main__':
    sam2bam = sam2bam(samDir=args.samDirectory, processors=args.processors)
    sam2bam.makeBams()
    sam2bam.sortBams()
    sam2bam.indexBams()
    sam2bam.moveBams(outputDir=args.outputDirectory)