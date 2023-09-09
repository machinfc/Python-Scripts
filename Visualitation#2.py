# This script is similar to the file Visualization.py, but it only loads a single depth map from a file and plots it.
# It is important to note that water model visualization doesn't work for Sand Mounds.
import os

from craterslab.sensors import DepthMap
from craterslab.craters import Surface
from craterslab.ellipse import EllipseVisualConfig
from craterslab.ellipse import EllipticalModel
from craterslab.visuals import plot_2D, plot_3D, plot_profile

# Load the depth map from the specified file
file_path = 'data/data_CAGEO/Figs/crater_Fig4.npz'
depth_map = DepthMap.load(file_path)
depth_map.auto_crop()

em = EllipticalModel(depth_map, 20)
p = em.max_profile()
m1, m2 = p.slopes()
s = Surface(depth_map)

# Extract the filename from the file path
file_name = os.path.basename(file_path)

# Print the file name of the depth map being processed
print(f'Processing file: {file_name}')

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
    
plot_2D(depth_map, profile=p, ellipse=em)
plot_profile(p, draw_slopes=True)
plot_3D(depth_map, ellipse=em, preview_scale=(1, 1, 4), block=True)
