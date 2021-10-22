
## CookieSimSlim  
===============  
Slim simulator for LCLS-SLAC CookieBox detector  

## The Probability Distribution Function (PDF)  

```bash  
./src/prob_dist.py <outfilename.h5> <nimages> <nchannels> <nthreads>  
./src/prob_dist.py <point_this_somewhere.h5> <nimages=25000> <nchannels=128> <nthreads=10>  
```  

An example of running this for a simple test on two threads with 128 angle channels and 10 images each thread is as follows,
which in principle should be run as a script:  
```bash  
opath=~/data/h5files  
mkdir -p ${opath}  
outfile=${opath}/test.h5  
./src/prob_dist.py ${outfile} 10 128 2  
```  


.h5 file structure: (assuming 64 angles and 128 energy bins)  
* image	  
	* Xhits (N,)  
	* Xaddresses (64,)  
	* Xnedges (64,)  
	* Ximg (64,128)  
	* Ypdf (64,128)  
	* attrs  
		* nangles = 64   
		* nenergies = 128  
		* drawscale = ~4 ??  
		* Test = True/False  
		* Train = True/False  
* image  
* image  



