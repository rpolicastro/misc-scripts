#!/usr/bin/env python3.6

import os
import argparse
import sys
import subprocess as sp

parser = argparse.ArgumentParser()
parser.add_argument('-b','--bamDirectory', help='directory containing bam files', required=True)
parser.add_argument('-o','--outputDirectory', help='directory to save bigwigs', required=True)
parser.add_argument('-p','--processors', help='number of processors', default=1)
parser.add_argument('-g','--effectiveGenomeSize', help='effective genome size of assembly', required=True)
args = parser.parse_args()

class deeptools(object):
    
    def __init__(self, bamDir, outputDir, processors, effectiveGenomeSize):
        self.output_dir, self.bam_dir = outputDir, bamDir
        self.processors = processors
        self.effective_genome_size = effectiveGenomeSize
        
        if not os.path.isdir(self.bam_dir):
            sys.exit(bamDir + ' is not a valid directory')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        os.chdir(self.bam_dir)
    
    def makeBigwigs(self):
        bams = [x for x in os.listdir(os.getcwd()) if x.endswith('sorted.bam')]
        for bam in bams:
            command = ['bamCoverage -b', bam,
                       '-of bigwig',
                       '-o', os.path.join(self.output_dir, bam[:-4] + '.bw'),
                       '--effectiveGenomeSize', self.effective_genome_size,
                       '--normalizeUsing CPM',
                       '-p', self.processors]
            sp.call(' '.join(command), shell=True)

if __name__ == '__main__':
    
    bam2bw = deeptools(bamDir = args.bamDirectory,
                       outputDir = args.outputDirectory,
                       processors = args.processors,
                       effectiveGenomeSize = args.effectiveGenomeSize)
    bam2bw.makeBigwigs()
            