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
    return ind,rmax,res

def conv1d(xmat,ymat):
    #return np.fft.ifft(np.fft.fft(xmat,axis=1)*np.fft.fft(np.flip(ymat,axis=1),axis=1),axis=1)
    return np.fft.ifft(np.fft.fft(xmat,axis=1)*np.fft.fft(np.flip(ymat,axis=1),axis=1),axis=1)

def fillKernel(f,k,kern):
    for r in range(kern.shape[1]):
        w = f[k].attrs['sasewidth']
        c = float(kern.shape[0]>>1) + f[k].attrs['kickstrength'] * np.sin(r*2*np.pi/float(kern.shape[1]))
        kern[r,:] = gauss(np.arange(kern.shape[0]),w,c)
    return kern

def main(fname):
    rng = np.random.default_rng()
    with h5py.File(fname,'r') as f:
        shotkeys = [k for k in f.keys()]
        rng.shuffle(shotkeys)
        k = shotkeys[0]
        x = f[k]['Ximg'][()]
        y = f[k]['Ypdf'][()]
        kern = np.zeros(x.shape,dtype=float)
        kern = fillKernel(f,k,kern)
        fig,axs = plt.subplots(1,4)
        ix,jx,resx = kernConv1d(kern,x)
        iy,jy,resy = kernConv1d(kern,y)
        axs[0].plot(resx,label='resx, %i,%i'%(ix,jx))
        axs[0].plot(resy,label='resy, %i,%i'%(iy,jy))
        axs[0].legend()
        axs[1].imshow(x)
        axs[1].set_title('Ximg')
        axs[2].imshow(y)
        axs[2].set_title('Ypdf')
        axs[3].imshow(kern)
        axs[3].set_title('kernel')
        plt.show()

    return

if __name__ == '__main__':
    if len(sys.argv)<2:
        print('give me a file to process')
    else:
        main(sys.argv[1])
