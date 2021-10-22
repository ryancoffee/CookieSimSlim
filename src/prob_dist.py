#!/usr/bin/python3

import h5py
import sys
import multiprocessing as mp

import os
import utils



def main():
    if len(sys.argv)<5:
        print('syntax: %s <outfilename.h5> <nimages> <nchannels> <nthreads>'%sys.argv[0])
        return

    paramslist = [Params('%s'%(sys.argv[1]),int(sys.argv[2])) for i in range(int(sys.argv[4]))]
    for p in paramslist:
        p.setnangles(int(sys.argv[3])).setdrawscale(2).settestsplit(.1)

    with mp.Pool(processes=len(paramslist)) as pool:
        pool.map(runprocess,paramslist)


    return

if __name__ == '__main__':
    main()
