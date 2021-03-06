#!/usr/bin/python3

import h5py
import numpy as np
import re
import argparse

parser = argparse.ArgumentParser(description='Collects the listed h5 files into a train block of images and a test block of images.')
parser.add_argument('-ifnames', type=str,nargs='+',required=True, help='List of .h5 filenames from which to collect images.')
parser.add_argument('-mike', type=bool,required=False,default=False,help='If this is set True, then the format will be for Mike K.')

def main():
    args,unparsed = parser.parse_known_args()
    if len(unparsed) > 0:
        print('Unrecognized argument(s): \n%s \nProgram exiting ... ... ' % '\n'.join(unparsed))
        exit(0)

    for fname in args.ifnames:
        Xtrain = []
        Ytrain = []
        Xtest = []
        Ytest = []
        m = re.search('(^.*)\/(\w+.pid\d+)\.h5',fname)
        if not m:
            print('failed filename match for ofname = %s'%fname)
            return
        print('%s\t%s'%(m.group(1),m.group(2)))
        with h5py.File(fname,'r') as f:
            for shotkey in f.keys():
                shot = f[shotkey]
                if shot.attrs['Train']:
                    Xtrain += [shot['Ximg'][()]]
                    Ytrain += [shot['Ypdf'][()]]
                if shot.attrs['Test']:
                    Xtest += [shot['Ximg'][()]]
                    Ytest += [shot['Ypdf'][()]]
        ofnameTrain = '%s/%s.Train.h5'%(m.group(1),m.group(2))
        ofnameTest = '%s/%s.Test.h5'%(m.group(1),m.group(2))
        if len(Xtrain)>1:
            if args.mike:
                ax = 0
            else:
                ax = -1
            x = np.stack(Xtrain,axis=ax)
            y = np.stack(Ytrain,axis=ax)
            with h5py.File(ofnameTrain,'w') as f:
                f.create_dataset('Xtrain',data=x,dtype=np.uint8)
                f.create_dataset('Ytrain',data=y,dtype=np.float16)
        if len(Xtest)>1:
            if args.mike:
                ax = 0
            else:
                ax = -1
            x = np.stack(Xtest,axis=ax)
            y = np.stack(Ytest,axis=ax)
            with h5py.File(ofnameTest,'w') as f:
                f.create_dataset('Xtest',data=x,dtype=np.uint8)
                f.create_dataset('Ytest',data=y,dtype=np.float16)
    return

if __name__ == '__main__':
    main()
