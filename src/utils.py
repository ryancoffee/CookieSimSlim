#!/usr/bin/python3

import numpy as np
import h5py
from scipy.fftpack import dct

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


def dct_2d(x):
    return(dct(dct(x,axis=0,type=2),axis=1,type=2))

def idct_2d(x):
  return dct(dct(x,axis=0,type=3), axis=1,type=3)/4/x.shape[0]/x.shape[1]

