#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt

def logisticchoice(r=3.2,iterations=1<<4):
    if r<0:
        r = 0.
    if r >4:
        r = 4.

    x = np.random.rand()
    for i in range(iterations):
        y = 1-x
        x *= r*y
    return x

def main():
    r = float(sys.argv[1])
    nsamples = int(sys.argv[2])
    niterations = int(sys.argv[3])

    numtoplot = nsamples>>1
    lims = np.zeros(nsamples)

    fig,ax = plt.subplots()
    fig.set_size_inches(16, 9)

    xlist = []
    while len(xlist)<nsamples:
        xlist += [logisticchoice(r=float(sys.argv[1]),iterations=32)]
    h,b = np.histogram(xlist,1<<10)
    bincenters = (b[:-1]+b[1:])/2.
    ax.plot(bincenters,h,'.')
    ax.set(xlabel='distribution [x]', ylabel='counts', title='histogram of logistic at r = %.3f'%r)
    #ax.legend('r = %.3f'%r,loc='upper left')
    plt.savefig('histlogisticchoice_%i_%i_%s.png'%(nsamples,niterations,sys.argv[1]))
    plt.show()
    return

if __name__ == '__main__':
    if len(sys.argv)<4:
        print('./logisticchoice.py <r> <nsamples> <interations> ')
        print('r = 2.8: 0.642800 < x < 0.642929')

        print('r = 3.0: 0.62700 < x < 0.702482')
    else:
        main()
