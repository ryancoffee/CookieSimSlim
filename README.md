
## CookieSimSlim  
===============  
Slim simulator for LCLS-SLAC CookieBox detector  

## The Probability Distribution Function (PDF)  

```bash  
./src/prob_dist.py -ofname <outfilename.h5> <optional> -n_images <nimages> -n_angles <nchannels> -n_threads <nthreads>    
./src/prob_dist.py -ofname /home/user/herigo/withmydata/somewhere.h5 -n_images 25000 -n_angles 128 -n_threads 10    
```  

An example of running this for a simple test on two threads with 128 angle channels and 10 images each thread is as follows,
which in principle should be run as a script:  
```bash  
opath=~/data/h5files  
mkdir -p ${opath}  
outfile=${opath}/test.h5  
./src/prob_dist.py -ofname ${outfile} -n_images 10 -n_angles 128 -n_threads 2  
```  


.h5 file structure: (assuming 64 angles and 128 energy bins)  
* image	-- still setting the key as a hash... avoiding collision since could be adding images to existing file.
	* Xhits (N,)  
	* Xaddresses (128,)  
	* Xnedges (128,)  
	* Ximg (128,128)  
	* Ypdf (128,128)  
	* attrs  
		* nangles = 128   
		* nenergies = 128  
		* drawscale = ~4 ??  
		* Test = True/False  
		* Train = True/False  
* image  
* image  

## Viewing the first few images in a given resulting .h5 file

```bash
./src/images2ascii.py -ifname ~/data/h5files/latest/test.3570.h5 -ofpath ~/data/ascii -n_images 3
gnuplot -c ./figs/plotting.sample_Ximg.gnuplot ~/data/ascii/test.3570.Ximg00[01].ascii ~/data/ascii/test.3570.Ypdf00[01].ascii
```


