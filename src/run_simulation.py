#!/usr/bin/python3

import h5py
from simulation import Params, runprocess
import utils
import sys
import multiprocessing as mp
import os
import re
import math

import argparse

parser = argparse.ArgumentParser(description='CookieBox simulator for Attosecond Angular Streaking')
parser.add_argument('-ofname', type=str,required=True, help='ouput path and base file name')
parser.add_argument('-n_threads',   type=int, default=2, help='Number of Threads')
parser.add_argument('-offset_threads',   type=int, default=0,required=False, help='DONT USE: Offset for Threads, used to produce rngseed[offset] to rngseed[offset + n_threads]')
parser.add_argument('-n_angles',type=int, default=128, help='Number of angles')
parser.add_argument('-n_energies',type=int, default=128, help='Number of energy bins [in eV for now]')
parser.add_argument('-n_images', type=int,default=10, help='Number of images per thread [default 10]')
parser.add_argument('-drawscale', type=float,default=0.1,required=False, help='Scaling for draws from the distribution, e.g. scale the number of electrons [default 1]')
parser.add_argument('-drawscalevar', type=float,default=0.0,required=False, help='Sinusoidal variation (over nthreads)  for scaling the number of draws from the distribution, e.g. scale the number of electrons [default 0.0]')
parser.add_argument('-sasescale', type=int,default=3,required=False, help='Scaling for number of sase subspikes (like number of sinusoids) [default 3]')
parser.add_argument('-sasescalevar', type=int,default=0,required=False, help='Sinusoidal variation (over nthreads) for scaling the number of sinusoids [default 0]')
parser.add_argument('-centralenergy', type=float,default=50.0,required=False, help='central photon energy [default 50.0]')
parser.add_argument('-centralenergywidth', type=float,default=5.0,required=False, help='central photon energy width [default 5.0]')
parser.add_argument('-centralenergyvar', type=float,default=0.0,required=False, help='central photon energy variation as sinusoid over nthreads')
parser.add_argument('-darkscale', type=float,default=0.0005,required=False, help='Scaling for the dark count haze that is independent total intensity')
parser.add_argument('-secondaryscale', type=float,default=0.002,required=False, help='Scaling for the secondary counts as proportion of total intensity')
parser.add_argument('-kickstrength', type=float,default=30,required=False, help='angular streaking kick strength')
parser.add_argument('-kickstrengthvar', type=float,default=5,required=False, help='variation of kick strength due to streaking laser fluctuations')
parser.add_argument('-polstrength', type=float,default=0,required=False, help='anisotropy is 1 + polstrength*cos(2*theta))')
parser.add_argument('-polstrengthvar', type=float,default=0,required=False, help='variation of anisotropy')
parser.add_argument('-testsplit', type=float,default=0.1,required=False, help='test images as percent of total')
parser.add_argument('-custom_evenly_distributed_sase', type=bool,default=False,required=False, help='custom evenly distributed sase')

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
    print('sz = %i'%sz)
    for i,p in enumerate(paramslist):
        print('i = %i'%i)
        p.settid(i+args.offset_threads).setstreaking()
        p.setnenergies(args.n_energies).setnangles(args.n_angles).settestsplit(args.testsplit).setdarkscale(args.darkscale).setsecondaryscale(args.secondaryscale)
        p.setdrawscale(args.drawscale) # + int(args.drawscalevar*math.cos(float(i)*2.0*math.pi/float(sz))))
        p.setsasescale(args.sasescale) # + int(args.sasescalevar*math.cos(math.pi/4. + float(i)*2.0*math.pi/float(sz)) ))
        p.setcentralenergy(args.centralenergy)
        #p.setcentralenergyvar(args.centralenergyvar) #*math.sin(float(i)*2.0*math.pi/float(sz)))
        p.setkickstrength(args.kickstrength)
        p.setkickstrengthvar(args.kickstrengthvar) #*math.sin(-math.pi/4. + float(i)*2.0*math.pi/float(sz)))
        p.setcentralenergywidth(args.centralenergywidth)
        p.set_custom_evenly_distributed_sase(args.custom_evenly_distributed_sase)

    with mp.Pool(processes=len(paramslist)) as pool:
        pool.map(runprocess,paramslist)

    return

if __name__ == '__main__':
    main()
