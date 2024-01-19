import os

from aiml_virtual.simulator import ActiveSimulator

from aiml_virtual.xml_generator import SceneXmlGenerator

from aiml_virtual.trajectory import CarTrajectory
from aiml_virtual.controller import CarLPVController
from aiml_virtual.controller import LtvLqrLoadControl
from aiml_virtual.util import mujoco_helper, carHeading2quaternion
from aiml_virtual.object.drone import DRONE_TYPES
from aiml_virtual.object.payload import PAYLOAD_TYPES

import numpy as np
import matplotlib.pyplot as plt

from aiml_virtual.object import parseMovingObjects


RED = "0.85 0.2 0.2 1.0"
BLUE = "0.2 0.2 0.85 1.0"
BLACK = "0.1 0.1 0.1 1.0"


abs_path = os.path.dirname(os.path.abspath(__file__))
xml_path = os.path.join(abs_path, "..", "xml_models")
xml_base_filename = "scene_base.xml"
save_filename = "built_scene.xml"


# create xml with a car
scene = SceneXmlGenerator(xml_base_filename)
car0_name = scene.add_car(pos="0 0 0.052", quat=carHeading2quaternion(0.64424), color=RED, is_virtual=True, has_rod=False, has_trailer=True)
payload0_name = scene.add_payload("-.4 -.3 .18", "0.05 0.05 0.05", "1", carHeading2quaternion(0.64424), BLACK, PAYLOAD_TYPES.Teardrop)
bb0_name = scene.add_drone("0 0 1", "1 0 0 0", RED, DRONE_TYPES.BUMBLEBEE_HOOKED, 2)
 

# saving the scene as xml so that the simulator can load it
scene.save_xml(os.path.join(xml_path, save_filename))

# create list of parsers 
virt_parsers = [parseMovingObjects]



control_step, graphics_step = 0.01, 0.02
xml_filename = os.path.join(xml_path, save_filename)

# recording interval for automatic video capture
#rec_interval=[1,25]
rec_interval = None # no video capture

simulator = ActiveSimulator(xml_filename, rec_interval, control_step, graphics_step)

simulator.onBoard_elev_offset = 20

# grabbing the drone and the car
car0 = simulator.get_MovingObject_by_name_in_xml(car0_name)

car0_trajectory=CarTrajectory()

# define path points and build the path
path_points = np.array(
    [
        [0, 0],
        [1, 1],
        [2, 2],
        [3, 2],
        [4, 1],
        [4.5, 0],
        [4, -1],
        [3, -2],
        [2, -2],
        [1, -1],
        [0, 0],
        [-1, 1],
        [-2, 2],
        [-3, 2],
        [-4, 1],
        [-4.5, 0],
        [-4, -2.1],
        [-3, -2.3],
        [-2, -2],
        [-1, -1],
        [0, 0],
    ]
)

path_points /= 1.5

car0_trajectory.build_from_points_const_speed(path_points=path_points, path_smoothing=0.01, path_degree=4, const_speed=1., start_delay=1.0)
#car0_trajectory.plot_trajectory()

car0_controller = CarLPVController(car0.mass, car0.inertia)

car0_controllers = [car0_controller]


# setting trajectory and controller for car0
car0.set_trajectory(car0_trajectory)
car0.set_controllers(car0_controllers)

bb0 = simulator.get_MovingObject_by_name_in_xml(bb0_name)

#bb0_controller = 
#bb0_trajectory = 

#bb0.set_controllers([bb0_controller])
#bb0.set_trajectory(bb0_trajectory)


while not simulator.glfw_window_should_close():
    simulator.update()
    
simulator.close()