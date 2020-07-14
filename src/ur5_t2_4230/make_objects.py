#!/usr/bin/env python
import random
import tf
import rospy
import typing
from std_msgs.msg import String
from gazebo_msgs.srv import SpawnModel, DeleteModel
from geometry_msgs.msg import Pose, Point, Quaternion

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
		#'''Args: str, Point'''

		# first try to delete it (it might already exist)
		self.delete_model(node_name)
	
		MODEL_PATH = rospy.get_param('MODEL_PATH') + 'sdf/'
		print(MODEL_PATH)
		with open(MODEL_PATH + object_name + '.sdf') as file:
			xml = file.read()
			# item_pose = Pose(point, self.orientation)
			self.spawn_model(node_name, xml, '', pose, 'world')

def main():
	#rospy.init_node("spawn_products_in_bins")
	rospy.wait_for_service("gazebo/spawn_urdf_model")
	rospy.wait_for_service("gazebo/spawn_sdf_model")
	rospy.wait_for_service("gazebo/delete_model")

	#spawn the table in a predefined position
	pose = Pose(Point(1.5, 1, 0.25), Quaternion(0, 1, 0, -1))
	object_table = SDF_Object('object_table', 'table', pose)

	#spawn ten objects in a random position within set bounds
	object_list = ['red_box', 'green_box', 'blue_box', 'red_cylinder', 'green_cylinder', 'blue_cylinder']
	object_counter = 10
	x_coords = [0]
	y_coords = [0]

	while object_counter != 0:
		#makes a random choice from the list of available objects to spawn
		selected_object = random.choice(object_list)

		#x coordinate
		x = random.uniform(0.4,1.6)
		#y coordinate
		y = random.uniform(0.4,1.6)
		
		#flag to work out when to terminate loop
		found_coord = False
		while found_coord == False:
			#check if the coordinate has been done before
			for (c) in zip(x_coords,y_coords):
				#check current x coordinate against randomised
				if ((x-0.025)< c[0] < (x+0.025)) & ((y-0.025) < c[1] < (y+0.025)):
					print("matching coords")
					x = random.uniform(0.4,1.6)
					y = random.uniform(0.4,1.6)
				else:
					#print("unique coords")
					found_coord = True	

		x_coords.append(x)
		y_coords.append(y)

		#spawn object at random location
		URDF_Object(str(object_counter), selected_object, Point(x, y, 1.5))

		object_counter = object_counter - 1




if __name__ == '__main__':
	try:
	#print(rospy.get_param('MODEL_PATH'))
		main()
		
	except rospy.ROSInterruptException:
		pass
