#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import h5py
import os
import sys
import re

def main():

    #allfiles = [os.listdir('/media/coffee/9C33-6BBD/CookieSimSlim_data/output/%s/'%(k)) for k in os.listdir('/media/coffee/9C33-6BBD/CookieSimSlim_data/output/')]
    baratzapath = '/media/coffee/9C33-6BBD/CookieSimSlim_data/output/4in4/'
    officepath = '/media/coffee/9C33-6BBD/CookieSimSlim_data/output/16in16/'
    officepath2 = '/media/coffee/9C33-6BBD/CookieSimSlim_data/output/32in16/'

    xbins = np.arange(0,6.1,.1,dtype=np.float16)

    runtimes = []
    fnames = [f for f in os.listdir(baratzapath) if re.search('16x128',f)]
    flist = [h5py.File('%s%s'%(baratzapath,f),'r') for f in fnames]
    for i,f in enumerate(flist):
        runtimes += list(f['runtimes'][()])
        f.close()
    plt.bar(xbins[:-1],np.histogram(runtimes,xbins)[0],0.05,label='4 threads, 4 cores, single')
    fnames = [f for f in os.listdir(baratzapath) if re.search('16x128',f)]

    runtimes = []
    fnames = [f for f in os.listdir(officepath) if re.search('16x128',f)]
    flist = [h5py.File('%s%s'%(officepath,f),'r') for f in fnames]
    for i,f in enumerate(flist):
        runtimes += list(f['runtimes'][()])
        f.close()
    plt.bar(xbins[:-1]-.0125,np.histogram(runtimes,xbins)[0],.05,label='16 threads, 8 cores, hyper')

    runtimes = []
    fnames = [f for f in os.listdir(officepath2) if re.search('16x128',f)]
    flist = [h5py.File('%s%s'%(officepath2,f),'r') for f in fnames]
    for i,f in enumerate(flist):
        runtimes += list(f['runtimes'][()])
        f.close()
    plt.bar(xbins[:-1]+.0125,np.histogram(runtimes,xbins)[0],.05,label='32 threads, 8 cores, hyper')
    plt.xlabel('per-image runtime [s]')
    plt.ylabel('histogram [num. shots]')

    plt.legend()
    plt.savefig('./figs/runtimes.png')
    plt.show()


    # _ = [f.close() for f in flist]

    print('Power estimate is CPU\% * numCPUs/tast * Voltage^2 * clock frequency' )
    return

if __name__ == '__main__':
    if len(sys.argv)>1:
        print('no longer using list of files')
        #main(sys.argv[1:])
    else:
        print('no longer using list of files to compile together in a figure')
        main()
