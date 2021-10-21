#!/usr/bin/python3

import hashlib
import numpy as np
import time
import re
import os
import utils

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

