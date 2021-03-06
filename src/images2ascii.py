#!/usr/bin/python3

from utils import images2ascii
from numpy import savetxt
import re
import os

import argparse
parser = argparse.ArgumentParser(description='Inspection tool: convert h5 files to a few ascii image output files')
parser.add_argument('-ifname', type=str,required=True, help='input path and base file name')
parser.add_argument('-ofpath', type=str,required=True, help='ouptut path only, base will be taken from .h5 name')
parser.add_argument('-n_images', type=int,default=4, help='Number of images to produce')

def main():
    args, unparsed = parser.parse_known_args()
    if len(unparsed) > 0:
        print('Unrecognized argument(s): \n%s \nProgram exiting ... ... ' % '\n'.join(unparsed))
        exit(0)

    ## checking for input file and path
    m = re.search('(^.+)\/(.+)\.h5',args.ifname)
    if not m:
        print('failed filename match for ofname = %s'%args.ifname)
        return
    print('%s\t%s'%(m.group(1),m.group(2)))
    ifname_head = m.group(2)

    ## checking for output path
    if not os.path.exists(args.ofpath):
        os.makedirs(args.ofpath)

    listofXimages,listofYimages = images2ascii(args.ifname,args.n_images)
    for i in range(len(listofXimages)):
            print('%s/%s.Ximg%03i.ascii'%(args.ofpath,ifname_head,i))
            print('%s/%s.Ypdf%03i.ascii'%(args.ofpath,ifname_head,i))
            savetxt('%s/%s.Ximg%03i.ascii'%(args.ofpath,ifname_head,i),listofXimages[i],fmt='%i')
            savetxt('%s/%s.Ypdf%03i.ascii'%(args.ofpath,ifname_head,i),listofYimages[i],fmt='%.3f')

if __name__ == '__main__':
    main()
