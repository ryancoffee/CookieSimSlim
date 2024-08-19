#!/usr/bin/python3

import sys
import os
import re
import h5py
import numpy as np
import matplotlib.pyplot as plt
import math
import time

from utils import gauss,addGauss2d,addGauss2d_padding_10

DISTRIBUTIONS = True
#NSHOTS = 1<<10
NSHOTS = 1<<3
TEPROD = 1.62
TWIN=4./.3 #4 micron streaking/(.3microns/fs)
EWIN=100. #100 eV window
THRESH = 10

def kernConv1d(kmat,xmat):
    res = np.zeros(xmat.shape[1],dtype=float)
    ind = 0
    rmax = 0
    vmax = 0.
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
    vmax = 0.
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
    for r in range(kern.shape[0]):
        w = width 
        c = float(kern.shape[0]>>1) + strength * np.sin(r*2*np.pi/float(kern.shape[0]))
        kern[r,:] = gauss(np.arange(kern.shape[1]),w,c)
    #norm = math.sqrt(np.sum(kern))
    norm = math.sqrt(np.inner(kern.flatten(),kern.flatten()))
    return kern/norm

def main(fname,plotting=False):
    rng = np.random.default_rng()
    print('For now assuming 4 micron wavelength streading for a 13 fs temporal window')
    print('For now also assuming 100eV for the energy window regardless of sampling')
    print('.1eV = 100fs, 1eV = 10fs, (30nm width @ 800nm) 50meV = 33fs gives time-bandwidth product dE[eV]*dt[fs] = %f'%TEPROD)
    runtimes = []
    with h5py.File(fname,'r') as f:
        shotkeys = [k for k in f.keys() if len(f[k].attrs['sasecenters'])>1]
        rng.shuffle(shotkeys)
        oname = fname + '.tempout.h5'
        m = re.search('^(.*/)(\w+.+\.\d+)\.h5',fname)
        if m:
            oname = m.group(2) + '.confusion.h5'
            opath = m.group(1) + 'output/'
            if not os.path.exists(opath):
                os.mkdir(opath)
        else:
            print('using default output file in current directory')

        temat = np.zeros(f[shotkeys[0]]['Ximg'].shape,dtype=float)
        tedist = np.zeros((f[shotkeys[0]]['Ximg'].shape[0]+10,f[shotkeys[0]]['Ximg'].shape[1]+10),dtype=float)

        with h5py.File(opath + '/' + oname,'w') as o:
            if 'shotkeys' in o.keys():
                o['true'].attrs['hist'] = np.zeros((1<<4),dtype=np.uint16)
                o['80pct']=np.zeros((1<<4,1<<4),dtype=np.uint16)
                o['40pct']=np.zeros((1<<4,1<<4),dtype=np.uint16)
                o['20pct']=np.zeros((1<<4,1<<4),dtype=np.uint16)
                o['10pct']=np.zeros((1<<4,1<<4),dtype=np.uint16)
                o['05pct']=np.zeros((1<<4,1<<4),dtype=np.uint16)
                o['02pct']=np.zeros((1<<4,1<<4),dtype=np.uint16)
                o['01pct']=np.zeros((1<<4,1<<4),dtype=np.uint16)
                o['shotkeys']=shotkeys[:NSHOTS]
                o['coeffhist']=np.zeros((1<<7),dtype=np.uint32)
                o['coeffbins']=np.arange((1<<7)+1,dtype=float)/float(1<<7)
            else: 
                o.create_group('true')
                o['true'].attrs.create('hist',data = np.zeros((1<<4),dtype=np.uint16))
                o.create_dataset('80pct',data = np.zeros((1<<4,1<<4),dtype=np.uint16))
                o.create_dataset('40pct',data = np.zeros((1<<4,1<<4),dtype=np.uint16))
                o.create_dataset('20pct',data = np.zeros((1<<4,1<<4),dtype=np.uint16))
                o.create_dataset('10pct',data = np.zeros((1<<4,1<<4),dtype=np.uint16))
                o.create_dataset('05pct',data = np.zeros((1<<4,1<<4),dtype=np.uint16))
                o.create_dataset('02pct',data = np.zeros((1<<4,1<<4),dtype=np.uint16))
                o.create_dataset('01pct',data = np.zeros((1<<4,1<<4),dtype=np.uint16))
                o.create_dataset('shotkeys',data = shotkeys[:NSHOTS])
                o.create_dataset('coeffhist',data = np.zeros(1<<7,dtype=np.uint32))
                o.create_dataset('coeffbins',data = np.arange((1<<7)+1,dtype=float)/float(1<<7))

            coefflist = []
            nsase={'true':0}
            for p in o.keys():
                if re.search('\d+pct',p):
                    nsase[p]=0
                    if 'hist' in o[p].attrs.keys():
                        o[p]['hist'] = np.zeros((1<<4),dtype=np.uint16)
                    else:
                        o[p].attrs.create('hist',data = np.zeros((1<<4),dtype=np.uint16))

            for k in shotkeys[:NSHOTS]:
                temat = np.zeros(f[shotkeys[0]]['Ximg'].shape,dtype=float)
                tedist = np.zeros((f[shotkeys[0]]['Ximg'].shape[0]+10,f[shotkeys[0]]['Ximg'].shape[1]+10),dtype=float)

                t0 = time.time()

                nsase={'true':0}
                for p in o.keys():
                    if re.search('\d+pct',p):
                        nsase[p]=0

                nsase['true'] = f[k].attrs['sasecenters'].shape[0]
                if nsase['true']>2:
                    print('skipping nsase = %i'%(nsase['true']))
                    continue
                x = np.copy(f[k]['Ximg'][()]).astype(int) # deep copy to preserve original
                y = np.copy(f[k]['Ypdf'][()]).astype(float) # deep copy to preserve original
                tstep = TWIN/x.shape[0]
                estep = EWIN/x.shape[1]
                wlist = f[k].attrs['sasewidth']*estep*np.arange(.25,1.75,.125,dtype=float)
                #print(wlist)
                slist = f[k].attrs['kickstrength']*np.arange(.25,2,.125,dtype=float)
                #print(slist)
                kern = np.zeros(x.shape,dtype=float)

                estep=EWIN/float(tedist.shape[1])
                tstep=TWIN/float(tedist.shape[0])
        
                clow=0
                chigh=20
                if plotting:
                    fig,axs = plt.subplots(3,4)
    
                    #axs[0][0].imshow(proj,origin='lower') 
                    #axs[0][0].set_title('st%.1f, wd%.1f, v%.1f'%(stref,wdref,vref))
                    axs[0][0].pcolor(x)#,vmin=clow,vmax=chigh)
                    #axs[0][0].imshow(x,origin='lower',vmin=clow,vmax=chigh)
                    axs[0][0].set_title('Ximg')

                cmax = 1.0
                cthis = 1.0
                for i in range(5):
                    indref,rowref,stref,ewidth,vref = scanKernel(wlist,slist,x)
                    if i==0:
                        cmax = vref
                    kern = fillKernel(width=ewidth,strength=stref,kern=kern)
                    twidth=float(TEPROD)/ewidth
    
                    proj = np.roll(np.roll(kern,-indref,axis=0),rowref,axis=1)
                    coeff = np.inner(x.flatten(),proj.flatten())
                    coefflist += [coeff]
                    cthis = coeff
                    if cthis > THRESH:
                        rat = cthis/cmax
                    
                        if rat > 0.8:
                            nsase['80pct'] += 1;
                        if rat > 0.4:
                            nsase['40pct'] += 1;
                        if rat > 0.2:
                            nsase['20pct'] += 1;
                        if rat > 0.1:
                            nsase['10pct'] += 1;
                        if rat > 0.05:
                            nsase['05pct'] += 1;
                        if rat > 0.02:
                            nsase['02pct'] += 1;
                        if rat > 0.01:
                            nsase['01pct'] += 1;
    
                        x -= (coeff*proj).astype(int)

                        if plotting:
                            #axs[(i+1)//4][(i+1)%4].imshow(x,vmin=clow,vmax=chigh,origin='lower')
                            axs[(i+1)//4][(i+1)%4].pcolor(x)#,vmin=clow,vmax=chigh)
                            axs[(i+1)//4][(i+1)%4].set_title('rm_%i'%i)
                    
                    if DISTRIBUTIONS:

                        #temat[(indref+(temat.shape[1]>>1))%temat.shape[1],
                        #        (rowref+(temat.shape[0]>>1))%temat.shape[0]] += coeff
                        #addGauss2d_padding_10(tedist,coeff,(rowref+(tedist.shape[0]>>1))%tedist.shape[0],(indref+(tedist.shape[1]>>1))%tedist.shape[1],ewidth/estep,twidth/tstep)
                        temat[(indref+(temat.shape[0]>>1))%temat.shape[0],
                                (rowref+(temat.shape[1]>>1))%temat.shape[1]] += coeff
                        addGauss2d_padding_10(tedist,coeff,(rowref+(tedist.shape[1]>>1))%tedist.shape[1],(indref+(tedist.shape[0]>>1))%tedist.shape[0],ewidth/estep,twidth/tstep)
    
    
                    if plotting:
                        #axs[-1][-3].imshow(tedist,origin='lower')
                        axs[-1][-3].pcolor(tedist)
                        axs[-1][-3].set_title('tedist')
                        #axs[-1][-2].imshow(temat,origin='lower')
                        axs[-1][-2].pcolor(temat)
                        #axs[-1][-2].imshow(np.roll(np.roll(temat,temat.shape[0]//2,axis=0),temat.shape[1]//2,axis=1),origin='lower')
                        axs[-1][-2].set_title('temat')
                        axs[-1][-1].pcolor(y)
                        #axs[-1][-1].imshow(y,origin='lower')
                        axs[-1][-1].set_title('Ypdf')
                if plotting:
                    plt.show()


                i = min(nsase['true'],o['true'].attrs['hist'].shape[0]-1)
                o['true'].attrs['hist'][i] += 1
                for p in nsase.keys():
                    if re.search('\d+pct',p):
                        j = min(nsase[p],o[p].shape[1]-1)
                        #print('%s:(%i %i)'%(p,i,j))
                        o[p][i,j] += 1
                        o[p].attrs['hist'][j] += 1

                t1=time.time()
                runtimes += [t1-t0]

            print('... working coefficient histogram ... ')
            h,b = np.histogram(coefflist,o['coeffhist'].shape[0])
            o['coeffhist'][()] = h
            o['coeffbins'][()] = b

    #bins = np.arange(nbins+1,dtype=float)/(nbins)*10.*1e9
    nbins = 1<<6
    print('... working runtime histogram ... ')
    h,b=np.histogram(runtimes,bins=nbins)
    _=[print('%02i.%i s:'%(int(b[i]),int((b[i]%1)*1e3)) + ' '*v+'+') for i,v in enumerate(h)]
    return

if __name__ == '__main__':
    if len(sys.argv)<2:
        print('give me a file to process')
        tedist = np.zeros((1<<7,1<<7),dtype=float)
        ewidth=2.5
        twidth=float(TEPROD)/ewidth
        estep=EWIN/float(tedist.shape[1])
        tstep=TWIN/float(tedist.shape[0])
        print(tstep,estep,twidth,ewidth,TEPROD/ewidth)
        print(tedist.shape[0]//3,tedist.shape[1]//3)
        addGauss2d(tedist,1,tedist.shape[1]//2,tedist.shape[0]//2,ewidth/estep,twidth/tstep)
        #addGauss2d(tedist,1,tedist.shape[1]//4,tedist.shape[0]//4,10,2)
        print(np.max(tedist))
        plt.imshow(tedist,origin='lower')
        plt.colorbar()
        plt.show()

    else:
        main(sys.argv[1],plotting=True)
