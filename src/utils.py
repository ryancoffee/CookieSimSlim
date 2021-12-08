#!/usr/bin/python3

import numpy as np
import h5py

def cossq(x,w,c):
    inds = np.where(np.abs(x.astype(float)-c)<w)
    y = np.zeros(x.shape)
    y[inds] = 0.5*(1+np.cos(np.pi*(x[inds].astype(float)-c)/w))
    return y

def gauss(x,w,c):
    return np.exp(-((x.astype(float)-c)/w)**2)

def images2ascii(fname,nimages):
    Ximgs = []
    Yimgs = []
    with h5py.File(fname,'r') as f:
        for i,k in enumerate(list(f.keys())[:nimages]):
            Ximgs += [ f[k]['Ximg'][()] ]
            Yimgs += [ f[k]['Ypdf'][()] ]
    return Ximgs,Yimgs
