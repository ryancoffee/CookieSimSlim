
## CookieSimSlim  
===============  
Slim simulator for LCLS-SLAC CookieBox detector  

The basic interface is to run wither the full or the simple scripts... editing to change the output file directory...  
```bash
./runsimple.bash
```
but this still gives an overflow warning... I can't yet figure that out.  
But the full simulation is similarly  
```bash
./runfull.bash
```

## Driving directly  
Give only the -ofname arguement for the default run.  
```bash  
./src/run_sim.py -ofname /home/user/herigo/withmydata/somewhere.h5
```  


And this is if you want control for something other than 50000 images/file and 20 files.  
```bash
./src/run_sim.py -ofname <outfilename.h5> -n_images <nimages> -n_threads <nthreads>    
```

An example of running this for a simple test on two threads with 128 angle channels and 10 images each thread is as follows,
which in principle should be run as a script:  
```bash  
opath=~/data/h5files  
mkdir -p ${opath}  
outfile=${opath}/test.h5  
./src/run_sim.py -ofname $outfle -n_threads 2 -n_images 10 
```  


.h5 file structure: (assuming 64 angles and 128 energy bins)  
* image	-- still setting the key as a hash... avoiding collision since could be adding images to existing file.... though really unlikely since using PID in filename to avoid fileaccess collisions.
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
nthreads=2
./src/run_sim.py -ofname ~/data/h5files/slac_cbsim.h5 -n_threads $nthreads -n_images $nimgs
for tid in `seq 0 $nthread`; do
	./src/images2ascii.py -ifname ~/data/h5files/newmainbranch.$tid.h5 -ofpath ~/data/ascii -n_images $nimgs
	for im in `seq 0 3`; do
	gnuplot -c ./figs/plotting.sample_Ximg.gnuplot /home/coffee/data/ascii/newmainbranch.$tid.Ximg00$im.ascii /home/coffee/data/ascii/newmainbranch.$tid.Ypdf00$im.ascii figs/sampleimg.$im.png
	done
done
```


