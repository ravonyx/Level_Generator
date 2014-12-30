import bpy
from math import *
from random import *
from mathutils import *
import bmesh

a = uniform(0,1)
b = uniform(1, 2)
c = uniform(2,3);
d = uniform(4,5)

length_nose = uniform(2,4)
length_body = uniform(2,7)
length_wing = uniform(3,5)

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
    
def vaisseau(a, b, c, d, length_nose, length_body, length_wing):
    print(a)
    print(b)
    bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
    
    mesh = bpy.context.object
    mesh_data = mesh.data
    
    bm = bmesh.new()
    bm.from_mesh(mesh_data)
    bpy.ops.object.mode_set(mode='EDIT')  
    
    for v in bm.verts:
        v.co.x += 1
    update_bmesh(bm, mesh_data)
    bpy.ops.object.mode_set(mode='OBJECT')  
    bpy.ops.object.modifier_add(type='MIRROR')
    bpy.context.object.modifiers["Mirror"].use_clip=1
    
    bpy.ops.object.mode_set(mode='EDIT')
    mesh = bmesh.from_edit_mesh(mesh_data)
    
    scale_face(mesh, 3, a, c, a)
    extrude_face(mesh, 3, 0, -length_nose, 0)
    extrude_face(mesh, 1, 0, length_body, 0)  
    extrude_face(mesh, 11, length_wing, 0, 0)
    translate_face(mesh, 14, 0, c, 0)
    scale_face_contraint(mesh, 14, False, False, True, a)
    extrude_face(mesh, 10, 0, 2, 0)
    scale_face_contraint(mesh, 6, True, False, False, -a)
    scale_face_contraint(mesh, 6, False, False, True, a)
    scale_face(mesh, 18, b, b, b)
    
    translate_edge(mesh, 17, -b, b, 0)
    
    bpy.ops.object.mode_set(mode='OBJECT')  
    bpy.ops.object.shade_smooth()

    #update_bmesh(bm, mesh_data)    
    #bm.free()
   
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
    for vert in mesh.verts:
        if vert.select == True:
            print(i)
        i = i + 1   
 
vaisseau(a, b, c, d, length_nose, length_body, length_wing)
#print_index()

