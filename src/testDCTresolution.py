#!/usr/bin/python3

import numpy as np
import h5py
from scipy.fftpack import dct
import utils
import sys

def main():
    if len(sys.argv) < 2:
        print('need input h5 filename')
        return

    fname = sys.argv[1]
    f = h5py.File(fname,'r')
    for k in list(f.keys()):
        print(list(f[k].keys()))

    return

if __name__ == '__main__':
    main()
