#!/usr/bin/python3

import numpy as np

def cossq(x,w,c):
    inds = np.where(np.abs(x.astype(float)-c)<w)
    y = np.zeros(x.shape)
    y[inds] = 0.5*(1+np.cos(np.pi*(x[inds].astype(float)-c)/w))
    return y

def gauss(x,w,c):
    return np.exp(-((x.astype(float)-c)/w)**2)

def build_XY(nenergies=128,nangles=64,drawscale = 10):
    rng = np.random.default_rng()
    x = np.arange(nenergies,dtype=float)
    w = 5.
    amp = 30.
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
