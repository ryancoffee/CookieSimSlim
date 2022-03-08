import numpy as np
from utils import testBit,setBit,getSetBits,mod2exp

storebase = int(64)

def encode(edges,sz):
    s = int(0)
    overcount = int(0)
    for e in edges:
        if testBit(s,int(e)):
            overcount += 1
        s |= 1<<int(e) #2**int(e)
    nwords = sz//storebase
    wordlist = []
    for w in range(nwords):
        wordlist += [ np.uint64(mod2exp(s,storebase)) ] ## [s%(2**storebase)]
        s >>= storebase ## s /= 2**storebase
    return wordlist,overcount

def decode(s):
    l = int(0)
    for i,v in enumerate(s):
        l |= int(v) << (i*storebase)
    return getSetBits(l)  #list(l.iter_set())

def bindist(x,y): ## so far only returns the number of different bits, not related to the earth-movers distance yet
    X = int(0)
    Y = int(0)
    for i,v in enumerate(x):
        X |= int(v)<<int(storebase*i)
    for i,v in enumerate(y):
        Y |= int(v)<<int(storebase*i)
    d = X^Y
    return bin(d).count("1")

