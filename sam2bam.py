import os
import subprocess as sp

class samToBam(object):
    
    def __init__(self, sam_dir):
        
        self.current_dir = sam_dir
        os.chdir(self.current_dir)
        self.current_dir = os.getcwd()
        
        if not os.path.isdir(os.path.join(self.current_dir, 'bams')):
            os.mkdir(os.path.join(self.current_dir, 'bams'))
    
    def sam_to_bam(self):
        
        file_list = os.listdir(self.current_dir)
        sam_files = [x for x in file_list if x.endswith('.sam')]
    
        for sam in sam_files:
            new_file = os.path.join(self.current_dir,'bams',str(sam[:-4] + '.bam'))
            command = ['samtools','view','-bS',sam,'>',new_file]
            command = ' '.join(command)
            sp.call(command, shell=True)
            
if __name__ == '__main__':
    
    convert = samToBam('/N/dc2/scratch/rpolicas/chec_free_mnase/aligned/')
    convert.sam_to_bam()
        
        
        