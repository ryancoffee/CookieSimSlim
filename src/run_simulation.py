#!/usr/bin/python3

import h5py
from simulation import Params, runprocess
import sys
import multiprocessing as mp
import os
import re
import math

import argparse

parser = argparse.ArgumentParser(description='CookieBox simulator for Attosecond Angular Streaking')
parser.add_argument('-ofname', type=str,required=True, help='ouput path and base file name')
parser.add_argument('-n_threads',   type=int, default=2, help='Number of Threads')
parser.add_argument('-n_angles',type=int, default=128, help='Number of angles')
parser.add_argument('-n_images', type=int,default=10, help='Number of images per thread')
parser.add_argument('-drawscale', type=int,default=1,required=False, help='Scaling for draws from the distribution, e.g. scale the number of electrons')
parser.add_argument('-drawscalevar', type=int,default=0,required=False, help='Sinusoidal variation (over nthreads)  for scaling the number of draws from the distribution, e.g. scale the number of electrons')
parser.add_argument('-centralenergy', type=float,default=50.0,required=False, help='central photon energy')
parser.add_argument('-centralenergywidth', type=float,default=5.0,required=False, help='central photon energy width')
parser.add_argument('-centralenergyvar', type=float,default=0.0,required=False, help='central photon energy variation as sinusoid over nthreads')
parser.add_argument('-darkscale', type=float,default=0.0005,required=False, help='Scaling for the dark count haze that is independent total intensity')
parser.add_argument('-secondaryscale', type=float,default=0.002,required=False, help='Scaling for the secondary counts as proportion of total intensity')
parser.add_argument('-kickstrength', type=float,default=30,required=False, help='angular streaking kick strength')
parser.add_argument('-kickstrengthvar', type=float,default=5,required=False, help='variation of kick strength due to streaking laser fluctuations')
parser.add_argument('-polstrength', type=float,default=0,required=False, help='anisotropy is 1 + polstrength*cos(2*theta))')
parser.add_argument('-polstrengthvar', type=float,default=0,required=False, help='variation of anisotropy')
parser.add_argument('-testsplit', type=float,default=0.1,required=False, help='test images as percent of total')

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
    paramslist = [Params(m.group(1),m.group(2),args.n_images) for i in range(args.n_threads)]
    sz = len(paramslist)
    for i,p in enumerate(paramslist):
        p.settid(i).setstreaking()
        p.setnangles(args.n_angles).settestsplit(args.testsplit).setdarkscale(args.darkscale).setsecondaryscale(args.secondaryscale)
        p.setdrawscale(args.drawscale + int(args.drawscalevar*math.cos(float(i)*2.0*math.pi/float(sz))))
        p.setcentralenergy(args.centralenergy + args.centralenergyvar*math.sin(float(i)*2.0*math.pi/float(sz)))
        p.setkickstrength(args.kickstrength + args.kickstrengthvar*math.sin(-math.pi/4. + float(i)*2.0*math.pi/float(sz)))
        p.setcentralenergywidth(args.centralenergywidth)

    with mp.Pool(processes=len(paramslist)) as pool:
        pool.map(runprocess,paramslist)

    return

if __name__ == '__main__':
    main()
