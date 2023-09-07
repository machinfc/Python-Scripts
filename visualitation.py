# Load a single depth map from file, compute an elliptical model and plot
# the depth map together with the model and its max profile

from craterslab.sensors import DepthMap
from craterslab.visuals import plot_2D, plot_3D, plot_profile
from craterslab.ellipse import EllipticalModel

for i in range(1, 52):
    depth_map = DepthMap.load(f'data/data_Fluized_sand/fluized_{i}.npz')
    depth_map.auto_crop()

    em = EllipticalModel(depth_map, 20)
    p = em.max_profile()
    m1, m2 = p.slopes()
    print(f'Computed slopes {m1=} {m2=}')

    print(f'number#_{i}')
    plot_2D(depth_map, profile=p, ellipse=em)
    plot_profile(p, draw_slopes=True)
    plot_3D(depth_map, ellipse=em,profile=p, preview_scale=(1, 1, 5), block=True)




