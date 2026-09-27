"""Reusable illustrative USB cable models and four exact-CAD storage scenes.

Run: blender --background --python docs/render/render_cables.py
Dimensions are mm. Cable housings are illustrative, not a connector specification.
"""
import bpy
import math
import json
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs' / 'images'
MODELS = ROOT / 'docs' / 'models'
MODELS.mkdir(exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def mat(name, color, rough=.4, metal=0):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=rough
    p.inputs['Metallic'].default_value=metal
    return m

orange=mat('USB Buddy / tangerine PLA',(.91,.21,.028))
sage=mat('USB Buddy / sage PLA',(.24,.37,.26))
graphite=mat('USB Buddy / graphite PLA',(.045,.058,.069))
black=mat('Cable / charcoal',(.018,.026,.032),.48)
white=mat('Cable / warm white',(.78,.76,.68),.48)
blue=mat('Cable / slate blue',(.055,.19,.31),.46)
silver=mat('Connector / nickel',(.58,.62,.66),.23,.88)
dark=mat('Connector / black insert',(.009,.012,.014),.5)
gold=mat('Connector / contact',(.64,.39,.065),.25,.75)
groundmat=mat('Backdrop / warm stone',(.60,.59,.55),.8)

def box(name,dims,loc,material,bevel=0,parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object
    o.name=name
    o.dimensions=dims
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(material)
    if bevel:
        mod=o.modifiers.new('Soft molded edges','BEVEL')
        mod.width=bevel
        mod.segments=5
        normal=o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    if parent:
        o.parent=parent
    return o

def plug(kind,tip,axis,color,name):
    root=bpy.data.objects.new(name,None)
    bpy.context.collection.objects.link(root)
    root.location=tip
    root.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler()
    if kind=='A':
        # Four walls form a hollow USB-A shell, with an insulating tongue.
        for x in [-2.1,2.1]:
            box(name+' shell side',(.3,11.8,11.5),(x,0,5.75),silver,.10,root)
        for y in [-5.75,5.75]:
            box(name+' shell edge',(4.5,.3,11.5),(0,y,5.75),silver,.10,root)
        box(name+' tongue',(1.65,9.9,9),(.85,0,6),dark,.12,root)
        for y in [-3.4,-1.15,1.15,3.4]:
            box(name+' contact',(.06,.8,6),(-.02,y,5),gold,.02,root)
        for x in [-2.26,2.26]:
            for y in [-2.6,2.6]:
                box(name+' retention detail',(.025,2.1,2),(x,y,3.8),dark,.1,root)
        box(name+' overmold',(7,14,13),(0,0,18),color,1.25,root)
        box(name+' strain relief',(4.7,5.6,5),(0,0,27),color,1.0,root)
        end=29.5
    else:
        box(name+' oval metal shell',(2.5,8.1,6.5),(0,0,3.25),silver,1.10,root)
        box(name+' tip insert',(1.45,6.6,.08),(0,0,-.01),dark,.60,root)
        box(name+' overmold',(5.5,10.5,10),(0,0,11.5),color,1.8,root)
        box(name+' strain relief',(3.8,4.5,5),(0,0,19),color,.9,root)
        end=21.5
    return Vector(tip)+Vector(axis)*end

def cable(name,points,color):
    data=bpy.data.curves.new(name,'CURVE')
    data.dimensions='3D'
    data.resolution_u=28
    data.bevel_depth=1.35
    data.bevel_resolution=5
    data.use_fill_caps=True
    spline=data.splines.new('BEZIER')
    spline.bezier_points.add(len(points)-1)
    for p,co in zip(spline.bezier_points,points):
        p.co=co
        p.handle_left_type='AUTO'
        p.handle_right_type='AUTO'
    obj=bpy.data.objects.new(name,data)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(color)
    return obj

def aim(o,target):
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()

def light(name,loc,power,size,color):
    d=bpy.data.lights.new(name,'AREA')
    d.energy=power
    d.shape='DISK'
    d.size=size
    d.color=color
    o=bpy.data.objects.new(name,d)
    bpy.context.collection.objects.link(o)
    o.location=loc
    aim(o,(0,20,0))

def setup(name,product_mat=orange):
    scene=bpy.data.scenes.new(name)
    bpy.context.window.scene=scene
    bpy.ops.wm.stl_import(filepath=str(ROOT/'usb_buddy.stl'))
    obj=bpy.context.object
    obj.name='USB BUDDY / exact v19 printable mesh'
    obj.location=(-56.5,-8,0)
    obj.data.materials.append(product_mat)
    scene.render.engine='CYCLES'
    scene.cycles.samples=48
    scene.cycles.use_denoising=True
    scene.render.resolution_x=1800
    scene.render.resolution_y=1300
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='JPEG'
    scene.render.image_settings.quality=90
    scene.world=bpy.data.worlds.new(name+' world')
    scene.world.color=(.28,.28,.28)
    scene.view_settings.view_transform='AgX'
    bpy.ops.mesh.primitive_plane_add(size=2000,location=(0,0,-53))
    bpy.context.object.name='Studio backdrop'
    bpy.context.object.data.materials.append(groundmat)
    light('Key softbox',(-80,-100,190),650000,140,(1,.93,.84))
    light('Fill softbox',(100,30,130),400000,100,(.78,.88,1))
    light('Edge softbox',(-70,140,80),450000,80,(1,.79,.58))
    bpy.ops.object.camera_add(location=(145,-200,145))
    cam=bpy.context.object
    cam.data.type='ORTHO'
    cam.data.ortho_scale=208
    aim(cam,(0,38,15))
    scene.camera=cam
    return scene,obj

counts={}
for mode,full in [('loop',False),('loop',True),('pair',False),('pair',True)]:
    name=('10' if full else '01')+'-'+('cable-loop' if mode=='loop' else 'cable-pair')
    scene,obj=setup(name)
    slots=range(10) if full else [4]
    for i in slots:
        x=-56.5+i*11.5+4.75
        prefix=f'Pod {i+1:02d}'
        color=([black,blue][i%2] if mode=='pair' else [black,white,blue][i%3]) if full else black
        top=plug('A',(x,0,9),(0,0,1),color,prefix+' / A parked')
        if mode=='loop':
            bottom=plug('C',(x,0,6.5),(0,0,-1),color,prefix+' / C parked')
            cable(prefix+' / ONE continuous A-to-C cable',[
                top,(x,0,55),(x,18,65),(x,72,65),
                (x,90,48),(x,90,-17),(x,72,-35),(x,18,-35),
                (x,0,-28),bottom],color)
        else:
            # Two complete independent cables, with their other ends visible.
            far_top=plug('C',(x,130,39),(0,-1,0),color,prefix+' / upper cable free C')
            cable(prefix+' / first cable A-to-C',[
                top,(x,0,56),(x,20,67),(x,70,67),
                (x,92,53),(x,99,40),far_top],color)
            bottom=plug('C',(x,0,6.5),(0,0,-1),white,prefix+' / C parked')
            far_bottom=plug('C',(x,130,-27),(0,-1,0),white,prefix+' / lower cable free C')
            cable(prefix+' / second cable C-to-C',[
                bottom,(x,0,-30),(x,20,-42),(x,73,-42),
                (x,94,-30),far_bottom],white)
    if mode=='pair':
        scene.camera.location=(155,-190,140)
        aim(scene.camera,(0,48,13))
        scene.camera.data.ortho_scale=230
    scene.render.filepath=str(OUT/(name+'.jpg'))
    counts[name]={'occupied_pods':len(slots),'parked_ends':len(slots)*2,
                  'distinct_cables':len(slots)*(1 if mode=='loop' else 2)}
    bpy.ops.render.render(write_still=True)

# A true mesh section exposes the shared pod interior and the two parked tips.
scene,obj=setup('pod-cutaway')
cut=box('Section volume',(9.5,8,60),(-5.75,4,10),dark)
mod=obj.modifiers.new('One pod, front half removed','BOOLEAN')
mod.operation='INTERSECT'
mod.solver='EXACT'
mod.object=cut
bpy.context.view_layer.objects.active=obj
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(cut,do_unlink=True)
top=plug('A',(-5.75,0,9),(0,0,1),black,'Section / A parked')
bottom=plug('C',(-5.75,0,6.5),(0,0,-1),white,'Section / C parked')
cable('Section / A cable',[top,(-5.75,0,47)],black)
cable('Section / C cable',[bottom,(-5.75,0,-24)],white)
scene.camera.location=(28,-130,35)
aim(scene.camera,(-5.75,0,11))
scene.camera.data.ortho_scale=88
scene.render.resolution_x=1200
scene.render.resolution_y=1400
scene.render.filepath=str(OUT/'pod-cutaway.jpg')
bpy.ops.render.render(write_still=True)

# Product-only color and end-label views use the identical revised mesh.
for name,material,campos in [
    ('product-orange',orange,(95,-155,95)),
    ('product-sage',sage,(-90,-155,85)),
    ('product-graphite',graphite,(90,-155,75))]:
    scene,obj=setup(name,material)
    scene.render.resolution_y=1000
    scene.camera.location=campos
    aim(scene.camera,(0,0,7))
    scene.camera.data.ortho_scale=145
    for o in scene.objects:
        if o.name.startswith('Studio backdrop'):
            o.location.z=-.05
    if name=='product-graphite':
        scene.world.color=(.06,.07,.10)
        for o in scene.objects:
            if o.type=='LIGHT' and o.name.startswith('Edge'):
                o.data.color=(.35,.55,1)
                o.data.energy=700000
    scene.render.filepath=str(OUT/(name+'.jpg'))
    bpy.ops.render.render(write_still=True)

bpy.context.window.scene=bpy.data.scenes['01-cable-loop']
bpy.ops.wm.save_as_mainfile(filepath=str(MODELS/'usb-buddy-cable-scenes.blend'))
(MODELS/'scene-inventory.json').write_text(json.dumps(counts,indent=2)+'\n')
print('SCENE INVENTORY:',json.dumps(counts))
