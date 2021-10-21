#!/usr/bin/python3

import h5py
import sys
import multiprocessing as mp




def main():
    if len(sys.argv)<4:
        print('syntax: %s <outfilename.h5> <nimages> <nthreads>'%sys.argv[0])
        return

    paramslist = [Params('%s'%(sys.argv[1]),int(sys.argv[2]) ) for i in range(int(sys.argv[3]))]
    for p in paramslist:
        p.setnangles(128).setdrawscale(5)

    with mp.Pool(processes=len(paramslist)) as pool:
        pool.map(runprocess,paramslist)


    return

if __name__ == '__main__':
    main()
