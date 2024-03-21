#!/usr/bin/python3

import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt
import math
from utils import gauss

def kernConv1d(kmat,xmat):
    res = np.zeros(xmat.shape[1],dtype=float)
    ind = 0
    rmax = 0
    for i in range(xmat.shape[0]):
        tmp = np.sum( np.fft.ifft(np.fft.fft(np.roll(xmat,i,axis=0),axis=1)*np.fft.fft(np.flip(kmat,axis=1),axis=1),axis=1).real, axis=0)
        if np.max(tmp)>np.max(res):
            res = tmp
            ind = i
            rmax = np.argmax(res)
            vmax = res[rmax]
    return ind,rmax,vmax,res

def conv1d(xmat,ymat):
    return np.fft.ifft(np.fft.fft(xmat,axis=1)*np.fft.fft(np.flip(ymat,axis=1),axis=1),axis=1)

def scanThinKernel(xmat):
    widths = [1.0]
    strengths = [float(i) for i in range(1<<5)]
    kmat = np.zeros(xmat.shape,dtype=float)
    vref = 0.
    stref = 0.
    wdref = 3.0
    indref = 0
    rowref = 0
    if not np.max(xmat)>0:
        return indref,rowref,stref,wdref,vref
    for wd in widths:
        for st in strengths:
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

def scanKernel(widths,strengths,xmat):
    kmat = np.zeros(xmat.shape,dtype=float)
    vref = 0.
    stref = 0.
    wdref = 0.
    indref = 0
    rowref = 0
    if not np.max(xmat)>0:
        return indref,rowref,stref,wdref,vref
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
    #norm = math.sqrt(np.sum(kern))
    norm = math.sqrt(np.inner(kern.flatten(),kern.flatten()))
    return kern/norm

def main(fname):
    rng = np.random.default_rng()
    with h5py.File(fname,'r') as f:
        shotkeys = [k for k in f.keys() if len(f[k].attrs['sasecenters'])>1]
        rng.shuffle(shotkeys)
        for k in shotkeys[:2]:
            x = np.copy(f[k]['Ximg'][()]).astype(int) # deep copy to preserve original
            y = np.copy(f[k]['Ypdf'][()]).astype(float) # deep copy to preserve original
            wlist = f[k].attrs['sasewidth']*np.arange(.2,1.1,.1,dtype=float)
            print(wlist)
            slist = f[k].attrs['kickstrength']*np.arange(.25,4,.125,dtype=float)
            print(slist)
            temat = np.zeros(x.shape,dtype=float)
    
            indref,rowref,stref,wdref,vref = scanThinKernel(x)
            kern = np.zeros(x.shape,dtype=float)
            kern = fillKernel(width=wdref,strength=stref,kern=kern)
            proj = np.roll(np.roll(kern,-indref,axis=0),rowref,axis=1)
            coeff = np.inner(x.flatten(),proj.flatten())
            p:int = 0
            fig,axs = plt.subplots(2,4)
            #while coeff>10 and p<20:
            while p<20:
                print("proj num %i"%p)
                temat[indref,rowref] += coeff
                x -= (coeff*proj).astype(int)
                indref,rowref,stref,wdref,vref = scanThinKernel(x)
                kern = fillKernel(width=wdref,strength=stref,kern=kern)
                proj = np.roll(np.roll(kern,-indref,axis=0),rowref,axis=1)
                coeff = np.inner(x.flatten(),proj.flatten())
                if p < 4 :
                    axs[0][p].imshow(x,origin='lower')
                    axs[0][p].set_title('coeff = %.2f'%coeff)
                p += 1

            axs[1][0].imshow(np.roll(np.roll(temat,temat.shape[0]>>1,axis=0),temat.shape[1]>>1,axis=1),origin='lower')
            axs[1][0].set_title('time-energy')

            axs[1][1].imshow(f[k]['Ximg'][()],origin='lower')
            axs[1][1].set_title('Ximg')

            axs[1][2].imshow(x,origin='lower')
            axs[1][2].set_title('coeff %i = %.2f'%(p,coeff))
    
            axs[1][3].imshow(y,origin='lower')
            axs[1][3].set_title('Ypdf')
            plt.show()

    return

if __name__ == '__main__':
    if len(sys.argv)<2:
        print('give me a file to process')
    else:
        main(sys.argv[1])
