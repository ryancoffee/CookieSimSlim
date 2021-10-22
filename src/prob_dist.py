#!/usr/bin/python3

import h5py
from simulation import Params
import sys
import multiprocessing as mp
import argparse
import os
import utils

parser = argparse.ArgumentParser(description='Bragg Peak representation encoding')
parser.add_argument('-n_threads',   type=int, default=2, help='Number of Threads')
parser.add_argument('-angle',type=int, default=128, help='Number of angles')
parser.add_argument('-num_images', type=int,default=10, help='Number of images per thread')
parser.add_argument('-ofn', type=str,required=True, help='ouput file name')

def main():
    args, unparsed = parser.parse_known_args()
    if len(unparsed) > 0:
        print('Unrecognized argument(s): \n%s \nProgram exiting ... ... ' % '\n'.join(unparsed))
        exit(0)
    if not os.path.exists(args.ofn):
        os.makedirs(args.ofn)
    paramslist = [Params('%s'%(args.ofn),args.num_images) for i in range(args.n_threads)]
    for p in paramslist:
        p.setnangles(args.angle).setdrawscale(2).settestsplit(.1)

    with mp.Pool(processes=len(paramslist)) as pool:
        pool.map(runprocess,paramslist)


    return

if __name__ == '__main__':
    main()
