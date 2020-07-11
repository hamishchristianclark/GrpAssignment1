#!/usr/bin/env python
import random
import tf
import rospy
import typing
from std_msgs.msg import String
from gazebo_msgs.srv import SpawnModel, DeleteModel
from geometry_msgs.msg import Pose, Point, Quaternion

def test():
    print("hi")

class URDF_Object:
    orientation = Quaternion(0, 0, 0, 0)
    item_pose = Pose(Point(x=0, y=0, z=0), orientation)
    spawn_model = rospy.ServiceProxy("gazebo/spawn_urdf_model", SpawnModel)
    delete_model = rospy.ServiceProxy("gazebo/delete_model", DeleteModel)

    def __init__(self, node_name, object_name, point):
        '''Args: str, Point'''

        # first try to delete it (it might already exist)
        self.delete_model(node_name)

        MODEL_PATH = rospy.get_param('MODEL_PATH') + 'urdf/'
	print(MODEL_PATH)

        with open(MODEL_PATH + object_name + '.urdf') as file:
            xml = file.read()
            item_pose = Pose(point, self.orientation)
            self.spawn_model(node_name, xml, '', item_pose, 'world')

class SDF_Object:
    orientation = Quaternion(0, 0, 0, 0)
    item_pose = Pose(Point(x=0, y=0, z=0), orientation)
    spawn_model = rospy.ServiceProxy("gazebo/spawn_sdf_model", SpawnModel)
    
    delete_model = rospy.ServiceProxy("gazebo/delete_model", DeleteModel)

    def __init__(self, node_name, object_name, pose):
        '''Args: str, Point'''

        # first try to delete it (it might already exist)
        self.delete_model(node_name)
        test()
	
        MODEL_PATH = rospy.get_param('MODEL_PATH') + 'sdf/'
	print(MODEL_PATH)
        with open(MODEL_PATH + object_name + '.sdf') as file:
            xml = file.read()
            # item_pose = Pose(point, self.orientation)
            self.spawn_model(node_name, xml, '', pose, 'world')

def main():
    rospy.init_node("spawn_products_in_bins")
    rospy.wait_for_service("gazebo/spawn_urdf_model")
    rospy.wait_for_service("gazebo/spawn_sdf_model")
    rospy.wait_for_service("gazebo/delete_model")

    #spawn the table in a predefined position
    pose = Pose(Point(2, 2, 0), Quaternion(0, 1, 0, -1))
    output_container = SDF_Object('output_container', 'container', pose)

    #spawn ten objects in a random position within set bounds
    object_list = ['red_box', 'green_box', 'blue_box', 'red_cylinder', 'green_cylinder', 'blue_cylinder']
    object_counter = 10
#delete_model = rospy.ServiceProxy("gazebo/delete_model", DeleteModel)
    while object_counter != 0:
    	selected_object = random.choice(object_list)
    	#delete_model(str(object_counter))
    	#x coordinate
    	x = random.uniform(0.5,2.5)

    	#y coordinate
    	y = random.uniform(1,3)
    	
    	URDF_Object(str(object_counter), selected_object, Point(x, y, 0))


    	object_counter = object_counter - 1


    #URDF_Object('red_box', 'red_box', Point(0, 0, 0.2))
    # green_box = URDF_Object('green_box', 'green_box', Point(0, -0.2, 0.2))
    # blue_box = URDF_Object('blue_box', 'blue_box', Point(0, 0.2, 0.2))
    # red_cylinder = URDF_Object('red_cylinder', 'red_cylinder', Point(0, 0, 0.6))
    # green_cylinder = URDF_Object('green_cylinder', 'green_cylinder', Point(0, -0.2, 0.6))
    # blue_cylinder = URDF_Object('blue_cylinder', 'blue_cylinder', Point(0, 0.2, 0.6))


if __name__ == '__main__':
    try:
	#print(rospy.get_param('MODEL_PATH'))
        main()
    except rospy.ROSInterruptException:
	pass
