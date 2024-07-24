#!/usr/bin/python3

import h5py
import numpy as np
import sys

def main():
    if len(sys.argv)<2:
        print('need input h5 name')
        return
    fname = sys.argv[1]
    with h5py.File(fname,'r') as f:
        shots = [k for k in f.keys()]
        i = 0
        for shot in shots[:10]:
            np.savetxt('img_%02i.dat'%i,f[shot]['Ximg'][()],fmt='%i')
            np.savetxt('pdf_%02i.dat'%i,f[shot]['Ypdf'][()],fmt='%.2f')
            adds = f[shot]['Xaddresses'][()]
            edges = f[shot]['Xnedges'][()]
            hits = f[shot]['Xhits'][()]
            angles = []
            energies = []
            nangles = len(edges)
            for a in range(nangles):
                for k in range(edges[a]):
                    angles += [2.*np.pi*a/nangles]
                    energies += [hits[adds[a]+k]]
            np.savetxt('polar_%02i.dat'%i,np.stack((angles,energies),axis=-1),fmt='%.2f')
            i += 1
    return

if __name__ == '__main__':
    main()
