import bpy
from math import *
from random import *
from mathutils import *
import bmesh
import random

def update_bmesh(bm, mesh_data):
    bpy.ops.object.mode_set(mode='OBJECT')  
    bm.to_mesh(mesh_data)
    
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

def makeMaterial(name, diffuse, specular, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT' 
    mat.diffuse_intensity = 1.0 
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 1
    return mat
	
def createMaterial(mesh, ob, name):
	img = bpy.data.images.load('D://ESGI/Dev_3D/Level_Generator/'+name)
	tex = bpy.data.textures.new('TexName', type = 'IMAGE')
	tex.image = img
	mat = bpy.data.materials.new('MatName')
	
	
	#print(ob.data.uv_textures.active)
	#ob.data.uv_textures.active.data[0].image = img
	ctex = mat.texture_slots.add()
	ctex.texture = tex
	ctex.texture_coords = 'ORCO'
	ctex.mapping = 'CUBE'
	return mat
	
def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)
   
def update_bmesh(bm, mesh_data):
	
	bm.to_mesh(mesh_data)

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
	bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
	mesh_object = bpy.context.object
	mesh_data = mesh_object.data
	
	bm = bmesh.new()
	bm.from_mesh(mesh_data)
	
	bpy.ops.object.mode_set(mode='EDIT')
	#mat_ground = makeMaterial('Red', (1,0,0), (1,1,1), 1)
	
	mesh = bmesh.from_edit_mesh(mesh_data)
	mat_ground = createMaterial(mesh, mesh_object,'color.jpg')
	
	
	extrude_face(mesh, 2, length, 0, 0)
	mesh.faces[1].select = True
	mesh.faces[9].select = True
	extrude_face_simple(mesh, 0, width, 0)
	
	setMaterial(mesh_object, mat_ground);
	"""mesh.faces[0].select = True
	bpy.ops.mesh.subdivide()
	bpy.ops.mesh.subdivide()
	bpy.ops.mesh.subdivide()
	bpy.ops.mesh.subdivide()"""
	
	# Walls extrude #
	"""index_topright = 0
	index_bottomright = 255
	index_bottomleft = 215
	index_topleft = 175

	extrude_face_multiple(mesh, 0,0, height, index_topright, index_topleft)
	
	index_topleft = index_topleft + 1
	extrude_face_multiple(mesh, 0,0, height, index_topleft, index_bottomleft)

	index_bottomleft = index_bottomleft + 1
	extrude_face_multiple(mesh, 0,0, height, index_bottomleft, index_bottomright)

	extrude_face_multiple(mesh, 0,0, height, 63, 66)"""
	
	mat_wall = createMaterial(mesh, mesh_object,'wall.jpg')
	#WALL LENGTH
	#create a simple cube and move it to the right place
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
	#bpy.ops.transform.resize(value=(0.3, 0.3, 0.3), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
	bpy.ops.transform.translate(value=(0, 0, 2), constraint_axis=(False, False, True))
	
	#get data from the cube and set material
	wall = bpy.context.active_object
	wall_data = wall.data
	
	#edit the mesh and transform it in a wall
	bpy.ops.object.mode_set(mode='EDIT')
	mesh = bmesh.from_edit_mesh(wall_data)

	
	extrude_face(mesh, 2, length, 0, 0)
	mesh.faces[5].select = True
	mesh.faces[8].select = True
	extrude_face_simple(mesh, 0, 0, height)
	bpy.ops.object.mode_set(mode='OBJECT')  
	#duplicate this wall and move it
	setMaterial(wall, mat_wall)
	bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, width, 0), "constraint_axis":(False, True, False)});
	
	#WALL WIDTH 
	#create a simple cube and move it to the right place
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
	#bpy.ops.transform.resize(value=(0.3, 0.3, 0.3), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
	bpy.ops.transform.translate(value=(0, 0, 2), constraint_axis=(False, False, True))
	
	#get data from the cube
	wall = bpy.context.active_object
	wall_data = wall.data
	#setMaterial(wall, mat)
	#edit the mesh and transform it in a wall
	bpy.ops.object.mode_set(mode='EDIT')
	mesh = bmesh.from_edit_mesh(wall_data)
	extrude_face(mesh, 1, 0, width, 0)
	mesh.faces[5].select = True
	mesh.faces[8].select = True
	extrude_face_simple(mesh, 0, 0, height)
	bpy.ops.object.mode_set(mode='OBJECT')  
	
	setMaterial(wall, mat_wall)
	#duplicate this wall and move it
	bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(length, 0, 0), "constraint_axis":(True, False, False)});

	#get the scene
	#scene = bpy.context.scene
	
	#Walls inside
	"""extrude_face_multiple(mesh, 0,0, height, 45, 69)
	rand_faces = [5, 31, 34, 79, 166]
	extrude_face_multiple(mesh, 0,0, height, 8,random.choice(rand_faces))
	
	from_rand_faces = [97, 98, 209]
	to_rand_faces = [12, 24, 138]
	extrude_face_multiple(mesh, 0,0, height, random.choice(from_rand_faces),random.choice(to_rand_faces))"""
	
	"""from_rand_faces = [97, 98, 209]
	to_rand_faces = [12, 24, 138]
	extrude_face_multiple(mesh, 0,0, height, random.choice(from_rand_faces),random.choice(to_rand_faces))"""
	
	#Stairs extrude#
	"""height_inc = height / 4
	height_stair = height
	extrude_face(mesh, 149, 0, 0, height_stair)
	height_stair = height_stair - height_inc
	extrude_face(mesh, 150, 0, 0, height_stair)
	height_stair = height_stair - height_inc
	extrude_face(mesh, 77, 0, 0, height_stair)
	height_stair = height_stair - height_inc
	extrude_face(mesh, 78, 0, 0, height_stair)"""
	
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
height = 5
#print_index()
map(length, width, height)

