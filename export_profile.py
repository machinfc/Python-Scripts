# This script automatically or manually computes profile sections and exports values of distance and height along the profile.
# It also exports the slopes corresponding to the chosen profile section.

import csv

from craterslab.sensors import DepthMap
from craterslab.visuals import plot_2D, plot_3D, plot_profile
from craterslab.ellipse import EllipticalModel

SLOPES_OUTPUT_FILE = "slopes.csv"

data = [["Filename", "m1", "m2"]]
for i in range(1, 52):
    filename = f'fluized_{i}.npz'
    depth_map = DepthMap.load(f'data/data_Fluized_sand/{filename}')
    depth_map.auto_crop()

    em = EllipticalModel(depth_map, 20)
    p = em.max_profile()
    m1, m2 = p.slopes()    
    data.append([filename, m1, m2])

# Open the file for writing
with open(SLOPES_OUTPUT_FILE, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the data by rows
    for row in data:
        writer.writerow(row)
