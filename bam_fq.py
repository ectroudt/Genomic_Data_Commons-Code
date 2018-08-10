import sys 
import subprocess
import re

class Bam_fq():
    def __init__(self):
        return

    def bam_to_sorted_bam(self, unsorted_bam):
        sorted_bam = unsorted_bam.replace('.bam', '.sorted')
        command = ['samtools', 'sort', unsorted_bam, sorted_bam]
        sys.stdout.write(' '.join(command) + '\n')
        subprocess.call(command)
        return sorted_bam
    
    def remove_file(self, filename):
        subprocess.call(['rm', '-r', '-f', filename])
        return
    
    def sorted_bam_to_fq(self, sorted_bam):
        fq = sorted_bam.replace('.sorted.bam', '.fq')
        command = ['samtools', 'bam2fq', sorted_bam]
        sys.stdout.write(' '.join(command) + '\n')
        with open(fq, 'w') as outfile:
            subprocess.call(command, stdout=outfile)
        return fq
        
    def split_and_sort_fq(self, fq):
        fq1 = fq.replace('.fq', '_1.fq')
        fq2 = fq.replace('.fq', '_2.fq')
        with open(fq, 'r') as infile, open(fq1, 'w') as outfile1, open(fq2, 'w') as outfile2:
            loose_chunks_1 = set()
            loose_chunks_1_dict = {}
            loose_chunks_2 = set()
            loose_chunks_2_dict = {}
            line = infile.readline()
            while line:
                chunk = ''
                if re.search("^@.*/1$", line):
                    chunk += line; chunk += infile.readline(); chunk += infile.readline(); chunk += infile.readline()
                    if self.check_chunk(chunk):
                        continue
                    chunk = '\n'.join([(chunk.split('\n')[0]).replace('/2', '')]+chunk.split('\n')[1:])
                    subline = line.replace('/1', '')
                    if subline in loose_chunks_2:
                        outfile1.write(chunk)
                        outfile2.write(loose_chunks_2_dict[subline])
                        del loose_chunks_2_dict[subline]
                        loose_chunks_2.remove(subline)
                    else:
                        loose_chunks_1_dict[subline] = chunk
                        loose_chunks_1.add(subline)
                if re.search("^@.*/2$", line):
                    chunk += line; chunk += infile.readline(); chunk += infile.readline(); chunk += infile.readline()
                    if self.check_chunk(chunk):
                        continue
                    chunk = '\n'.join([(chunk.split('\n')[0]).replace('/2', '')]+chunk.split('\n')[1:])
                    subline = line.replace('/2', '')
                    if subline in loose_chunks_1:
                        outfile2.write(chunk)
                        outfile1.write(loose_chunks_1_dict[subline])
                        del loose_chunks_1_dict[subline]
                        loose_chunks_1.remove(subline)
                    else:
                        loose_chunks_2_dict[subline] = chunk
                        loose_chunks_2.add(subline)
                line = infile.readline()
        return fq1, fq2
    
    def check_chunk(self, chunk):
        chunk = chunk.split('\n')
        if len(chunk[1]) != len(chunk[3]):
            return True
        return False