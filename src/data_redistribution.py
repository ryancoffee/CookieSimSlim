import h5py
import numpy as np
import os


number_poisson_test = 90000
max_number_examples_per_output_file = 10000
output_poisson_files = number_poisson_test // number_examples_per_output_poisson_file
directory = "/sdf/group/lcls/ds/scratch/jhirschm/MRCO_Sim_Data/CookieSimSlim_data/large_poisson_Nov25_2023_directory/"
poisson_subset_directory = "/sdf/group/lcls/ds/scratch/jhirschm/MRCO_Sim_Data/CookieSimSlim_data/large_poisson_Nov25_2023_directory/poisson_subset/"
even_distribution_directory = "/sdf/group/lcls/ds/scratch/jhirschm/MRCO_Sim_Data/CookieSimSlim_data/large_poisson_Nov25_2023_directory/even_distribution_subset/"
data_file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.h5')]
# data_files = [file for file in os.listdir(directory) if file.endswith('.h5')]

poisson_data_identifiers = []
remaining_identifiers = []

# Set to keep track of selected file indices and image indices
selected_indices = set()
# Randomly select 90,000 images
while len(selected_indices) < 90000:
    file_number = np.random.randint(0, len(data_file_paths))
    image_number = np.random.randint(0, 8192)

    # Check if the pair has already been selected
    if (file_number, image_number) not in selected_indices:
        selected_indices.add((file_number, image_number))

# Convert the set to a NumPy array for indexing
selected_indices = np.array(list(selected_indices))

poisson_file_incrementer = 0
even_file_incrementer = 0
number_0 = 0
number_1 = 0
number_2 = 0
number_3plus = 0

for i,file_path in enumerate(data_file_paths):
    with h5py.File(file_path, 'r') as h5f:
        for j,image_key in enumerate(h5f.keys()):
            npulse = h5f[image_key].attrs["sasecenters"].shape[0]
            image = h5f[image_key]

            if (i,j) in selected_indices:
                save_file = os.path.join(poisson_subset_directory, "poisson_subset_%i.h5" % poisson_file_incrementer)
                with h5py.File(save_file, 'a') as h5f_selected:
                    group_name = f'group_{i}_{j}'
                    h5f_selected.copy(h5f[image_key], group_name)
                if poisson_file_incrementer == output_poisson_files:
                    poisson_file_incrementer = 0
                else:
                    poisson_file_incrementer += 1
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
number_0 = 0
number_1 = 0
number_2 = 0
number_3plus = 0

# even_selected_indices = set()
# while len(number_0) < max_pulses and len(number_1) < max_pulses and len(number_2) < max_pulses and len(number_3plus) < max_pulses:
#     file_number = np.random.randint(0, len(data_file_paths))
#     image_number = np.random.randint(0, 8192)

#     # Check if the pair has already been selected
#     if (file_number, image_number) not in even_selected_indices and (file_number, image_number) not in selected_indices:
#         even_selected_indices.add((file_number, image_number))
even_selected_indices = set()
  
for i,file_path in enumerate(data_file_paths):
    with h5py.File(file_path, 'r') as h5f:
        for j,image_key in enumerate(h5f.keys()):
            npulse = h5f[image_key].attrs["sasecenters"].shape[0]
            image = h5f[image_key]

            if (i,j) not in selected_indices and (i,j) not in even_selected_indices:
                if npulse == 0 and number_0 < max_pulses:
                    even_selected_indices.add((i,j))
                    number_0 += 1
                elif npulse == 1 and number_1 < max_pulses:
                    even_selected_indices.add((i,j))
                    number_1 += 1
                elif npulse == 2 and number_2 < max_pulses:
                    even_selected_indices.add((i,j))
                    number_2 += 1
                elif npulse > 2 and number_3plus < max_pulses:
                    even_selected_indices.add((i,j))
                    number_3plus += 1
            
