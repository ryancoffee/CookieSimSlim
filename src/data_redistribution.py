import h5py
import numpy as np
import os


number_poisson_test = 90000
directory = "/sdf/group/lcls/ds/scratch/jhirschm/MRCO_Sim_Data/CookieSimSlim_data/LargePoissonNov25/"
data_file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.h5')]
data_files = [file for file in os.listdir(directory) if file.endswith('.h5')]
for file_path in file_paths:
        with h5py.File(file_path, 'r') as h5f:
            for image_key in h5f.keys():
                npulse = h5f[image_key].attrs["sasecenters"].shape[0]
                image = h5f[image_key]["Ximg"][:]
                npulses.append(npulse)
                images.append(image)