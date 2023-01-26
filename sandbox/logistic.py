#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt

def main():
    interval = (float(sys.argv[1]), float(sys.argv[2]) )  # start, end
    if interval[0]<0:
        interval[0] = 0.
    if interval[1] >4:
        interval[1] = 4.
    nsamplers = int(sys.argv[3])
    nsamples = int(sys.argv[4])
    niterations = int(sys.argv[5])

    numtoplot = nsamples>>1
    lims = np.zeros(nsamples)

    fig,ax = plt.subplots()
    fig.set_size_inches(16, 9)

    xlist = []
    rlist = []
    #for r in np.arange(interval[0], interval[1], step=(interval[1]-interval[0])/float(nsamplers),dtype=float):
    for r in (np.random.rand(nsamplers)*(interval[1]-interval[0])+interval[0]):
        for x in np.random.rand(nsamples):
            for i in range(niterations):
                y = 1-x
                x *= r*y
                #xnew = r*x*(1-x)
                #x = xnew
            xlist += [x]
            rlist += [r]

    ax.plot(rlist,xlist, 'k.', markersize=.01)
    ax.set(xlabel='r', ylabel='x', title='logistic map')
    plt.savefig('logistic_%.3f_%.3f_%i.png'%(interval[0],interval[1],nsamples))
    plt.show()
    return

if __name__ == '__main__':
    if len(sys.argv)<6:
        print('./logistic.py <r lowlim> <r highlim> <nsamplers> <nsamples each r> <interations>')
    else:
        main()
