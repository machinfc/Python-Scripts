# This script corrects the SurfaceType for misclassifications by the "train_classifier.py" script for multiple files
# and exports their observables.
# Note that it not corrects bad fitted ellipses.
import csv
import os

from craterslab.craters import Surface
from craterslab.sensors import DepthMap
from craterslab.classification import SurfaceType

# Define the files with corrected surface types
wrongly_classified = [
    ("compacted_41.npz", SurfaceType.COMPLEX_CRATER),
    ("compacted_43.npz", SurfaceType.COMPLEX_CRATER),
    ("compacted_47.npz", SurfaceType.COMPLEX_CRATER),
]

output_folder = 'output'
# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

META_DATA = ["filename", "type"]
ALL_OBSERVABLES = ["D", "d_max", "V_in", "V_ex",
                   "V_exc", "epsilon", "V_cp", "H_cp"]
DEFAULT_OBS_VAL = -1

# Define the output file path for observables
OBSERVABLES_OUTPUT_FILE = os.path.join(
    output_folder, f'compacted_obsv_S.Type.csv')  # Full path to the file

data = []
for filename, s_type in wrongly_classified:
    print(f'Analyzing file {filename}')
    depth_map = DepthMap.load(f'data/data_Compacted/{filename}')
    depth_map.auto_crop()
    s = Surface(depth_map)

    # Set the corrected surface type
    s.set_type(s_type)

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
