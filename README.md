
## CookieSimSlim  
===============  
Slim simulator for LCLS-SLAC CookieBox detector  

## The Probability Distribution Function (PDF)  

```bash  
./src/prob_dist.py -ofname <outfilename.h5> <optional> -n_images <nimages> -n_angles <nchannels> -n_threads <nthreads>    
./src/prob_dist.py -ofname /home/user/herigo/withmydata/somewhere.h5 -n_images 50000 -n_angles 128 -n_threads 20    
```  

An example of running this for a simple test on two threads with 128 angle channels and 10 images each thread is as follows,
which in principle should be run as a script:  
```bash  
opath=~/data/h5files  
mkdir -p ${opath}  
outfile=${opath}/test.h5  
./src/prob_dist.py -ofname $outfle -n_threads 2 -n_images 10 -drawscale 8 -darkscale .001 -secondaryscale .01
```  


.h5 file structure: (assuming 64 angles and 128 energy bins)  
* image	-- still setting the key as a hash to avoiding collision since could be adding images to existing file.... though really unlikely since using PID in filename to avoid fileaccess collisions.  
This may need revisiting... maybe each file update would start a new dataset with a new rngseed?
	* Xhits (N,)  
	* Xaddresses (nangles,)  
	* Xnedges (nangles,)  
	* Ximg (nangles,128)  
	* Ypdf (nangles,128)  
	* attrs  
		* nangles = 128   
		* nenergies = 128  
		* drawscale = 8 
		* darkscale = 0.001
		* secondaryscale = 0.01
		* Test = bool
		* Train = bool  
* image  
* image  

## Viewing the first few images in a given resulting .h5 file

```bash
nimgs=10
./src/prob_dist.py -ofname ~/data/h5files/mainbranch.h5 -n_threads 2 -n_images $nimgs -drawscale 8
./src/images2ascii.py -ifname ~/data/h5files/newmainbranch.rngseed1.h5 -ofpath ~/data/ascii -n_images $nimgs
im=3
gnuplot -c ./figs/plotting.sample_Ximg.gnuplot /home/coffee/data/ascii/newmainbranch.$procid.Ximg00$im.ascii /home/coffee/data/ascii/newmainbranch.$procid.Ypdf00$im.ascii figs/trythis$im.png
```
