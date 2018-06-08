#!/usr/bin/env python3.6

import os
import pandas as pd
import sys
import argparse as ap

parser = ap.ArgumentParser(description = 'remove headers from macs2 peak files')
parser.add_argument('-p','--peakDirectory', help = 'directory containing the macs2 peak files', required = True)
parser.add_argument('-o','--outputDirectory', help = 'directory to output cleaned peak files', required = True)
args = parser.parse_args()

class cleanMacsPeaks(object):
    
    def __init__(self, peakDir, outputDir):
        if not os.path.isdir(peakDir):
            sys.exit(peakDir + ' is not a valid directory')
        if not os.path.isdir(outputDir):
            os.makedirs(outputDir)
        os.chdir(peakDir)
        peak_files = [x for x in os.listdir() if x.endswith('peaks.xls')]
        for file in peak_files:
            with open(file) as f:
                    cleaned = [x.rstrip().split('\t') for x in f if not x.startswith('#') and x.rstrip() != '']
                    df = pd.DataFrame(cleaned)
                    df.columns = df.iloc[0]
                    df = df[1:4]
                    df.to_csv(os.path.join(outputDir, file[:-4] + '.bed'), sep='\t', header=True, index=False)

if __name__ == '__main__':
    
    results = cleanMacsPeaks(peakDir = args.peakDirectory,
                             outputDir = args.outputDirectory)
