import subprocess

class Tools():
    def __init__(self):
        pass
    
    def salmon(self, fq1, fq2, index, prefix):
        command = ['salmon', 'quant', '-i', index, '-l', 'A', '-1', fq1,\
                   '-2', fq2, '-o', prefix]
        print(' '.join(command))
        subprocess.call(command)
        return