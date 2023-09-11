# Fetching depth maps of laboratory experiments from Kinect sensors for craterslab observables analysis.
import os

from craterslab.sensors import DepthMap, SensorResolution
from craterslab.visuals import plot_3D

# Establish sensor resolution obtained experimentally
resolution = SensorResolution(2.8025, 2.8025, 1.0, 'mm')

# Ask if the first depth map should be taken
take_plane = input("Would you like to take the plane's depth map? (y/n): ")
if take_plane.lower() == 'y':
    # Obtain the first depth map, averaged 500 times on depth values
    plane = DepthMap.from_kinect_sensor(resolution, average_on=500)
else:
    # If 'no' is selected, terminate the code
    exit()

# Ask if the second depth map should be taken

take_impact = input("Would you like to take the impact's depth map? (y/n): ")
if take_impact.lower() == 'y':
    # Obtain the second depth map, averaged 500 times on depth values
    impact = DepthMap.from_kinect_sensor(resolution, average_on=500)
else:
    # If 'no' is selected, terminate the code
    exit()

# Subtract the second depth map from the first to get the third depth map
depth_map = impact - plane

# Visualize the resulting third depth map
plot_3D(depth_map, block=True)

# Create a folder to save the depth maps
output_folder = 'output/depth_maps'
os.makedirs(output_folder, exist_ok=True)

# Save the depth maps
# plane.save(os.path.join(output_folder, 'plane_1.npz'))
# impact.save(os.path.join(output_folder, 'impact_1.npz'))
depth_map.save(os.path.join(output_folder, 'depthMap_1.npz'))
