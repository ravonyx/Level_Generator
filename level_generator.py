import bpy
from math import *
from random import *
from mathutils import *
import bmesh

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
 
def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)
    
def map(length, width):
    bpy.ops.mesh.primitive_plane_add(location=(0,0,0))
    mesh_object = bpy.context.object
    mesh_data = mesh_object.data

    bpy.ops.object.mode_set(mode='EDIT')
    mat_ground = makeMaterial('Red', (1,0,0), (1,1,1), 1)
    mesh = bmesh.from_edit_mesh(mesh_data)
    
    scale_face(mesh, 0, length, width, 0)
    setMaterial(mesh_object, mat_ground)
    
    
    mesh.faces[0].select = True
    bpy.ops.mesh.subdivide()
    bpy.ops.mesh.subdivide()
    bpy.ops.mesh.subdivide()
    bpy.ops.mesh.subdivide()
    
    """print(bpy.data.objects)
    bpy.data.object.selected = True
    bpy.context.scene.objects.active = bpy.data.objects['Plane']
    setState0()
   
    index_topright = 0
    index_bottomright = 255
    index_bottomleft = 215
    index_topleft = 175
    mesh.faces[index_topright].select = True
    mesh.faces[index_topleft].select = True
    bpy.ops.mesh.shortest_path_pick()
    mesh.faces[index_bottomleft].select = True
    bpy.ops.mesh.shortest_path_pick()
    mesh.faces[index_bottomright].select = True
    bpy.ops.mesh.shortest_path_pick()"""

def setState0():  
    for ob in bpy.data.objects.values():
        ob.selected=False
    bpy.context.scene.objects.active = None
  
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
    

    #for vert in mesh.verts:
     #   if vert.select == True:
      #      print(i)
       # i = i + 1   
    
map(7, 7)
#print_index()
