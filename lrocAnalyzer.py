# This script calculates observables from .xyz files for lroc data using craterslab.

# It can report incorrect crater classifications or bad fitted ellipses.
# For this reason, it allows 2D and 3D visualization of the data to find poorly fitted ellipses
# that may report incorrect observables or identify potential incorrect surface classifications.

# To correct these errors, please use lrocFixer.py

import csv
import os

from craterslab.craters import Surface
from craterslab.sensors import DepthMap

from craterslab.visuals import plot_2D, plot_3D
from craterslab.ellipse import EllipticalModel
from craterslab.sensors import DepthMap, SensorResolution

# Define the output folder path
output_folder = 'output'
# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Metadata columns for the output CSV file
META_DATA = ["filename", "type"]

# List of all observables to be calculated
ALL_OBSERVABLES = ["D", "d_max", "V_in",
                   "V_ex", "V_exc", "epsilon", "V_cp", "H_cp"]

# Default value for observables if they are not available
DEFAULT_OBS_VAL = -1

# Define the output file path for observables
OBSERVABLES_OUTPUT_FILE = os.path.join(
    output_folder, f'lroc_obsv.csv')  # Full path to the file

data = []

# Loop through the data files and calculate observables
for index in range(1, 2):
    print(f'Analyzing file {index}')
    filename = f"lroc_{index}.xyz"
    data_resolution = SensorResolution(235.65, 235.65, 1.0, "m")
    depth_map = DepthMap.from_xyz_file(filename, data_folder="data/data_QuickMap", resolution=data_resolution
                                       )

    depth_map.auto_crop()
    s = Surface(depth_map)
    surface_data = [filename, s.type]

    # Compute profile and other visualizations
    em = EllipticalModel(depth_map, 20)
    p = em.max_profile()

    print(f'Processing file {index} with type: {s.type}')

    # Visualize data in 2D and 3D
    plot_2D(depth_map, profile=p, ellipse=em)
    plot_3D(depth_map, ellipse=em, preview_scale=(1, 1, 5), block=True)

    # Calculate and append observables to the data
    for o in ALL_OBSERVABLES:
        if o in s.observables:
            surface_data.append(s.observables[o].value)
        else:
            surface_data.append(DEFAULT_OBS_VAL)

    data.append(surface_data)

# Define the headers for the CSV file
headers = META_DATA + ALL_OBSERVABLES

# Open the file for writing
with open(OBSERVABLES_OUTPUT_FILE, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the headers to the CSV file
    writer.writerow(headers)

    # Write the data rows
    for row in data:
        writer.writerow(row)
