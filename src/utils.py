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


def build_XY(params):
    rng = params.rng
    x = np.arange(params.nenergies,dtype=float)
    w = 5.
    ncenters = rng.poisson(3)
    phases = rng.normal(np.pi,2,ncenters)
    centers = rng.random(ncenters)*x.shape[0]
    amp = rng.normal(30,3)
    intens = [rng.poisson(10)/10 for c in centers]
    ymat = params.darkscale * np.ones((params.nangles,x.shape[0]),dtype=float)
    if ncenters>0:
        ymat += float(params.secondaryscale)*np.sum(intens)/float(ncenters) #* np.ones((nangles,x.shape[0]),dtype=float)

    for i in range(len(centers)):
        for a in range(params.nangles):
            kick = amp*np.cos(a*2.*np.pi/params.nangles + phases[i])
            ymat[a,:] += intens[i]*cossq(x,w,centers[i]+kick) # this produces the 2D PDF
    cmat = np.cumsum(ymat,axis=1)
    # the number of draws for each angle should be proportional to the total sum of that angle
    hits = []
    for a in range(params.nangles):
        cum = cmat[a,-1]
        draws = int(params.drawscale*cum)
        drawpoints = np.sort(rng.random(draws))
        if cum>0:
            hits.append(list(np.interp(drawpoints,cmat[a,:]/cum,x)))
        else:
            hits.append([])
    return hits,ymat

def images2ascii(fname,nimages):
    Ximgs = []
    Yimgs = []
    with h5py.File(fname,'r') as f:
        for i,k in enumerate(list(f.keys())[:nimages]):
            Ximgs += [ f[k]['Ximg'][()] ]
            Yimgs += [ f[k]['Ypdf'][()] ]
    return Ximgs,Yimgs
