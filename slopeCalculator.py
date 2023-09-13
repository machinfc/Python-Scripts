# This script calculates slopes automatically computed by craterslab. It enables 2D visualization and provides numerical 
# values of slopes for visual error correction.

# If you need to calculate height and depth values for profiles automatically associated with slopes, 
# please refer to lines 51-61 and 73-78.

# For manual corrections of inaccurately computed slopes and profiles, obtained automatically, use profileFixer.py.


import os
import csv

from craterslab.craters import Surface
from craterslab.sensors import DepthMap
from craterslab.ellipse import EllipticalModel
from craterslab.visuals import plot_2D, plot_profile

# Define the output folder path
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist

def compute_slopes_and_profiles(index):
    # Load the depth map
    filename = f"compacted_{index}.npz"
    depth_map = DepthMap.load(f'data/data_Compacted/{filename}')
    depth_map.auto_crop()
    
    # Compute slopes and other visualizations
    em = EllipticalModel(depth_map, 20)
    p = em.max_profile()
    m1, m2 = p.slopes()
    
    print(f'Processing file {index}')
    print(f'Computed slopes {m1=} {m2=}')
    
    # Visualize 2D profiles with slopes for error determination
    plot_2D(depth_map, profile=p, ellipse=em)
    plot_profile(p, draw_slopes=True, block=True)
    
    return filename, m1, m2

def write_slopes_to_csv(data):
    # Define the path for the slopes CSV file
    SLOPES_OUTPUT_FILE = os.path.join(output_folder, "compacted_slopes.csv")

    with open(SLOPES_OUTPUT_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write headers to the CSV file
        writer.writerow(["Filename", "m1", "m2"])
        # Write the data rows
        writer.writerows(data)

# def write_profile_to_csv(filename, s):
#     # Define the path for the profile CSV file
#     profile_file = os.path.join(output_folder, filename.replace('.npz', '_profile.csv'))
    
#     with open(profile_file, 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         # Write headers to the CSV file
#         writer.writerow(["Distance (s)", "Height (h)"])
#         # Write the profile data by columns
#         p_data = [s.max_profile.s, s.max_profile.h]
#         writer.writerows(zip(*p_data))

data = []


for i in range(25, 50):
    filename, m1, m2 = compute_slopes_and_profiles(i)
    data.append([filename, m1, m2])

# Write slopes data to a CSV file
write_slopes_to_csv(data)

# # Write profile data to CSV files
# for i in range(1, 52):
#     filename = f"fluized_{i}.npz"
#     depth_map = DepthMap.load(f'data/data_Fluized_sand/{filename}')
#     s = Surface(depth_map)
#     write_profile_to_csv(filename, s)
