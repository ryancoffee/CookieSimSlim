#!/usr/bin/python3

import numpy as np
import h5py
from scipy.fftpack import dct,idct,idst
from scipy import stats
import math
from utils import testBit,setBit,getSetBits,mod2exp
from binEncodings import decode,storebase


import argparse

parser = argparse.ArgumentParser(description='Comparator for the binary encoding versus the Ximg representations')
parser.add_argument('-ofpath', type=str,required=True, help='ouput path')
parser.add_argument('-nimages', type=int,required=False,default=10, help='Number of images to process [default 10]')
parser.add_argument('-ifname', type=str,required=True,help='in file name')




def main():
    args, unparsed = parser.parse_known_args()
    f = h5py.File(args.ifname,'r')
    inum = 0
    for shot in list(f.keys())[:args.nimages]:
        im = f[shot]['Ximg'][()]
        np.savetxt('%s/im%i.dat'%(args.ofpath,inum),im,fmt='%i')

        nangles,nbits = f[shot]['words'][()].shape 
        nbits *= storebase
        bitsim = np.zeros((nangles,nbits),dtype=np.uint8)
        for a in range(nangles):
            for i in decode(f[shot]['words'][()][a]):
                bitsim[a,i] += 1
        np.savetxt('%s/bisim%i.dat'%(args.ofpath,inum),bitsim,fmt='%i')


        inum += 1

    return

if __name__ == '__main__':
    main()
