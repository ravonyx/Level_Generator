import bpy
from math import *
from random import *
from mathutils import *
import bmesh
import random

def extrude_face(mesh, index, x, y, z):
    bpy.ops.mesh.select_all(action="DESELECT")
    mesh.faces[index].select = True
    axis_x = False
    axis_y = False
    axis_z = False
    if x != 0:
        axis_x = True
    if y != 0:
        axis_y = True
    if z != 0:
        axis_z = True
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(x, y, z), "constraint_axis":(axis_x, axis_y, axis_z)})
	
    bpy.ops.mesh.select_all(action="DESELECT")  

def extrude_face_simple(mesh, x, y, z):
    axis_x = False
    axis_y = False
    axis_z = False
    if x != 0:
        axis_x = True
    if y != 0:
        axis_y = True
    if z != 0:
        axis_z = True
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(x, y, z), "constraint_axis":(axis_x, axis_y, axis_z)})
	
    bpy.ops.mesh.select_all(action="DESELECT")  
	
def extrude_face_multiple(mesh, x, y, z, from_face, to_face):	
	bpy.ops.mesh.select_all(action="DESELECT")  
	mesh.faces[from_face].select = True
	mesh.faces[to_face].select = True
	bpy.ops.mesh.shortest_path_select()
	
	axis_x = False
	axis_y = False
	axis_z = False
	if x != 0:
		axis_x = True
	if y != 0:
		axis_y = True
	if z != 0:
		axis_z = True
	bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(x, y, z), "constraint_axis":(axis_x, axis_y, axis_z)})
	bpy.ops.mesh.select_all(action="DESELECT")  
	
def translate_face(mesh, index, x, y, z):
    bpy.ops.mesh.select_all(action="DESELECT")
    mesh.faces[index].select = True
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.mesh.select_all(action="DESELECT")  

def translate_edge(mesh, index, x, y, z):
    bpy.ops.mesh.select_all(action="DESELECT")
    mesh.verts[index].select = True
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.mesh.select_all(action="DESELECT")  

def scale_face_contraint(mesh, index, x,y,z, value):
    bpy.ops.mesh.select_all(action="DESELECT")  
    mesh.faces[index].select = True
    bpy.ops.transform.resize(value=(value, value, value), constraint_axis=(x,y,z), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.mesh.select_all(action="DESELECT")  

def scale_face(mesh, index, x,y,z):
    bpy.ops.mesh.select_all(action="DESELECT")  
    mesh.faces[index].select = True
    bpy.ops.transform.resize(value=(x, y, z), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.mesh.select_all(action="DESELECT")  
	
def createMaterial(name):
	img = bpy.data.images.load('//'+name)
	tex = bpy.data.textures.new('TexName', type = 'IMAGE')
	tex.image = img
	mat = bpy.data.materials.new('MatName')
	
	ctex = mat.texture_slots.add()
	ctex.texture = tex
	ctex.texture_coords = 'ORCO'
	ctex.mapping = 'CUBE'
	return mat
	
def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)

def duplicate_object(scene, name, copyobj):
	# Create new mesh
	mesh = bpy.data.meshes.new(name)

	# Create new object associated with the mesh
	ob_new = bpy.data.objects.new(name, mesh)

	# Copy data block from the old object into the new object
	ob_new.data = copyobj.data.copy()
	ob_new.scale = copyobj.scale
	ob_new.location = copyobj.location

	# Link new object to the given scene and select it
	scene.objects.link(ob_new)
	ob_new.select = True
	
	return ob_new
	
def map(length, width, height):
	print("-----Gen Level-----")
	
	base_length = length
	base_width = width
	pos_z = 0
	length = uniform(30,50)
	width = uniform(30,50)
	
	#FIRST FLOOR
	#ground under
	create_ground(pos_z, length, width)
	#wall
	create_walls_border(pos_z, length, width, 0)
	create_walls_border(pos_z, length, width, 1)
	
	border_length = length - 10
	border_width = width - 10
	
	
	#walls inside
	if length < width:
		pos_x = uniform(border_length/2 , border_length)
		pos_y = uniform(10 ,border_width/3)
		
		length_wall = uniform(5,border_length)
		create_wall_inside(2, pos_x, pos_y, pos_z, height, length_wall, border_length, 0)
		
		bpy.ops.object.mode_set(mode='OBJECT')

		pos_x2 = uniform(2 , border_length/2)
		pos_y2 = uniform(border_width/3 + 10 , border_width * 2/3)
			
		length_wall = uniform(5,border_length)
		create_wall_inside(2, pos_x2, pos_y2, pos_z, height, length_wall, border_length, 0)
		
		bpy.ops.object.mode_set(mode='OBJECT')
		
		pos_x3 = uniform(border_length/2 , border_length)
		pos_y3 = uniform(border_width * 2/3 + 10 , border_width)
			
		length_wall = uniform(5,border_length)
		create_wall_inside(2, pos_x3, pos_y3, pos_z, height, length_wall, border_length, 0)

	else:
		pos_x = uniform(10 , border_length/3)
		pos_y = uniform(border_width/2 , border_width)
		
		length_wall = uniform(5,border_length)
		create_wall_inside(1, pos_x, pos_y, pos_z, height, length_wall, border_width, 1)
		
		bpy.ops.object.mode_set(mode='OBJECT')

		pos_x2 = uniform(border_length/3 + 10 , border_length * 2/3)
		pos_y2 = uniform(2 , border_width/2)
			
		length_wall = uniform(5,border_length)
		create_wall_inside(1, pos_x2, pos_y2, pos_z, height, length_wall, border_width, 1)
		
		bpy.ops.object.mode_set(mode='OBJECT')
		
		pos_x3 =	uniform(border_length * 2/3 + 10 , border_length)
		pos_y3 =	uniform(border_width/2 , border_width)
			
		length_wall = uniform(5,border_length)
		create_wall_inside(1, pos_x3, pos_y3, pos_z, height, length_wall, border_width, 1)
	
	bpy.ops.object.mode_set(mode='OBJECT')
	
	pos_z = height + 4
	#ground above
	create_ground(pos_z, length, width)
	
	bpy.ops.object.mode_set(mode='OBJECT')
	
	#SECOND FLOOR
	"""pos_z = pos_z + 1
	length = uniform(30,50)
	width = uniform(30,50)
	#ground under
	create_ground(pos_z, length, width)
	#wall
	create_walls_border(pos_z, length, width, 0)
	create_walls_border(pos_z, length, width, 1)
	pos_z = height*2 + 4*2"""

def create_wall_inside(index, pos_x, pos_y, pos_z, height, length_wall, border, isWidth):
	mat_wall_inside = createMaterial('wall_inside.jpg')
	bpy.ops.mesh.primitive_cube_add(location=(2,2,pos_z+2))
	
	
	wall_inside = bpy.context.active_object
	wall_inside_data = wall_inside.data
	
	bpy.ops.object.mode_set(mode='EDIT')
	mesh = bmesh.from_edit_mesh(wall_inside_data)
	
	print(pos_x)
	print(length_wall)
	print(border)
	
	if isWidth == 0:
		if length_wall + pos_x > border:
			print("out of border")
			pos_x = border - length_wall
	else:
		if length_wall + pos_y > border:
			print("out of border")
			pos_y = border - length_wall
			
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.transform.translate(value=(pos_x, pos_y, 0), constraint_axis=(True, True, False))
	
	bpy.ops.object.mode_set(mode='EDIT')
	mesh = bmesh.from_edit_mesh(wall_inside_data)
	
	if isWidth == 0:
		extrude_face(mesh, index, length_wall, 0, 0)
	else:
		extrude_face(mesh, index, 0, length_wall, 0)
		
	mesh.faces[5].select = True
	mesh.faces[8].select = True
	extrude_face_simple(mesh, 0, 0, height)
	
	setMaterial(wall_inside, mat_wall_inside)
	
def create_ground(pos_z, length, width):
	mat_ground = createMaterial('ground.png')
	
	bpy.ops.mesh.primitive_cube_add(location=(0,0,pos_z))
	ground = bpy.context.active_object
	ground_data = ground.data
	
	bpy.ops.object.mode_set(mode='EDIT')
	mesh = bmesh.from_edit_mesh(ground_data)
	
	extrude_face(mesh, 2, length, 0, 0)
	mesh.faces[1].select = True
	mesh.faces[9].select = True
	extrude_face_simple(mesh, 0, width, 0)
	
	setMaterial(ground, mat_ground)
	
def create_walls_border(pos_z, length, width, isWidth):
	mat_wall = createMaterial('wall.jpg')

	#create a simple cube and move it to the right place
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.mesh.primitive_cube_add(location=(0,0,pos_z))
	#bpy.ops.transform.resize(value=(0.3, 0.3, 0.3), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
	bpy.ops.transform.translate(value=(0, 0, 2), constraint_axis=(False, False, True))
	
	#get data from the cube and set material
	wall = bpy.context.active_object
	wall_data = wall.data
	
	#edit the mesh and transform it in a wall
	bpy.ops.object.mode_set(mode='EDIT')
	mesh = bmesh.from_edit_mesh(wall_data)

	if(isWidth == 0):
		extrude_face(mesh, 2, length, 0, 0)
	else:
		extrude_face(mesh, 1, 0, width, 0)
		
	mesh.faces[5].select = True
	mesh.faces[8].select = True
	extrude_face_simple(mesh, 0, 0, height)
	bpy.ops.object.mode_set(mode='OBJECT')  
	#duplicate this wall and move it
	
	mat_wall.alpha = 0.5
	mat_wall.use_transparency = True
	setMaterial(wall, mat_wall)
	
	if(isWidth == 0):
		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, width, 0), "constraint_axis":(False, True, False)});
	else:
		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(length, 0, 0), "constraint_axis":(True, False, False)});
	
def print_index():
    mesh = bpy.context.object
    mesh_data = mesh.data
    mesh = bmesh.from_edit_mesh(mesh_data)
    i = 0
    for face in mesh.faces:
        if face.select == True:
            print(i)
        i = i + 1
    i = 0
   
    """for vert in mesh.verts:
        if vert.select == True:
            print(i)
        i = i + 1   """
		
length = 30
width = 30
height = 15
#print_index()
map(length, width, height)

