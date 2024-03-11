from aiml_virtual.object import Radar
import numpy as np


def parentheses_contents(string: str):
    stack = []
    for i, c in enumerate(string):
        if c == '[':
            stack.append(i)
        elif c == ']' and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])

class DroneParams:

    def __init__(self, size: np.array, position_idx: int, safe_sphere_radius: float) -> None:
        self.size = size
        self.position_idx = position_idx
        self.safe_sphere_radius = safe_sphere_radius


class RadarScenario:

    def __init__(self, sim_volume_size=np.array((0.0, 0.0, 0.0)), mountain_height=0.0, height_map_name="",
                 target_point_list=np.array(((0., 0., 0.), (0., 0., 0.))),
                 drone_param_list=[DroneParams(np.array((0.1, 0.1, 0.1)), 0, 0.0)],
                 radar_list=[Radar(np.array((0.0, 0.0, 0.0)), 1.0, 1.0, 50, 60)]) -> None:
        
        self.sim_volume_size = sim_volume_size
        self.mountain_height = mountain_height
        self.height_map_name = height_map_name
        self.target_point_list = target_point_list
        self.drone_param_list = drone_param_list
        self.radar_list = radar_list

    @staticmethod
    def parse_config_file(full_filename: str) -> "RadarScenario":

        file = open(full_filename,'r')

        line = file.readline().split('#')[0].strip()

        split_line = line.split(' ')

        volume_x = float(split_line[1])
        volume_y = float(split_line[3])
        volume_z = float(split_line[5])

        volume_size = np.array((volume_x, volume_y, volume_z))

        line = file.readline().split('#')[0].strip()

        split_line = line.split(' ')

        mountain_height = float(split_line[1])

        line = file.readline().split('#')[0].strip()
        
        height_map_filename = line

        line = file.readline().split('#')[0].strip()[1:-2]

        split_line = line.split("] ")

        target_point_list = []

        for s in split_line:
            point = np.fromstring(s[1:], sep=' ')
            target_point_list += [point]
        

        line = file.readline().split('#')[0].strip()

        drone_param_list = []
        
        for l in list(parentheses_contents(line)):
            if l[0] == 1:
                split_dp = l[1][1:-1].split('] [')

                size = np.fromstring(split_dp[0], sep=' ')
                position_idx = int(split_dp[1])
                safe_sphere_radius = float(split_dp[2])

                drone_param_list += [DroneParams(size, position_idx, safe_sphere_radius)]


        line = file.readline().split('#')[0].strip()

        radar_list = []

        for l in list(parentheses_contents(line)):

            if l[0] == 1:
                split_r = l[1][1:-1].split('] [')

                pos = np.fromstring(split_r[0], sep=' ')
                a = float(split_r[1])
                exp = float(split_r[2])
                height_scale = float(split_r[3])
                tilt = float(split_r[4])    

                radar_list += [Radar(pos, a, exp, 50, 60, height_scale, tilt, display_lobe=True)]


        return RadarScenario(volume_size, mountain_height, height_map_filename,
                             target_point_list, drone_param_list, radar_list)