
# CookieSimSlim  
===============  
Slim simulator for LCLS-SLAC CookieBox detector.  I am changing this now to accommodate eventually also the spectroscopy version as well as the streaking version.  For now, still concentrating on streaking though.  

## The Probability Distribution Function (PDF)  

An example of running this for a simple test on two threads with 128 angle channels and 10 images each thread is as follows,
which in principle should be run as a script:  
```bash  
opath=~/data/h5files  
mkdir -p ${opath}  
outfile=${opath}/test.h5  
./src/run_simulation.py -ofname /media/coffee/9C33-6BBD/CookieSimSlim_data/lowsig.h5 -n_threads 2 -n_images 20 -n_angles 16 -n_energies 128 -polstrength 1 -polstrengthvar 1 -centralenergy 64 -centralenergyvar 40 -kickstrengthvar 10 -drawscale 1
```  

## HDF5 file structure  
.h5 file structure: 
* image	-- still setting the key as a hash to avoiding collision since could be adding images to existing file.... though really unlikely since using PID in filename to avoid fileaccess collisions.  
This may need revisiting... maybe each file update would start a new dataset with a new rngseed?
	* Xhits (N,)  
	* Xaddresses (nangles,)  
	* Xnedges (nangles,)  
	* Ximg (nangles,128)  
	* Ypdf (nangles,128)  
	* attrs  
		* sasecenters = [list of sase spike energies]
		* sasephases = [list of sase spike times(sinogram phases)]
		* saseamps = [list of sase spike amplitudes]
		* nangles = 128   
		* nenergies = 128  
		* drawscale = 8 
		* darkscale = 0.001
		* secondaryscale = 0.01
		* Test = bool
		* Train = bool  
* image  
* image  


## Collecting images
In order to make the output more managable, there is a script 
```bash
/src/collect_images -ifnames <list of .h5 filenames to process into individual Train and Test .h5 files>
```
The output should be two files, using the front ofo the filename from the list and segregating the Train and Test into consistently named seperate files.  
In each file, there will be a pair of datasets, one for Y and another for X.

## Reducing dimensionality  

To reduce dimensionality, using a 2D dct and taking the variance over all the keys in a single .h5 file.  Then using that variance and cutting it at the 0.01 of max variance in the dct coeffs (see ./src/testDCTresolution.py).  This mask is then used on the individual images which are then back transformed for comparison to both raw (left) and truth (right)

![plot](./figs/plotting.dctmasking.png)



