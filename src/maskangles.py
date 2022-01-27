#!/usr/bin/python3

import numpy as np
import h5py
import sys
import utils
import re
import argparse

parser = argparse.ArgumentParser(description='angle masking for results of CookieBox simulator of Attosecond Angular Streaking')
parser.add_argument('-f','--ifnames',nargs='+',type=str,required=True, help='input file list')
parser.add_argument('-t','--thresh',nargs=1,type=float,required=False,default=0.01, help='input variance threshold for masking')

def main():
    args, unparsed = parser.parse_known_args()
    if len(unparsed) > 0:
        print('Unrecognized argument(s): \n%s \nProgram exiting ... ... ' % '\n'.join(unparsed))
        exit(0)
    masklist = []
    for ifname in args.ifnames:
        m = re.search('(^.*)\.(.+)\.h5',ifname)
        if not m:
            print('failed filename match for ofname = %s'%args.ifname[0])
            return
        print('%s'%(m.group(1)))
        f = h5py.File(ifname,'r')
        ids = list(f.keys())
        np.savetxt('%s.%s.exampleX.dat'%(m.group(1),m.group(2)),f[ids[0]]['Ximg'][()],fmt='%i')
        np.savetxt('%s.%s.exampleY.dat'%(m.group(1),m.group(2)),f[ids[0]]['Ypdf'][()],fmt='%.2f')

        shotmasks = []
        for k in ids:
            shotmasks += [utils.dct_1d(f[k]['Ximg'][()],axis=1)]
        masklist += [np.var(np.stack(shotmasks,axis = -1),axis=-1)]
    varmat = np.max(np.stack(masklist,axis=-1),axis=-1)
    inds = np.where(varmat>args.thresh*np.max(varmat))
    mask = np.zeros(varmat.shape,dtype=int)
    mask[inds] = 1
    np.savetxt('%s.mask.dat'%(m.group(1)),mask,fmt='%i')
    np.savetxt('%s.varmat.dat'%(m.group(1)),varmat,fmt='%.3f')


    return

if __name__ == '__main__':
    main()
