'''
Author: Zhang Xu
Date: 2016/01/19
Version: 1.0
Description: Load the code and submit for compilation.
'''

import sys
import compilerSettings
import quack

def omics(filepath, *args):
    
    print(model)
    print(sys.argv)
    
#    with open(filepath, 'r') as infile:
#        quack(infile.readlines(), outputpath)
#        glb.contents = ''.join(infile.readlines()).split('\n') # to remove \n in each line


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('ERROR!Invalid Paramters.')
        exit()
    else:
        omics(model, sys.argv)

