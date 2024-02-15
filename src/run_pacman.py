#!/usr/bin/python3

import numpy as np
import h5py
import sys
import matplotlib.pyplot as plt
from utils import gauss

def main(fname):
    with h5py.File(fname,'r') as f:
        keylist = list(f.keys())
        for k in keylist[:3]:
            print(f[k].attrs.keys())
            X = f[k]['Ypdf'][()]
            #X = f[k]['Ximg'][()]
            plt.imshow(X)
            plt.show()
            XFT = np.fft.fft2(X)
            kern = np.zeros(XFT.shape,float)
            for r in range(kern.shape[1]):
                w = f[k].attrs['sasewidth']*.1
                c = float(kern.shape[0]>>1) + f[k].attrs['kickstrength'] * np.sin(r*2*np.pi/float(kern.shape[1]))
                kern[r,:] = gauss(np.arange(kern.shape[0]),w,c)
            norm = np.sqrt(np.inner(kern.flatten(),kern.flatten()))
            kernFT = np.fft.fft2(kern)
            res = np.fft.ifft2(XFT*kernFT).real
            inds = np.where(res==np.max(res))
            print(inds)
            plt.imshow(res)
            plt.title('%i,%i'%(inds[0],inds[1]))
            plt.colorbar()
            plt.show()
            remove = np.roll(np.roll(kern,inds[0]-kern.shape[0],axis=0),inds[1]-kern.shape[1],axis=1)
            #remove /=norm
            #plt.imshow(X+1e2*remove)
            plt.imshow(X-np.inner(X,remove)*remove)
            plt.show()

    return

if __name__ == '__main__':
    if len(sys.argv)<2:
        print('syntax: ./src/run_pacman.py path-to-h5filename.h5')
    else:
        main(sys.argv[1])
