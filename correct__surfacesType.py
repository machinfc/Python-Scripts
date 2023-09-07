# This script corrects the SurfaceType for misclassifications by the "train_classifier.py" script for multiple files and exports their observables.
import csv
import os
import numexpr as ne
from craterslab.craters import Surface
from craterslab.sensors import DepthMap
from craterslab.classification import SurfaceType

wrongly_classified = [
    ("fluized_9.npz", SurfaceType.COMPLEX_CRATER),
    ("fluized_12.npz", SurfaceType.COMPLEX_CRATER),
    ("fluized_26.npz", SurfaceType.SIMPLE_CRATER),
    ("fluized_27.npz", SurfaceType.SIMPLE_CRATER),
    ("fluized_29.npz", SurfaceType.SIMPLE_CRATER),
    ("fluized_31.npz", SurfaceType.SIMPLE_CRATER),
    ("fluized_35.npz", SurfaceType.SIMPLE_CRATER),
    ("fluized_39.npz", SurfaceType.COMPLEX_CRATER),
    ("fluized_44.npz", SurfaceType.COMPLEX_CRATER),
    ("fluized_45.npz", SurfaceType.COMPLEX_CRATER),
    ] 

output_folder = 'output_observables'

# Crear la carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

META_DATA = ["filename", "type"]
ALL_OBSERVABLES = ["D", "d_max", "V_in", "V_ex",
                   "V_exc", "epsilon"]
DEFAULT_OBS_VAL = -1
# Definir el nombre del archivo de salida de observables
OBSERVABLES_OUTPUT_FILE = os.path.join(
    output_folder, f'obs_output_correctedS.Type_fluized.csv')  # Ruta completa al archivo


data = []
for filename, s_type in wrongly_classified:
    print(f'Analyzing file {filename}')
    depth_map = DepthMap.load(f'data/data_Fluized_sand/{filename}')
    depth_map.auto_crop()
    s = Surface(depth_map)
    s.set_type(s_type)
    surface_data = [filename, s.type]
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

    # Write the headers
    writer.writerow(headers)

    # Write the data by columns
    for row in data:
        writer.writerow(row)
