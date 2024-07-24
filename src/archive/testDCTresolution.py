#!/usr/bin/python3

import numpy as np
import h5py
from scipy.fftpack import dct
import utils
import sys

def main():
    if len(sys.argv) < 2:
        print('need input h5 filename')
        return

    fname = sys.argv[1]
    f = h5py.File(fname,'r')
    Ydctlist = []
    Xdctlist = []
    for k in list(f.keys()):
        print(list(f[k].keys()))
        im = f[k]['Ximg'][()]
        np.savetxt('%s.%s.Ximg.dat'%(fname,k),im,fmt='%i')
        np.savetxt('%s.%s.Ypdf.dat'%(fname,k),f[k]['Ypdf'][()],fmt='%.3f')
        Xdct = utils.dct_2d(im)
        Xdctlist += [Xdct]
        Xdct_mean = Xdct[0][0] 
        Xdct[0][0] = 0
        np.savetxt('%s.%s.Xdct.dat'%(fname,k),Xdct,fmt='%i')
        Ydct = utils.dct_2d(f[k]['Ypdf'][()])
        Ydctlist += [Ydct]
        Ydct_mean = Ydct[0][0] 
        Ydct[0][0] = 0
        np.savetxt('%s.%s.Ydct.dat'%(fname,k),Ydct,fmt='%i')

    Xvar = np.var(np.stack(Xdctlist,axis=-1),axis=-1)
    np.savetxt('%s.Xdctvar.dat'%(fname),Xvar,fmt='%.2f')
    Yvar = np.var(np.stack(Ydctlist,axis=-1),axis=-1)
    np.savetxt('%s.Ydctvar.dat'%(fname),Yvar,fmt='%.2f')
    mask = np.zeros(Yvar.shape,dtype=int)
    inds = np.where(Xvar>.01*np.max(Xvar))
    mask[inds] = 1
    np.savetxt('%s.dctmask.dat'%(fname),mask,fmt='%i')
    for k in list(f.keys()):
        im = f[k]['Ximg'][()]
        Xdct = utils.dct_2d(im)
        Ximg_masked = utils.idct_2d(Xdct*mask)
        np.savetxt('%s.%s.Ximg_masked.dat'%(fname,k),Ximg_masked,fmt='%f')

    print(np.sum(mask)/(mask.shape[0]*mask.shape[1]))
    return

if __name__ == '__main__':
    main()
