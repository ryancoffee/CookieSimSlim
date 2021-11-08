#!/usr/bin/python3
import h5py
import hashlib
import numpy as np
import time
import re
import os
import utils


class Params:
    def __init__(self, path, name, n, s):
        self.ofpath = path
        self.ofname = name
        self.nimages = n
        self.nenergies = 128
        self.nangles = 128
        self.drawscale = 8
        self.darkscale = 0.001
        self.secondaryscale = 0.01
        self.testsplit = 0.1
        self.rngseed = s
        self.rng = np.random.default_rng(s)

    def setnenergies(self, n):
        self.nenergies = int(n)
        return self

    def setnangles(self, n):
        self.nangles = int(n)
        return self

    def setdrawscale(self, n):
        self.drawscale = int(n)
        return self

    def setofname(self, name):
        self.ofname = name
        return self

    def setnimages(self, n):
        self.nimages = n
        return self

    def setrngseed(self, n):
        self.rngseed = n
        self.rng = np.random.default_rng(n)
        return self

    def settestsplit(self, r):  # this is the ratio of test images to total images generated
        self.testsplit = r
        return self

    def setdarkscale(self, r):  # this is the level of dark counts (this doesn't scale with intensity)
        self.darkscale = r
        return self

    def setsecondaryscale(self, r):  # this is the level of secondary electron counts (this does scale with intensity) that scale with x-ray intensity
        self.secondaryscale = r
        return self

    def getsecondaryscale(self):
        return self.secondaryscale

    def getdarkscale(self):
        return self.darkscale

    def getrngseed(self):
        return self.rngseed

    def getnenergies(self):
        return self.nenergies

    def getnangles(self):
        return self.nangles

    def getdrawscale(self):
        return self.drawscale

    def getofname(self):
        return self.ofname

    def getnimages(self):
        return self.nimages


def runprocess(params):
    nimages = params.nimages
    print(params.rngseed)
    print('%s/%s.rngseed%i.h5'%(params.ofpath,params.ofname,params.rngseed))
    with h5py.File('%s/%s.rngseed%i.h5'%(params.ofpath,params.ofname,params.rngseed), 'w') as f:
        for i in range(nimages):
            key = 'shot_%i'%i
            grp = f.create_group(key)
            X, Y = utils.build_XY(params)
            grp.create_dataset('Ypdf', data=Y, dtype=np.float32)
            hitsvec = []
            nedges = [0]
            addresses = []
            for h in X:
                if len(h) == 0:
                    nedges += [0]
                    addresses += [0]
                else:
                    nedges += [len(h)]
                    addresses += [len(hitsvec)]
                    hitsvec += h
            grp.create_dataset('Xhits', data=hitsvec, dtype=np.float32)
            grp.create_dataset('Xaddresses', data=addresses, dtype=np.uint8)
            grp.create_dataset('Xnedges', data=nedges, dtype=np.uint8)
            grp.attrs.create('nangles', params.nangles,dtype=np.uint8)
            grp.attrs.create('nenergies', params.nenergies,dtype=np.uint8)
            grp.attrs.create('drawscale', params.drawscale,dtype=np.uint8)
            grp.attrs.create('darkscale', params.darkscale,dtype=np.float32)
            grp.attrs.create('secondaryscale', params.secondaryscale,dtype=np.float32)
            grp.attrs.create('rngseed', params.rngseed,dtype=np.int16)

            img = np.zeros((params.nangles,params.nenergies), dtype=np.uint16)

            for a in range(grp.attrs['nangles']):
                offset = grp['Xaddresses'][()][a]
                nhits = grp['Xnedges'][()][a]
                img[a,:] += np.histogram(hitsvec[offset:offset+nhits], np.arange(params.nenergies + 1))[0].astype(np.uint16)
            grp.create_dataset('Ximg', data=img, dtype=np.uint16)

            grp.attrs.create('Test', False)
            grp.attrs.create('Train', False)
            if params.rng.uniform() < params.testsplit:
                grp.attrs['Test'] = True
            else:
                grp.attrs['Train'] = True

        '''
        output file struct
        main--image --Xhits,Xaddresses,Xnedges
                    --Ypdf
                    --Ximg
                    --attrs --nangles (the number of angles measured)
                            --nenergies (the number of energy bins)
                            --drawscale (the x-ray intensity scale factor for draws from the CDF-cumulative distribution function)
                            --test/train
            --image
            --image
        '''

    return
