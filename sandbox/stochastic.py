#!/usr/bin/python3


import math
import numpy as np
import matplotlib.pyplot as plt

def gauss(X,Y,xc,yc,xw,yw):
    Z = np.exp(-1.0*(np.power((X-xc)/xw,int(2))+np.power((Y-yc)/yw,int(2))))
    return Z

def main():
    rng = np.random.default_rng()
    x1 = np.arange(1<<8)
    y1 = np.arange(1<<7)
    XX,YY = np.meshgrid(x1,y1)
    xc,yc,xw,yw=(32,64,8,16)
    ZZ = float(1<<8)*gauss(XX,YY,xc,yc,xw,yw)
    xc,yc,xw,yw=(70,90,16,16)
    ZZ += float(1<<7)*gauss(XX,YY,xc,yc,xw,yw)
    xc,yc,xw,yw=(100,20,16,12)
    ZZ += float((1<<8)+(1<<6))*gauss(XX,YY,xc,yc,xw,yw)
    xc,yc,xw,yw=(200,80,16,16)
    ZZ += float((1<<8)+(1<<6))*gauss(XX,YY,xc,yc,xw,yw)
    ZZ += np.ones(ZZ.shape,dtype=float)
    plt.imshow(ZZ,origin='lower')
    plt.colorbar()
    plt.show()

    RowCSum = np.cumsum(ZZ,axis=1)
    plt.imshow(RowCSum,origin='lower')
    plt.title('horizontal cumulative')
    plt.colorbar()
    plt.show()

    ColCSum = np.cumsum(ZZ,axis=0)
    plt.imshow(ColCSum,origin='lower')
    plt.title('try cross validate')
    plt.colorbar()
    plt.show()

    xlist = []
    ylist = []
    rowdim = RowCSum.shape[0]
    maxrows = np.max(RowCSum)
    for r in range(rowdim):
        vlist = list(rng.uniform(0,int(RowCSum[r,-1]),int(float(1<<8)*RowCSum[r,-1]/maxrows)))
        xlist += list(np.interp(vlist,RowCSum[r,:],x1))
        ylist += [r]*len(vlist)
    plt.plot(xlist,ylist,'.')
    plt.show()


    #then for every xval only pick one along ther vertical
    # no maybe that is wrong

    return

if __name__ == '__main__':
    main()
