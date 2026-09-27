"""Render the unmodified printable STL with Blender 5.x.

blender --background --python docs/render/render_product.py
"""
import bpy
import math
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.wm.stl_import(filepath=str(ROOT / 'usb_buddy.stl'))
product = bpy.context.object
print('SOURCE MESH DIMENSIONS (mm):', tuple(product.dimensions))
product.location.x = -56.5
product.location.y = -8

def material(name, color, roughness=0.38):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bs = m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (*color, 1)
    bs.inputs['Roughness'].default_value = roughness
    return m

orange = material('Warm orange PLA', (0.8, 0.19, 0.035))
product.data.materials.clear()
product.data.materials.append(orange)
bpy.ops.mesh.primitive_plane_add(size=2000, location=(0,0,-0.05))
floor = bpy.context.object
floor.data.materials.append(material('Warm white', (0.78,0.76,0.71), 0.7))

def aim(obj, target):
    obj.rotation_euler = (Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()

def light(name, loc, power, size, color):
    data=bpy.data.lights.new(name, 'AREA')
    data.energy=power
    data.shape='DISK'
    data.size=size
    data.color=color
    obj=bpy.data.objects.new(name,data)
    bpy.context.collection.objects.link(obj)
    obj.location=loc
    aim(obj,(0,0,0))
    return obj

key=light('Large softbox',(-40,-75,130),500000,100,(1,0.9,0.8))
fill=light('Fill',(70,35,85),350000,75,(0.8,0.9,1))
bpy.ops.object.camera_add(location=(94,-160,125))
camera=bpy.context.object
camera.data.type='ORTHO'
camera.data.ortho_scale=154
aim(camera,(0,0,7))
scene=bpy.context.scene
scene.camera=camera
scene.render.engine='CYCLES'
scene.cycles.samples=40
scene.cycles.use_denoising=True
scene.render.resolution_x=1800
scene.render.resolution_y=1000
scene.render.resolution_percentage=100
scene.world.color=(0.25,0.25,0.25)
scene.view_settings.view_transform='AgX'
scene.render.image_settings.file_format='PNG'

def render(name):
    scene.render.filepath=str(ROOT/'docs'/'images'/name)
    bpy.ops.render.render(write_still=True)

render('cad-reference.png')
floor.hide_render=True
camera.location=(65,-120,-115)
aim(camera,(0,0,6))
key.location=(-40,-75,-130)
aim(key,(0,0,6))
fill.location=(70,35,-85)
aim(fill,(0,0,6))
render('cad-underside.png')
