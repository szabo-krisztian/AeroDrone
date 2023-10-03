from classes.remote_trajectory import TrajectoryDistributor, RemoteDroneTrajectory
from classes.drone_classes.drone_geom_control import GeomControl
from classes.active_simulation import ActiveSimulator
from util.xml_generator import SceneXmlGenerator
from classes.drone import DRONE_TYPES
from classes.object_parser import parseMovingObjects
import os

RED = "0.85 0.2 0.2 1.0"
BLUE = "0.2 0.2 0.85 1.0"


abs_path = os.path.dirname(os.path.abspath(__file__))
xml_path = os.path.join(abs_path, "..", "xml_models")
xmlBaseFileName = "scene_base.xml"
save_filename = "built_scene.xml"


scene = SceneXmlGenerator(xmlBaseFileName)

drone0_name = scene.add_drone("0 0 1", "1 0 0 0", BLUE, DRONE_TYPES.CRAZYFLIE)
drone1_name = scene.add_drone("0 1 1", "1 0 0 0", BLUE, DRONE_TYPES.CRAZYFLIE)
drone2_name = scene.add_drone("1 0 1", "1 0 0 0", BLUE, DRONE_TYPES.CRAZYFLIE)

scene.save_xml(os.path.join(xml_path, save_filename))

virt_parsers = [parseMovingObjects]
mocap_parsers = None

control_step, graphics_step = 0.01, 0.02
xml_filename = os.path.join(xml_path, save_filename)


simulator = ActiveSimulator(xml_filename, None, control_step, graphics_step, virt_parsers, mocap_parsers,
                            connect_to_optitrack=False)

simulator.cam.distance = 3

drone0 = simulator.get_MovingObject_by_name_in_xml(drone0_name)
drone1 = simulator.get_MovingObject_by_name_in_xml(drone1_name)
drone2 = simulator.get_MovingObject_by_name_in_xml(drone2_name)

trajectory0 = RemoteDroneTrajectory(can_execute=False)
trajectory1 = RemoteDroneTrajectory(can_execute=False)
trajectory2 = RemoteDroneTrajectory(can_execute=False)

drone0.set_trajectory(trajectory0)
drone1.set_trajectory(trajectory1)
drone2.set_trajectory(trajectory2)

controller0 = GeomControl(drone0.mass, drone0.inertia, simulator.gravity)

drone0.set_controllers([controller0])

td = TrajectoryDistributor(simulator.all_virt_vehicles)
td.connect("127.0.0.1", 12345)
td.start_background_thread()

while not simulator.glfw_window_should_close():

    simulator.update()
    
simulator.close()