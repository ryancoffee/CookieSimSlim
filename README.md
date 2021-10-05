# CookieSimSlim
Slim simulator for LCLS-SLAC CookieBox detector

# The Probability Distribution Function (PDF)
```bash
./src/prob_dist.py <outfilename.h5> <nimages> <nchannels> <nthreads>
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
