#!/usr/bin/python3

import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt
import math
from utils import gauss,addGauss2d

TEPROD = 1.62

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
    print('For now assuming 10 micron wavelength (0.124eV) for period of 33 1/3 fs for the temporal window')
    print('For now also assuming 128eV for the energy window')
    twindow = 100./3 #in femtoseconds (10 microns/(0.3microns/fs))
    print('.1eV = 100fs, 1eV = 10fs, (30nm width @ 800nm) 50meV = 33fs gives time-energy product eV*fs = %f'%TEPROD)
    with h5py.File(fname,'r') as f:
        shotkeys = [k for k in f.keys() if len(f[k].attrs['sasecenters'])>1]
        rng.shuffle(shotkeys)
        for k in shotkeys[:2]:
            x = np.copy(f[k]['Ximg'][()]).astype(int) # deep copy to preserve original
            y = np.copy(f[k]['Ypdf'][()]).astype(float) # deep copy to preserve original
            wlist = f[k].attrs['sasewidth']*np.arange(.25,1.75,.125,dtype=float)
            print(wlist)
            slist = f[k].attrs['kickstrength']*np.arange(.25,2,.125,dtype=float)
            print(slist)
            tstep = twindow/x.shape[0]
            temat = np.zeros(x.shape,dtype=float)
            tedist = np.zeros(x.shape,dtype=float)
            kern = np.zeros(x.shape,dtype=float)
    
            fig,axs = plt.subplots(3,4)
            clow=0
            chigh=20
    
            #axs[0][0].imshow(proj,origin='lower') 
            #axs[0][0].set_title('st%.1f, wd%.1f, v%.1f'%(stref,wdref,vref))
            axs[0][0].imshow(x,origin='lower',vmin=clow,vmax=chigh)
            axs[0][0].set_title('Ximg')


            for i in range(1,4):
                indref,rowref,stref,ewidth,vref = scanKernel(wlist,slist,x)
                kern = fillKernel(width=ewidth,strength=stref,kern=kern)
    
                proj = np.roll(np.roll(kern,-indref,axis=0),rowref,axis=1)
                coeff = np.inner(x.flatten(),proj.flatten())
                print(coeff/vref)
                x -= (coeff*proj).astype(int)
                temat[indref,rowref] += coeff
                addGauss2d(tedist,coeff,rowref,indref,TEPROD*ewidth*tstep,ewidth)
    
                axs[i//4][i%4].imshow(x,vmin=clow,vmax=chigh,origin='lower')
                axs[i//4][i%4].set_title('rm_%i'%i)
    
            axs[-1][-3].imshow(np.roll(np.roll(tedist,tedist.shape[0]//2,axis=0),tedist.shape[1]//2,axis=1),origin='lower')
            axs[-1][-3].set_title('tedist')
            axs[-1][-2].imshow(np.roll(np.roll(temat,temat.shape[0]//2,axis=0),temat.shape[1]//2,axis=1),origin='lower')
            axs[-1][-2].set_title('temat')
            axs[-1][-1].imshow(y,origin='lower')
            axs[-1][-1].set_title('Ypdf')
            plt.show()

    return

if __name__ == '__main__':
    if len(sys.argv)<2:
        print('give me a file to process')
        tedist = np.zeros((1<<4,1<<6),dtype=float)
        addGauss2d(tedist,1,32,8,4,2)
        plt.imshow(tedist)
        plt.show()

    else:
        main(sys.argv[1])
