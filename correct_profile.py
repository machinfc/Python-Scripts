from craterslab.sensors import DepthMap
from craterslab.visuals import plot_2D, plot_3D, plot_profile
from craterslab.profiles import Profile

filename = 'data/data_Fluized_sand/fluized_1.npz'

depth_map = DepthMap.load(filename)
depth_map.auto_crop()

p = Profile(depth_map, start_point=(0,0), end_point=(40, 40))
m1, m2 = p.slopes()

print(f'Computed slopes {m1=} {m2=}')

plot_3D(depth_map, profile=p, preview_scale=(1, 1, 4))
plot_2D(depth_map, profile=p)
plot_profile(p, draw_slopes=True, block=True)
