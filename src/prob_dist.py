#!/usr/bin/python3

import numpy as np
import h5py
import hashlib
import time
import sys
import re
import multiprocessing as mp
import os

def cossq(x,w,c):
    inds = np.where(np.abs(x.astype(float)-c)<w)
    y = np.zeros(x.shape)
    y[inds] = 0.5*(1+np.cos(np.pi*(x[inds].astype(float)-c)/w))
    return y

def gauss(x,w,c):
    return np.exp(-((x.astype(float)-c)/w)**2)

def build_XY(nenergies=128,nangles=64,drawscale = 10):
    x = np.arange(nenergies,dtype=float)
    w = 5.
    amp = 30.
    rng = np.random.default_rng()
    ncenters = rng.poisson(3)
    phases = rng.normal(np.pi,2,ncenters)
    centers = rng.random(ncenters)*x.shape[0]
    ymat = np.zeros((x.shape[0],nangles),dtype=float)
    for i in range(len(centers)):
        for a in range(nangles):
            kick = amp*np.cos(a*2.*np.pi/nangles + phases[i])
            ymat[:,a] += cossq(x,w,centers[i]+kick) # this produces the 2D PDF
    cmat = np.cumsum(ymat,axis=0)
    # the number of draws for each angle should be proportional to the total sum of that angle
    hits = []
    for a in range(nangles):
        cum = cmat[-1,a]
        draws = int(drawscale*cum)
        drawpoints = np.sort(rng.random(draws))
        if cum>0:
            hits.append(list(np.interp(drawpoints,cmat[:,a]/cum,x)))
        else:
            hits.append([])
    return hits,ymat

class Params:
    def __init__(self,name,n):
        self.ofname = name
        self.nimages = n 
        self.nenergies = 128
        self.nangles = 64
        self.drawscale = 10

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

def runprocess(params):
    m = re.search('(^.*)\.h5',params.ofname)
    print(params.ofname)
    if not m:
        print('failed filename match')
        return
    ofname = '%s.pid%i.h5'%(m.group(1),os.getpid())
    nimages = params.nimages
    tstring = '%s%.9f'%(ofname,time.clock_gettime(time.CLOCK_REALTIME))
    keyhash = hashlib.sha256(bytearray(map(ord,tstring)))
    with h5py.File(ofname,'a') as f:
        for i in range(nimages):
            bs = bytearray(map(ord,'shot_%i_'%i))
            keyhash.update(bs)
            key = keyhash.hexdigest()
            grp = f.create_group(key)
            nenergies = params.nenergies #128
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
    return


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
