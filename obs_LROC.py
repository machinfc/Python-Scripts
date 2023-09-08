# Load a point cloud from an xyz file containing data from the King crater.
# Then, analyze the crater using craterslab functionalities.
# We can perform visualizations, print its observables, and export the crater's profile.

import os
import csv
import numexpr as ne

from craterslab.sensors import DepthMap, SensorResolution
from craterslab.visuals import plot_2D, plot_3D, plot_profile
from craterslab.ellipse import EllipseVisualConfig
from craterslab.ellipse import EllipticalModel
from craterslab.craters import Surface

# Set the maximum number of threads for NumExpr
os.environ["NUMEXPR_MAX_THREADS"] = str(ne.detect_number_of_cores())

# Define sensor resolution
data_resolution = SensorResolution(235.65, 235.65, 1.0, "m")

# Define data sources
depth_map = DepthMap.from_xyz_file(
    "king.xyz", data_folder="data/data_LROC", resolution=data_resolution
)
depth_map.crop_borders(ratio=0.25)

# Create a surface object from the depth map
s = Surface(depth_map)
em = EllipticalModel(depth_map, 20)
p = em.max_profile()
m1, m2 = p.slopes()

# This is the 3D graph that visually represents the values of V_in 
# with the analogy of the quantity of milliliters (ml) of water. 
ellipse_config = EllipseVisualConfig(
        color="blue", fill=True, z_val=s.observables["mean_h_rim"].value, alpha=0.5
            )

plot_3D(
        depth_map,
        ellipse=s.em,
        preview_scale=(1, 1, 4),
        ellipse_config=ellipse_config,
        block=False,
            )

# Produce the plots
plot_3D(depth_map, profile=s.max_profile, ellipse=s.em, preview_scale=(1, 1, 5))
plot_2D(depth_map, profile=s.max_profile, ellipse=s.em)
plot_profile(p, draw_slopes=True, block=True) 


# Output the observables computed for the crater
print(s)
print(f'Computed slopes {m1=} {m2=}')
# print(f'Height: {s.max_profile.h}')
# print(f'Distance: {s.max_profile.s}')

# Define the output folder path
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist

# Define the output file path for height and distance values
output_filename = os.path.join(output_folder, 'profile_LROC.csv')

# Write height and distance values to a CSV file in columns
with open(output_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write headers
    writer.writerow(["Distance (s)", "Height (h)"])
    
    # Write data in columns
    for s, h in zip(p.s, p.h): 
        writer.writerow([s, h])

# Print a message to confirm the export
print(f'Height and Distance values exported to {output_filename}')