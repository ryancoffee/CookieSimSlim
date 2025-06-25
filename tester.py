import os

def check_file_exists(directory, filename):
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        print(f"The file {filename} exists in {directory}.")
    else:
        print(f"The file {filename} does not exist in {directory}.")

# Specify the directory and filename
directory = "/sdf/home/j/jhirschm/Test/"
filename = "2-Pulse_03272024.h5"

# Check if the file exists
check_file_exists(directory, filename)

import re
file = "/sdf/home/j/jhirschm/Test/2-Pulse_03272024.sh"
#m = re.search('(^.*)\/(\w+)\.sh',file)
m = re.search(r'^(.+)/(.+)\.sh$', file)
print(m)
print(m.group(1))
print(m.group(2))
