import h5py
import numpy as np
import os

directory = "/sdf/group/lcls/ds/scratch/jhirschm/MRCO_Sim_Data/CookieSimSlim_data/large_poisson_Nov25_2023_directory/"
poisson_subset_directory = "/sdf/group/lcls/ds/scratch/jhirschm/MRCO_Sim_Data/CookieSimSlim_data/large_poisson_Nov25_2023_directory/poisson_subset/"
even_distribution_directory = "/sdf/group/lcls/ds/scratch/jhirschm/MRCO_Sim_Data/CookieSimSlim_data/large_poisson_Nov25_2023_directory/even_distribution_subset/"
data_file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.h5')]
# data_files = [file for file in os.listdir(directory) if file.endswith('.h5')]

poisson_data_identifiers = []
remaining_identifiers = []

#Go through each file
# For each file select desired number of random images for poisson distribution set
#On same loop determine number of 0,1,2,3+ pulse images in the remaining set
number_poisson_set = int(.08*8192)
file_iterator = 0
for i,file_path in enumerate(data_file_paths):
    random_integers = np.random.randint(0, 8192 + 1, size=number_poisson_set)
    number_0 = 0
    number_1 = 0
    number_2 = 0
    number_3plus = 0
    with h5py.File(file_path, 'r') as h5f:
        save_file = os.path.join(poisson_subset_directory, "poisson_subset_%i.h5" % file_iterator)
        with h5py.File(save_file, 'a') as pois_output_h5f:
            for j,image_key in enumerate(h5f.keys()):
                npulse = h5f[image_key].attrs["sasecenters"].shape[0]
                image = h5f[image_key]

                if j in random_integers:
                    group_name = f'group_{i}_{j}'
                    pois_output_h5f.copy(h5f[image_key], group_name)
                else:
                    if npulse == 0:
                        number_0 += 1
                    elif npulse == 1:
                        number_1 += 1
                    elif npulse == 2:
                        number_2 += 1
                    else:
                        number_3plus += 1
        max_pulses = np.min([number_0, number_1, number_2, number_3plus])
        save_file = os.path.join(even_distribution_directory, "even_subset_%i.h5" % file_iterator)
        with h5py.File(save_file, 'a') as even_output_h5f:
            for j,image_key in enumerate(h5f.keys()):
                npulse = h5f[image_key].attrs["sasecenters"].shape[0]
                image = h5f[image_key]
                if j not in random_integers:
                    if npulse == 0 and number_0 < max_pulses:
                        group_name = f'group_{i}_{j}'
                        even_output_h5f.copy(h5f[image_key], group_name)
                        number_0 += 1
                    elif npulse == 1 and number_1 < max_pulses:
                        group_name = f'group_{i}_{j}'
                        even_output_h5f.copy(h5f[image_key], group_name)
                        number_1 += 1
                    elif npulse == 2 and number_2 < max_pulses:
                        group_name = f'group_{i}_{j}'
                        even_output_h5f.copy(h5f[image_key], group_name)
                        number_2 += 1
                    elif npulse > 2 and number_3plus < max_pulses:
                        group_name = f'group_{i}_{j}'
                        even_output_h5f.copy(h5f[image_key], group_name)
                        number_3plus += 1







