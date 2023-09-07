# Compute the observables from the surfaces detected across multiple depth maps and save the profile section, along with distance and height values from the auto diameter.
# Please note that this script does not correct misclassifications caused by the "train_classifier.py" script or inaccurate ellipse fitting.

import csv
import os
import numexpr as ne
from craterslab.craters import Surface
from craterslab.sensors import DepthMap

os.environ["NUMEXPR_MAX_THREADS"] = str(ne.detect_number_of_cores())

output_folder = 'output_observables'
os.makedirs(output_folder, exist_ok=True)  # Crear la carpeta de salida si no existe

META_DATA = ["filename", "type"]
ALL_OBSERVABLES = ["D", "d_max", "V_in", "V_ex", "V_exc", "epsilon", "V_cp", "H_cp"]      #"V_cp", "H_cp", 'm1', 'm2'
DEFAULT_OBS_VAL = -1
# Definir el nombre del archivo de salida de observables
OBSERVABLES_OUTPUT_FILE = os.path.join(output_folder, f'obs_output.csv')  # Ruta completa al archivo


data = []
for index in range(1, 52):
    print(f'Analyzing file {index}')
    filename = f"fluized_{index}.npz"
    depth_map = DepthMap.load(f'data/data_Fluized_sand/{filename}')
    depth_map.auto_crop()
    s = Surface(depth_map)
    surface_data = [filename, s.type]
    for o in ALL_OBSERVABLES:
        if o in s.observables:
            surface_data.append(s.observables[o].value)
        else:
            surface_data.append(DEFAULT_OBS_VAL)
    data.append(surface_data)

    # # Save profile data to file
    # profile_file = os.path.join(output_folder, filename.replace('.npz', '_profile.csv'))    
    # with open(profile_file, 'w', newline='') as csvfile:
    #     headers = ["Distance (s)", "Height (h)"]
    #     writer = csv.writer(csvfile)

    #     # Write the headers
    #     writer.writerow(headers)
    #     p_data = [s.max_profile.s, s.max_profile.h]

    #     # Write the data by columns
    #     for row in zip(*p_data):
    #         writer.writerow(row)

headers = META_DATA + ALL_OBSERVABLES

# Open the file for writing
with open(OBSERVABLES_OUTPUT_FILE, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the headers
    writer.writerow(headers)

    # Write the data by rows
    for row in data:
        writer.writerow(row)






