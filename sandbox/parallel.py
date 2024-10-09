#!/usr/bin/python3
import sys
import multiprocessing as mp
import os
import numpy as np

def print_ij(x):
    print('row_%i\tcol_%i'%(int(x[0]),int(x[1])))
    return np.sum(x),np.prod(x)

def main(nproc):
    print(mp.cpu_count())
    rows = [i for i in range(nproc)]
    cols = [j for j in range(40,40+nproc)]
    grid = []
    for r in rows:
        for c in cols:
            grid += [(r,c)]

    with mp.Pool() as p:
        res = p.map(print_ij,grid)
    print(res)


    return

if __name__ == '__main__':
    if len(sys.argv)>1:
        main(int(sys.argv[1]))
    else:
        print('give me an nparallel')
