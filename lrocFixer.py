# Load a point cloud from an .xyz file containing data from lroc.
# Then, analyze the crater using craterslab functionalities.
# We can perform visualizations, profiles, fix bad ellipse fitting, correct wrongly Surface Type classification,
# print its observables, and export the crater's profile.

import os
import csv

from craterslab.sensors import DepthMap, SensorResolution
from craterslab.visuals import plot_2D, plot_3D, plot_profile
from craterslab.ellipse import EllipseVisualConfig
from craterslab.craters import Surface
from craterslab.classification import SurfaceType
from craterslab.profiles import Profile

CORRECT_CLASS = SurfaceType.COMPLEX_CRATER

# Metadata 
META_DATA = ["filename", "type"]
ALL_OBSERVABLES = ["D", "d_max", "d_exc","mean_h_rim", "V_in","V_ex", "V_exc", "V_cp","H_cp","epsilon" ] 
DEFAULT_OBS_VAL = -1

# Define sensor resolution
data_resolution = SensorResolution(230.5852, 230.5852, 1.0, "m")

# Define data sources
depth_map = DepthMap.from_xyz_file(
    "depthMap_1.xyz", data_folder="data/data_QuickMap", resolution=data_resolution, z_shift=0
)
# # crop map functions
# depth_map.auto_crop()

depth_map.crop_borders(ratio=0.25)

# bounding_box = (80, 90, 380, 320)
# depth_map.crop(bounding_box)

# Create a surface object from the depth map
s = Surface(depth_map, ellipse_points=20)

 # Set the corrected surface type
s.set_type(surface_type=CORRECT_CLASS)

# # Create a profile automatically
p = s.max_profile

# Create a new profile manually
# p = Profile(depth_map, start_point=(23, 18), end_point=(306, 300))

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

# Produce the plots # profile=p (manual profile) # profile=s.max_profile (automatic profile)
plot_3D(depth_map, ellipse=s.em, preview_scale=(1, 1, 4))
plot_2D(depth_map,profile=s.max_profile, ellipse=s.em) #profile=p manual profile
plot_profile(p, draw_slopes=True, block=True) 


# # Print all the observables in Surface computed for the crater
print(s)

# Print ALL_OBSERVABLES computed for the crater
for o in ALL_OBSERVABLES:
    if o in s.observables:
        print(f"{o}: {s.observables[o].value}")
    else:
        print(f"{o} not found")

print(f'Computed slopes {m1=} {m2=}')
# print(f'Height: {s.max_profile.h}')
# print(f'Distance: {s.max_profile.s}')

# Define the output folder path
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist

# Define the output file path for height and distance values of profile.
output_filename = os.path.join(output_folder, 'profile_lrocFixer.csv')

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