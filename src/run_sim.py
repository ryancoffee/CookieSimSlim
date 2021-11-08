#!/usr/bin/python3

import h5py
from simulation import Params, runprocess
import sys
import multiprocessing as mp
import os
import re

import argparse

parser = argparse.ArgumentParser(description='CookieBox simulator for Attosecond Angular Streaking\nFixed parameters and rng seeds\n-ofname is only required arguement')
parser.add_argument('-ofname', type=str,required=True, help='ouput path and base file name')
parser.add_argument('-n_threads',   type=int, default=20,required=False, help='DONT USE: Number of Threads')
parser.add_argument('-n_angles',type=int, default=128,required=False, help='DONT USE: Number of angles')
parser.add_argument('-n_images', type=int,default=50000,required=False, help='DONT USE: Number of images per thread')
parser.add_argument('-drawscale', type=int,default=8,required=False, help='DONT USE: Scaling for draws from the distribution, e.g. scale the number of electrons')
parser.add_argument('-darkscale', type=float,default=0.001,required=False, help='DONE USE: Scaling for the dark count haze that is independent total intensity')
parser.add_argument('-secondaryscale', type=float,default=0.01,required=False, help='DONT USE: Scaling for the secondary counts as proportion of total intensity')
parser.add_argument('-testsplit', type=float,default=0.1,required=False, help='DONT USE: test images as percent of total')

def main():
    args, unparsed = parser.parse_known_args()
    if len(unparsed) > 0:
        print('Unrecognized argument(s): \n%s \nProgram exiting ... ... ' % '\n'.join(unparsed))
        exit(0)
    m = re.search('(^.*)\/(\w+)\.h5',args.ofname)
    if not m:
        print('failed filename match for ofname = %s'%args.ofname)
        return
    print('%s\t%s'%(m.group(1),m.group(2)))

    if not os.path.exists(m.group(1)):
        os.makedirs(m.group(1))
    paramslist = [Params(m.group(1),m.group(2),args.n_images,i) for i in range(args.n_threads)]
    for p in paramslist:
        p.setnangles(args.n_angles).setdrawscale(args.drawscale).settestsplit(args.testsplit).setdarkscale(args.darkscale).setsecondaryscale(args.secondaryscale)

    #for i,p in enumerate(paramslist):
    #    p.setrngseed(i)
    #    #print(p.rngseed)

    with mp.Pool(processes=len(paramslist)) as pool:
        pool.map(runprocess,paramslist)

    return

if __name__ == '__main__':
    main()
