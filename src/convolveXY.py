#!/usr/bin/python3

import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt

def conv1d(xmat,ymat):
    #return np.fft.ifft(np.fft.fft(xmat,axis=1)*np.fft.fft(np.flip(ymat,axis=1),axis=1),axis=1)
    return np.fft.ifft(np.fft.fft(xmat,axis=1)*np.fft.fft(np.flip(ymat,axis=1),axis=1),axis=1)

def main(fname):
    rng = np.random.default_rng()
    with h5py.File(fname,'r') as f:
        shotkeys = [k for k in f.keys()]
        rng.shuffle(shotkeys)
        k = shotkeys[0]
        x = f[k]['Ximg'][()]
        y = f[k]['Ypdf'][()]
        fig,axs = plt.subplots(1,3)
        axs[0].plot(np.sum(conv1d(x,y).real,axis=0),label='x,y')
        axs[0].plot(np.sum(conv1d(y,y).real,axis=0),label='y,y')
        axs[1].imshow(x)
        axs[1].set_title('Ximg')
        axs[2].imshow(y)
        axs[2].set_title('Ypdf')
        plt.show()

    return

if __name__ == '__main__':
    if len(sys.argv)<2:
        print('give me a file to process')
    else:
        main(sys.argv[1])
