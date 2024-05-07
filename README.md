# TODO
Audrey is 16 by 128 Ximg --> npulses.  
Use python library for counting operations/clock cycles per image.  
```https://bnikolic.co.uk/blog/python/flops/2019/09/27/python-counting-events.html```  
And for NNs ```https://bnikolic.co.uk/blog/python/flops/2019/09/27/python-counting-events.html```  

# CookieSimSlim  
===============  
Getting better with FFT convolutions...  
```
res = np.fft.ifft(np.fft.fft(f[k]['Ypdf'][()],axis=1)*-1*np.flip(np.fft.fft(f[k]['Ximg'][()],axis=1),axis=1),axis=1)
```

Slim simulator for LCLS-SLAC CookieBox detector.  
Updating for 2023 revivial on S3DF.   

# Parallelism
Now I'm using mpi at home.  Usage is something like this... from directory /mnt/islands where I've moved the code as well, and using hard paths.  \
```bash
mpirun --host baratza:1,java:1,flores:1,timor:1,papua:1 /mnt/islands/CookieSimSlim/src/run_simulation.py -ofname /mnt/islands/CookieSimSlim_data/css.h5 -n_threads 8 -n_angles 128 -n_energies 128 -n_images 1024 -offset_threads 16
```  
The reason for using only one slot for the simulation is that it is itself parallel inside the node, and each thread that gets spun up by run\_sim will get its own filename and these collide if mpirun runs multiple jobs on a single node.  
Just a weird quirk of the way I parallelized first across single node and now am also playing with mpirun.  

## The Probability Distribution Function (PDF)  
Possibly need to source the conda environment via something like.

An example of running this for a simple test on two threads with 128 angle channels and 10 images each thread is as follows,  
which in principle should be run as a script (now moving this to ```./test_run.bash```):    
```bash  
opath=/sdf/scratch/${USER}/CookieSimSlim_data  
mkdir -p ${opath}  
outfile=${opath}/test.h5  
./src/run_simulation.py -ofname ${outfile} -n_threads 16 -n_images 100 -n_angles 128 -n_energies 512 -polstrength 1 -polstrengthvar 1 -centralenergy 256 -centralenergyvar 128 -kickstrength 128 -kickstrengthvar 64 -drawscale 8
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
	* words (*developmental*)  
	* attrs  
		* sasecenters = [list of sase spike energies]
		* sasephases = [list of sase spike times(sinogram phases)]
		* saseamps = [list of sase spike amplitudes]
		* nangles = 128   
		* nenergies = 512  
		* drawscale = 8 
		* darkscale = 0.001
		* secondaryscale = 0.01
		* Test = bool
		* Train = bool  
* image  
* image  


# ONLY FOR GRAPHCORE
## Collecting images
In order to make the output more managable, there is a script 
```bash
/src/collect_images -mike True -ifnames <list of .h5 filenames to process into individual Train and Test .h5 files>
```
The output should be two files per input filename, using the front of the filename from the list and segregating the Train and Test into consistently named seperate files.  
In each file, there will be a pair of datasets, one for Ytrain,Xtrain and Ytest,Xtest respectively for train and test files.  
*Please keep in mind, these output files are written into the same directory as the source data, just with the added 'Train.h5' or 'Test.h5' extensions.*  
Mike, this ```-mike True``` makes the output have the shape that you wanted, e.g. (Nimages,nangles,nenergies).  Hopefully this is right for you (e.g. old Naoufal geometry).  

What this means in practice is that when running collect\_images.py, one must supply the narrow-ish glob of input filenames, .e.g,
```bash
./src/run_simulation.py -ofname ~/data/CookieSimSlim_data/runfew.h5 -n_threads 4 -n_angles 32 -n_energies 128 -n_images 100 -drawscale 0.2
./src/collect_images.py -mike True -ifnames ~/data/CookieSimSlim_data/runfew.[01][0-9].h5
```
*Also note in example, using only 32 angles rather than square 128x128 images.*



# bitstring representation  
With the aim of moving toward transformer models like BERT or GPT-2, I have started storing also the bitstring representation of each angle.  
This is stored in the simulation output .h5 file as the key 'words' with the intention that the 'words' for a sentence and we intend to mask out words (e.g. specific angles) and then pre-train the transformer based on the loss between the actual masked words and the predicted.  
This function doesn't exist yet, but we are anticipating that we will run with bitstrings that are nenergies bits long for each angle.  
The nenergies bits are divided into a list of nenergies//64 +1 words such that each word is embedded as a 64 bit integer which is a native type available to h5py.  

In the figure we show a comparison of this decoded and plotted set-bit map along side the corresponding 'Ximg'.  
![plot](./figs/compare_images.png)
As one can see, the correspondence is excellent except for the undercounting bins that have more than one electron count in the energy bin for a given angle.  
We note that this will actually be rare for high-rate operations of hte FEL, and as well we have access to the 'overcounting' attribute for a given shot.  
The overcounting attribute will be the number of times the encode operation tried to add one to an already set bit.  
When overcounting is found, experimentally, then one would increase the resolution in energy via more nenergies for the same total energy window.  


## Reducing dimensionality  

To reduce dimensionality, using a 2D dct and taking the variance over all the keys in a single .h5 file.  Then using that variance and cutting it at the 0.01 of max variance in the dct coeffs (see ./src/testDCTresolution.py).  This mask is then used on the individual images which are then back transformed for comparison to both raw (left) and truth (right)

![plot](./figs/plotting.dctmasking.png)



