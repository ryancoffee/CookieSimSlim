#!/usr/bin/python3
import h5py
import sys

def main();
    if len(sys.argv)<2:
        print('At least give me one .h5 file to peek into')
        print('syntax: %s <list of h5 files> '%sys.argv[0])

    _=[[print(i,d,f[k][d][()].shape) for d in list(f[k].keys())] for i,k in enumerate(klist[:3])]
    return

if __name__ == '__main__':
    main()
