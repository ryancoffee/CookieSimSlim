#!/usr/bin/python3

import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt
from utils import gauss

def kernConv1d(kmat,xmat):
    res = np.zeros(xmat.shape[1],dtype=float)
    ind = 0
    rmax = 0
    for i in range(xmat.shape[0]):
        tmp = np.sum( np.fft.ifft(np.fft.fft(np.roll(kmat,i,axis=0),axis=1)*np.fft.fft(np.flip(xmat,axis=1),axis=1),axis=1).real, axis=0)
        if np.max(tmp)>np.max(res):
            res = tmp
            ind = i
            rmax = np.argmax(res)
            vmax = res[rmax]
    return ind,rmax,vmax,res

def conv1d(xmat,ymat):
    return np.fft.ifft(np.fft.fft(xmat,axis=1)*np.fft.fft(np.flip(ymat,axis=1),axis=1),axis=1)

def scanKernel(widths,strengths,xmat):
    kmat = np.zeros(xmat.shape,dtype=float)
    vref = 0.
    stref = 0.
    wdref = 0.
    indref = 0
    rowref = 0
    for st in strengths:
        for wd in widths:
            kmat = fillKernel(wd,st,kmat)
            ind,row,vmax,res = kernConv1d(kmat,xmat)
            if vmax>vref:
                indref = ind
                rowref = row
                wdref = wd
                stref = st
                vref = vmax
                print(vmax)
    return indref,rowref,stref,wdref,vref

def fillKernel(width,strength,kern):
    for r in range(kern.shape[1]):
        w = width 
        c = float(kern.shape[0]>>1) + strength * np.sin(r*2*np.pi/float(kern.shape[1]))
        kern[r,:] = gauss(np.arange(kern.shape[0]),w,c)
    integral = np.sum(kern)
    return kern/integral

def main(fname):
    rng = np.random.default_rng()
    with h5py.File(fname,'r') as f:
        shotkeys = [k for k in f.keys()]
        rng.shuffle(shotkeys)
        k = shotkeys[0]
        x = f[k]['Ximg'][()]
        y = f[k]['Ypdf'][()]
        wlist = f[k].attrs['sasewidth']*np.arange(.5,2,.1,dtype=float)
        print(wlist)
        slist = f[k].attrs['kickstrength']*np.arange(.5,2,.1,dtype=float)
        print(slist)
        indref,rowref,stref,wdref,vref = scanKernel(wlist,slist,y)
        kern = np.zeros(x.shape,dtype=float)
        kern = fillKernel(width=wdref,strength=stref,kern=kern)
        #ix,jx,xmx,resx = kernConv1d(kern,x)
        #iy,jy,ymx,resy = kernConv1d(kern,y)
        fig,axs = plt.subplots(1,4)
        #axs[0].plot(resx,label='resx, %i,%i'%(ix,jx))
        #axs[0].plot(resy,label='resy, %i,%i'%(iy,jy))
        #axs[0].legend()
        axs[0].imshow(np.roll(np.roll(kern,indref,axis=0),rowref,axis=1))
        axs[0].set_title('%i,%i,%i,%i,%i'%(indref,rowref,int(stref),int(wdref),int(vref)))
        axs[1].imshow(x)
        axs[1].set_title('Ximg')
        axs[2].imshow(y)
        axs[2].set_title('Ypdf')
        axs[3].imshow(kern)
        #axs[3].imshow(np.roll(np.roll(kern,ix,axis=0),iy,axis=1))
        axs[3].set_title('kernel')
        plt.show()

    return

if __name__ == '__main__':
    if len(sys.argv)<2:
        print('give me a file to process')
    else:
        main(sys.argv[1])
