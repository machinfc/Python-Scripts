# This script converts and exports data files from .mat to .npz format.
import os
from craterslab.sensors import DepthMap, SensorResolution

folder = 'data_CAGEO\matlab_ALL.CAGEO'
output_folder = 'data_CAGEO'

os.makedirs(output_folder, exist_ok=True)  # Crear la carpeta si no existe

for i in range(1, 38):
    r = SensorResolution(2.8025, 2.8025, 1, "mm")
    d0 = DepthMap.from_mat_file(
        f"planoexp{i}.mat", data_folder=folder, resolution=r)
    df = DepthMap.from_mat_file(
        f"craterexp{i}.mat", data_folder=folder, resolution=r)
    depth_map = d0 - df

    # Generar la ruta completa para guardar el archivo .npz en la carpeta de salida
    npz_file_path = os.path.join(output_folder, f'CAGEO_{i}.npz')

    # Guardar el archivo .npz en la carpeta de salida
    depth_map.save(npz_file_path)
