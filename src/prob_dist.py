#!/usr/bin/python3

import numpy as np
import h5py
import hashlib
import time
import sys
import re
import multiprocessing as mp
import os
from utils import cossq,gauss,build_XY

class Params:
    def __init__(self,name,n):
        self.ofname = name
        self.nimages = n 
        self.nenergies = 128
        self.nangles = 64
        self.drawscale = 10
        self.testsplit = 0.1

    def setnenergies(self,n):
        self.nenergies = int(n)
        return self
    def setnangles(self,n):
        self.nangles = int(n)
        return self
    def setdrawscale(self,n):
        self.drawscale = int(n)
        return self
    def setofname(self,name):
        self.ofname = name
        return self
    def setnimages(self,n):
        self.nimages = n
        return self
    def settestsplit(self,r): # this is the ratio of test images to total images generated
        self.testsplit = r
        return self

    def getnenergies(self):
        return self.nenergies
    def getnangles(self):
        return self.nangles 
    def getdrawscale(self):
        return self.drawscale
    def getofname(self):
        return self.ofname
    def getnimages(self):
        return self.nimages
    def gettestsplit(self): 
        return self.testsplit

def runprocess(params):
    rng = np.random.default_rng()
    m = re.search('(^.*)\.h5',params.ofname)
    #print(params.ofname)
    if not m:
        print('failed filename match')
        return
    ofname = '%s.pid%i.h5'%(m.group(1),os.getpid())
    nimages = params.nimages
    tstring = '%s%.9f'%(ofname,time.clock_gettime(time.CLOCK_REALTIME))
    keyhash = hashlib.sha256(bytearray(map(ord,tstring)))
    testsplit = params.testsplit
    with h5py.File(ofname,'a') as f:
        for i in range(nimages):
            bs = bytearray(map(ord,'shot_%i_'%i))
            keyhash.update(bs)
            key = keyhash.hexdigest()
            grp = f.create_group(key)
            nenergies = params.nenergies #128
            hbins = np.arange(nenergies+1,dtype=np.float16) # have to add 1 since histogram bin edges.
            nangles = params.nangles #64
            drawscale = params.drawscale #10
            X,Y = build_XY(nenergies = nenergies, nangles = nangles, drawscale = drawscale)
            grp.create_dataset('Ypdf',data=Y,dtype=np.float32)

            hitsvec = []
            nedges = [0]
            addresses = []
            for h in X:
                if len(h)==0:
                    nedges += [0]
                    addresses += [0]
                else:
                    nedges += [len(h)]
                    addresses += [len(hitsvec)]
                    hitsvec += h
            grp.create_dataset('Xhits',data=hitsvec,dtype=np.float32)
            grp.create_dataset('Xaddresses',data=addresses,dtype=int)
            grp.create_dataset('Xnedges',data=nedges,dtype=int)
            grp.attrs.create('nangles',nangles)
            grp.attrs.create('nenergies',nenergies)
            grp.attrs.create('drawscale',drawscale)

            img = np.zeros((grp.attrs['nangles'],grp.attrs['nenergies']),dtype=np.uint16)

            for a in range(grp.attrs['nangles']):
                offset = grp['Xaddresses'][()][a]
                nhits = grp['Xnedges'][()][a]
                img[a,:] += np.histogram(grp['Xhits'][()][offset:offset+nhits],hbins)[0].astype(np.uint16)
            grp.create_dataset('Ximg',data=img,dtype=np.int16)

            grp.attrs.create('Test',False)
            grp.attrs.create('Train',False)
            if rng.uniform()<testsplit:
                grp.attrs['Test'] = True
            else:
                grp.attrs['Train'] = True

        '''
        output file struct
        main--image --Xhits,Xaddresses,Xnedges
                    --Ypdf
                    --Ximg
                    --attrs --nangles (the number of angles measured)
                            --nenergies (the number of energy bins)
                            --drawscale (the x-ray intensity scale factor for draws from the CDF-cumulative distribution function)
                            --test/train
            --image
            --image
        '''

    return


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
