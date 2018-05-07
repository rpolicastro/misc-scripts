#!/usr/bin/env python3.6

import os
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-b','--bamDirectory', help='directory containing bam files', required=True)
parser.add_argument('-o','--outputDirectory', help='directory to save bigwigs', required=True)
parser.add_argument('-p','--processors', help='number of processors', default=1)
args = parser.parse_args()

class deeptools(object):
    
    def __init__(self, bamDir, outputDir):
        if not os.path.isdir(bamDir):
            sys.exit(bamDir + ' is not a valid directory')
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        os.chdir(bamDir)
    
    def makeBigwig(self):
        bams = [x for x in os.listdir(os.getcwd()) if x.endswith('.bam')]
        