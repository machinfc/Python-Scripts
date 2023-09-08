# This script corrects the SurfaceType for misclassifications caused by the "train_classifier.py" script
# and inaccurate ellipse fitting for individual files.
# It allows changing the number of points used for the ellipse fit and crop methods.
# It exports corrected observables for these two errors. It also corrects the surfaces in case of correct classification by the train_classifier.

import csv
import os

from craterslab.craters import Surface
from craterslab.sensors import DepthMap
from craterslab.visuals import plot_2D, plot_3D
from craterslab.classification import SurfaceType

filename = "fluized_30.npz"
ellipse_points = 20
correct_type = SurfaceType.COMPLEX_CRATER
# correct_type = SurfaceType.SIMPLE_CRATER
# correct_type = SurfaceType.SAND_MOUND

output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)

DEFAULT_OBS_VAL = -1
META_DATA = ["filename", "type"]
ALL_OBSERVABLES = ["D", "d_max", "V_in", "V_ex",
                   "V_exc", "epsilon", "V_cp", "H_cp"]

# Define the output file name for observables
output_name = filename.replace('.npz', '_em_corrected.csv')
OBSERVABLES_OUTPUT_FILE = os.path.join(output_folder, output_name)

data = []

print(f'Analyzing file {filename}')
depth_map = DepthMap.load(f'data/data_Fluized_sand/{filename}')

# # crop map functions
# depth_map.auto_crop()
# depth_map.crop_borders(0.7)

# Define the bounding box for cropping
bounding_box = (50, 30, 120, 90)
depth_map.crop(bounding_box)

s = Surface(depth_map, ellipse_points=ellipse_points)
s.set_type(correct_type)
plot_2D(depth_map, ellipse=s.em, block=True)
plot_3D(depth_map, ellipse=s.em, block=True)

surface_data = [filename, s.type]

# Calculate observables and append to data
for o in ALL_OBSERVABLES:
    if o in s.observables:
        surface_data.append(s.observables[o].value)
    else:
        surface_data.append(DEFAULT_OBS_VAL)

data.append(surface_data)

headers = META_DATA + ALL_OBSERVABLES

# Open the file for writing
with open(OBSERVABLES_OUTPUT_FILE, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the headers to the CSV file
    writer.writerow(headers)

    # Write the data by columns
    for row in data:
        writer.writerow(row)
