#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt

def main():
    rlist = [float(v) for v in sys.argv[3:]]
    nsamples = int(sys.argv[1])
    niterations = int(sys.argv[2])

    numtoplot = nsamples>>1
    lims = np.zeros(nsamples)

    fig,ax = plt.subplots()
    fig.set_size_inches(16, 9)

    legendlist = []
    for r in rlist:
        if r<0:
            r = 0.
        if r >4:
            r = 4.
        xlist = []
        for x in np.random.rand(nsamples):
            for i in range(niterations):
                y = 1-x
                x *= r*y
            xlist += [x]
        ax.semilogy(np.histogram(xlist,1<<8)[0],'.')
        legendlist += ['r = %.4f'%r]
    ax.set(xlabel='x distribution [arb]', ylabel='counts', title='histogram of logistic')
    ax.legend(legendlist,loc='upper left')
    rjoined = '_r'+'_r'.join(v for v in sys.argv[3:])
    plt.savefig('histlogistic_%i_%i%s.png'%(nsamples,niterations,rjoined))
    plt.show()
    return

if __name__ == '__main__':
    if len(sys.argv)<4:
        print('./histlogistic.py <nsamples> <interations> <r values as list>')
    else:
        main()
