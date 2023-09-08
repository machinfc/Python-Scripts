# Load depth maps from files, compute an elliptical model and plot
# the depth map together with the water model and its max profile. This script was used for export .eps graphs
# It is important to note that water model visualization doesn't work for Sand Mounds. 
import os
import numexpr as ne

from craterslab.sensors import DepthMap
from craterslab.craters import Surface
from craterslab.ellipse import EllipseVisualConfig
from craterslab.ellipse import EllipticalModel
from craterslab.visuals import plot_2D, plot_3D, plot_profile

os.environ["NUMEXPR_MAX_THREADS"] = str(ne.detect_number_of_cores())

for i in range(1, 52):
    depth_map = DepthMap.load(f'data/data_Fluidized_sand/fluized_{i}.npz')
    depth_map.auto_crop()

    em = EllipticalModel(depth_map, 20)
    p = em.max_profile()
    m1, m2 = p.slopes()
    s = Surface(depth_map)

    print(f'Processing file_{i}')

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




