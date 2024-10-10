#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import h5py
import os
import sys
import re

def main():

    #allfiles = [os.listdir('/media/coffee/9C33-6BBD/CookieSimSlim_data/output/%s/'%(k)) for k in os.listdir('/media/coffee/9C33-6BBD/CookieSimSlim_data/output/')]
    nodename = os.uname()[1]
    if re.search('baratza',nodename):
        paths = ['/media/coffee/9C33-6BBD/CookieSimSlim_data/output/4in4/',
                '/media/coffee/9C33-6BBD/CookieSimSlim_data/output/16in16/',
                '/media/coffee/9C33-6BBD/CookieSimSlim_data/output/32in16/']
        labels = ['4 threads, 4 cores, single',
                '16 threads, 8 cores, hyper',
                '32 threads, 8 cores, hyper']
        '''
        baratzapath = '/media/coffee/9C33-6BBD/CookieSimSlim_data/output/4in4/'
        officepath = '/media/coffee/9C33-6BBD/CookieSimSlim_data/output/16in16/'
        officepath2 = '/media/coffee/9C33-6BBD/CookieSimSlim_data/output/32in16/'
        '''
    elif re.search('sdf',nodename):
        paths = ['/sdf/data/lcls/ds/tmo/tmox42619/scratch/CookieSimSlim_data/output/4in4/',
                '/sdf/data/lcls/ds/tmo/tmox42619/scratch/CookieSimSlim_data/output/16in16/',
                '/sdf/data/lcls/ds/tmo/tmox42619/scratch/CookieSimSlim_data/output/32in16/',
                '/sdf/data/lcls/ds/tmo/tmox42619/scratch/CookieSimSlim_data/output/1in128/'
                ]
        labels = ['4 threads, 4 cores, single',
                '16 threads, 8 cores, hyper',
                '32 threads, 8 cores, hyper',
                '8 threads, 128 cores, single'
                ]
    else:
        print('working on unfamiliar node, fillepaths likely do not exist')
        return

    xbins = np.arange(0,6.1,.05,dtype=np.float16)

    jitter = 0.0
    width = 0.025
    runtimes = []
    for l,path in enumerate(paths):
        runtimes = []
        fnames = [f for f in os.listdir(path) if re.search('16x128',f)]
        flist = [h5py.File('%s%s'%(path,f),'r') for f in fnames]
        for i,f in enumerate(flist):
            print(fnames[i])
            runtimes += list(f['runtimes'][()])
            f.close()
        plt.bar(xbins[:-1]+(jitter*((l+1)//2)*(-1**l)),np.histogram(runtimes,xbins)[0],width,label=labels[l])

    plt.xlabel('per-image runtime [s]')
    plt.ylabel('histogram [num. shots]')

    plt.legend()
    plt.savefig('./figs/runtimes_all.png')
    plt.show()


    # _ = [f.close() for f in flist]

    print('Power estimate is CPU\% * numCPUs/task * Voltage^2 * clock frequency' )
    return

if __name__ == '__main__':
    if len(sys.argv)>1:
        print('no longer using list of files')
        #main(sys.argv[1:])
    else:
        print('no longer using list of files to compile together in a figure')
        main()
