#!/usr/bin/python3
import h5py
import hashlib
import numpy as np
import time
import re
import os
import utils
import binEncodings as be
import platform


class Params:
    def __init__(self, path, name, n):
        self.baseencode = be.storebase
        self.nodeid = int(hashlib.sha256(platform.node().encode('utf-8')).hexdigest(),16)%(1<<16)
        self.ofpath = path
        self.ofname = name
        self.nimages = n
        self.nenergies = 128
        self.nangles = 128
        self.drawscale = 0.1
        self.darkscale = 0.0005
        self.secondaryscale = 0.002
        self.testsplit = 0.1
        self.sasescale = 3
        self.sasewidth = 10.0
        self.sasecenters = []
        self.sasephases = []
        self.saseamps = []
        self.centralenergy = 64 
        self.centralenergywidth = 8
        self.centralenergyvar = 8
        self.kickstrength = 30.
        self.kickstrengthvar = 0.
        self.polstrengths = [1.]
        self.poldirections = [0.]
        self.streaking = True
        self.spectroscopy = False
        self.tid = 0
        self.threadoffset = 0
        self.fixedlinear = False
        self.iscirc = False
        self.rng = np.random.default_rng()

    def settidIPrng(self,x):
        self.tid = x
        self.rng = np.random.default_rng(seed=x+self.nodeid)
        return self

    def settid(self,x):
        self.tid = x
        self.rng = np.random.default_rng(seed=x)
        return self

    def gettid(self):
        return self.tid

    def setstreaking(self):
        self.streaking = True 
        self.spectroscopy = False
        return self

    def getstreaking(self):
        return self.streaking

    def getspectroscopy(self):
        return self.spectroscopy

    def setspectroscopy(self):
        self.streaking = False 
        self.spectroscopy = True
        return self

    def setnenergies(self, n):
        self.nenergies = int(n)
        return self

    def setnangles(self, n):
        self.nangles = int(n)
        return self

    def setdrawscale(self, n):
        self.drawscale = n
        return self

    def setofname(self, name):
        self.ofname = name
        return self

    def setnimages(self, n):
        self.nimages = n
        return self

    def settestsplit(self, r):  # this is the ratio of test images to total images generated
        self.testsplit = np.float16(r)
        return self

    def setkickstrength(self,x):
        self.kickstrength = np.float16(x)
        return self

    def setkickstrengthvar(self,x):
        self.kickstrengthvar = np.float16(x)
        return self

    def setdarkscale(self, r):  # this is the level of dark counts (this doesn't scale with intensity)
        self.darkscale = r
        return self

    def setsecondaryscale(self, r):  # this is the level of secondary electron counts (this does scale with intensity) that scale with x-ray intensity
        self.secondaryscale = r
        return self

    def setcentralenergy(self,x):    #setting the x-ray central energy (for now above retardation)
        self.centralenergy = x 
        return self

    def setcentralenergywidth(self,x):  # setting the gaussian width of the x-ray central energy spectrum
        self.centralenergywidth = x
        return self

    def setcentralenergyvar(self,x):  # setting the full width of the distribution of x-ray central energies 
        self.centralenergywidth = x
        return self

    def setsasescale(self,x):   # setting the number of SASE spikes in a given "assumed" gaussian distribution
        self.sasescale = x
        return self

    def setsasewidth(self,x):
        self.sasesidth = x
        return self

    def setcenters(self,x):
        self.sasecenters = x
        return self

    def setphases(self,x):
        self.sasephases = x
        return self

    def setamps(self,x):
        self.saseamps = x
        return self

    def setpoldirections(self,x): # this is a list of the directions of the major axis of the ellipse, from 0 to pi, this should be sasecenters long
        self.poldirections = x
        return self

    def setfixedlinear(self):
        self.fixedlinear = True 
        return self

    def setcircular(self):
        self.iscirc = True
        return self

    def setpolstrengths(self,x): # this is the strength of the polarization anisotropy, i.e. 0 for pure circular and 1 for pure linear
        self.polstrengths = x
        return self

    def getsecondaryscale(self):
        return self.secondaryscale

    def getdarkscale(self):
        return self.darkscale

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

    def getcentralenegy(self):
        return self.centralenergy 

    def getcentralenergywidth(self):
        return self.centralenergywidth

    def getcentralenergyvar(self):
        return self.centralenergyvar

    def getsasescale(self):
        return self.sasescale

    def getsasewidth(self):
        return self.sasesidth

    def getcenters(self):
        return self.sasecenters

    def getphases(self):
        return self.sasephases

    def getamps(self):
        return self.saseamps

    def getkickstrength(self):
        return self.kickstrength

    def getpoldirections(self):
        return self.poldirections

    def getpolstrengths(self):
        return self.polstrengths



def runprocess(params):
    nimages = params.nimages
    tstring = '%.9f' % (time.clock_gettime(time.CLOCK_REALTIME))
    keyhash = hashlib.sha1(bytearray(map(ord, tstring)))
    # HERE HERE HERE build the string for interpreting the leadning zeros based on the nthreads from run_simulation.
    with h5py.File('%s/%s.%s.%03i.h5'%(params.ofpath,params.ofname,platform.node(),params.tid), 'a') as f:
        for i in range(nimages):
            bs = bytearray(map(ord, 'shot_%i_' % i))
            keyhash.update(bs)
            key = keyhash.hexdigest()
            grp = f.create_group(key)
            X, Y = build_XY(params)
            grp.create_dataset('Ypdf', data=Y, dtype=np.float32)
            hitsvec = []
            nedges = []
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
            grp.create_dataset('Xaddresses', data=addresses, dtype=np.uint32)
            grp.create_dataset('Xnedges', data=nedges, dtype=np.uint16)
            grp.attrs.create('nangles', params.nangles,dtype=np.uint8)
            grp.attrs.create('nenergies', params.nenergies,dtype=np.uint8)
            grp.attrs.create('drawscale', params.drawscale,dtype=np.float16)
            grp.attrs.create('darkscale', params.darkscale,dtype=np.float16)
            grp.attrs.create('secondaryscale', params.secondaryscale,dtype=np.float16)
            grp.attrs.create('centralenergy', params.centralenergy,dtype=np.float16)
            grp.attrs.create('centralenergywidth', params.centralenergywidth,dtype=np.float16)
            grp.attrs.create('centralenergyvar', params.centralenergyvar,dtype=np.float16)
            grp.attrs.create('sasewidth', params.sasewidth,dtype=np.float16)
            grp.attrs.create('sasescale', params.sasescale,dtype=np.uint8)
            grp.attrs.create('sasecenters', params.sasecenters,dtype=np.float16)
            grp.attrs.create('sasephases', params.sasephases,dtype=np.float16)
            grp.attrs.create('saseamps', params.saseamps,dtype=np.float16)
            grp.attrs.create('poldirections', params.poldirections,dtype=np.float16)
            grp.attrs.create('polstrengths', params.polstrengths,dtype=np.float16)
            grp.attrs.create('kickstrength', params.kickstrength,dtype=np.float16)

            img = np.zeros((params.nangles,params.nenergies), dtype=np.uint16)
            words = []
            overcounts = []

            for a in range(grp.attrs['nangles']):
                offset = grp['Xaddresses'][()][a]
                nhits = grp['Xnedges'][()][a]
                img[a,:] += np.histogram(hitsvec[offset:offset+nhits], np.arange(params.nenergies + 1))[0].astype(np.uint16)
                w,o = be.encode(hitsvec[offset:offset+nhits], (params.nenergies//params.baseencode + 1)* params.baseencode)
                words += [w]
                overcounts += [o]
            grp.create_dataset('Ximg', data=img, dtype=np.uint16)
            grp.create_dataset('words', data=np.row_stack(words),dtype=np.uint64)
            grp.create_dataset('overcounts', data=overcounts,dtype=np.uint16)
            grp['words'].attrs['baseencode'] = params.baseencode

            grp.attrs.create('Test', False)
            grp.attrs.create('Train', False)
            if params.rng.uniform() < params.testsplit:
                grp.attrs['Test'] = True
            else:
                grp.attrs['Train'] = True

    return

def build_XY(params):
    rng = params.rng
    x = np.arange(params.nenergies,dtype=float)
    kickstrength = rng.normal(params.kickstrength,params.kickstrengthvar)
    ncenters = rng.poisson(params.sasescale)
    params.setcenters( list(rng.normal(params.centralenergy,params.centralenergyvar,ncenters)) )
    params.setphases( list(rng.random(ncenters)*2.*np.pi) )
    params.setamps( [rng.poisson(10)/10 for i in range(ncenters)] )
    if params.iscirc:
        params.setpolstrengths([0.0]*ncenters)
        params.setpoldirections([0.0]*ncenters)
    else:
        params.setpolstrengths(list(rng.random(ncenters)))
        if params.fixedlinear:
            params.setpoldirections([0.0]*ncenters)
        else:
            params.setpoldirections(list(rng.random(ncenters)*np.pi))
    bgmat = params.darkscale * np.ones((params.nangles,x.shape[0]),dtype=float)
    ymat = np.zeros((params.nangles,x.shape[0]),dtype=float)
    if ncenters>0:
        bgmat += float(params.secondaryscale)*np.sum(params.saseamps)/float(len(params.saseamps)) #* np.ones((params.nangles,x.shape[0]),dtype=float)
    for i,c in enumerate(params.sasecenters):
        for a in range(params.nangles):
            pol = 0.5*(1. + params.polstrengths[i]*np.cos(a*4.*np.pi/params.nangles + params.poldirections[i]) )
            if params.streaking:
                kick = kickstrength*np.cos(a*2.*np.pi/params.nangles + params.sasephases[i])
                ymat[a,:] += params.saseamps[i]* pol * utils.cossq( x , params.sasewidth , c + kick ) # this produces the 2D PDF
            else:
                ymat[a,:] += params.saseamps[i]* pol * utils.cossq( x , params.sasewidth , c) # this produces the 2D PDF

    cmat = np.cumsum(ymat + bgmat,axis=1)
    # the number of draws for each angle should be proportional to the total sum of that angle
    hits = []
    for a in range(params.nangles):
        cum = cmat[a,-1]
        draws = np.uint16(params.drawscale*cum)
        drawpoints = np.sort(rng.random(draws))
        if cum>0:
            hits.append(list(np.interp(drawpoints,cmat[a,:]/cum,x)))
        else:
            hits.append([])
    return hits,ymat

