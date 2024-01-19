# This script manually extracts a new profile, exports its distance and height values,
# and displays its slopes for a single file.

import os
import csv

from craterslab.craters import Surface
from craterslab.sensors import DepthMap
from craterslab.profiles import Profile
from craterslab.ellipse import EllipticalModel
from craterslab.visuals import plot_2D, plot_3D, plot_profile

# Define the input filename
filename = 'data/data_Fluized/fluized_35.npz'

# Load the depth map and perform auto-cropping
depth_map = DepthMap.load(filename)
depth_map.auto_crop()

# Fit an elliptical model to the depth map
em = EllipticalModel(depth_map, 20)

# Create a profile automatically
p = em.max_profile()

# Create a new profile manually
# p = Profile(depth_map, start_point=(107, 146), end_point=(5, 60))

# Calculate slopes for the profile
m1, m2 = p.slopes()

# Print the computed slopes
print(f'Computed slopes {m1=} {m2=}')

# Plot 3D visualization
plot_3D(depth_map, profile=p, ellipse=em, preview_scale=(1, 1, 4))

# Plot 2D visualization
plot_2D(depth_map, profile=p, ellipse=em)

# Plot the profile with slopes
plot_profile(p, draw_slopes=True, block=True)

# Create an output folder for the CSV file
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist

# Generate the output filename using the input filename
output_filename = os.path.join(output_folder, f'{os.path.basename(filename).replace(".npz", "")}_profileFixer.csv')

data = [["Distance (s)", "Height (h)"]]
for s, h in zip(p.s, p.h):
    data.append([s, h])

# Open the file for writing
with open(output_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the data by rows
    for row in data:
        writer.writerow(row)
