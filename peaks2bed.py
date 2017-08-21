##############
#change peak folder to the folder where your peak files are
#need to import module python
##############

import pandas as pd
import os
import sys

###variables

peak_folder = ''

###script

if peak_folder == '':
    peak_folder = os.getcwd()

output_dir = peak_folder + 'cleaned/'
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

#clean header

file_list = os.listdir(peak_folder)
peak_files = [x for x in file_list if x.endswith('.txt')]

if len(peak_files) == 0:
    sys.exit('no peak files found')    

for p in peak_files:
    
    peak_file = peak_folder + p
    with open(peak_file) as f:
        cleaned = [x.rstrip() for x in f if x.startswith('#PeakID') or not x.startswith('#')]
    
    new_file = output_dir + 'cleaned_' + p
    if not os.path.isfile(new_file):
        contents = '\n'.join(cleaned)
        with open(new_file, mode='a') as f:
            f.write(contents)
    
#format as bed

output_dir = peak_folder + 'beds/'
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

file_list = os.listdir(str(peak_folder + 'cleaned/'))
peak_files = [x for x in file_list if x.startswith('cleaned_') and x.endswith('.txt')]

for p in peak_files:
    
    peaks = pd.read_table(str(peak_folder + 'cleaned/' + p), sep='\t')
    filtered = peaks[['chr','start','end','#PeakID','findPeaks Score','strand']]
    
    new_file = output_dir + p[8:-4] + '.bed'
    if not os.path.isfile(new_file):
        filtered.to_csv(new_file, sep='\t', index=False, header=False)