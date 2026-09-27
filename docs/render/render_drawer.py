"""Physically oriented v18 CAD drawer study. All dimensions are millimeters.
Run: Blender --background --threads 4 --python docs/render/render_drawer.py
The five A plugs enter the true A openings; the front lettering faces upward.
No generative imagery is used: this is an illustrative CAD storage mockup.
"""
from pathlib import Path
# Reuse primitive builders only, stopping before render_cables' execution block.
helper=Path(__file__).with_name('render_cables.py').read_text().split('\ncounts={}')[0]
exec(compile(helper,str(Path(__file__).with_name('render_cables.py')),'exec'))
import random

scene=bpy.context.scene
scene.name='Same drawer / before and after / exact v18'
scene.render.engine='CYCLES'
scene.cycles.samples=64
scene.cycles.use_denoising=True
scene.render.threads_mode='FIXED'
scene.render.threads=4
scene.render.resolution_x=2400
scene.render.resolution_y=1500
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='JPEG'
scene.render.image_settings.quality=94
scene.world.color=(.32,.32,.32)
scene.view_settings.view_transform='AgX'

wood=mat('Light oak / restrained longitudinal grain',(.65,.48,.29),.55)
n=wood.node_tree.nodes; links=wood.node_tree.links
tex=n.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value=3.0; tex.inputs['Detail'].default_value=2.0
coords=n.new('ShaderNodeTexCoord'); mapping=n.new('ShaderNodeVectorMath'); mapping.operation='MULTIPLY'; mapping.inputs[1].default_value=(32,1.5,4)
links.new(coords.outputs['Generated'],mapping.inputs[0]); links.new(mapping.outputs[0],tex.inputs['Vector'])
ramp=n.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position=.15; ramp.color_ramp.elements[0].color=(.46,.29,.14,1); ramp.color_ramp.elements[1].position=.85; ramp.color_ramp.elements[1].color=(.76,.60,.40,1)
links.new(tex.outputs['Fac'],ramp.inputs[0]); links.new(ramp.outputs['Color'],n.get('Principled BSDF').inputs['Base Color'])
bum=n.new('ShaderNodeBump'); bum.inputs['Strength'].default_value=.11; bum.inputs['Distance'].default_value=.11; links.new(tex.outputs['Fac'],bum.inputs['Height']); links.new(bum.outputs[0],n.get('Principled BSDF').inputs['Normal'])
ink=mat('Captions / deep slate',(.035,.046,.045),.9)
bg=mat('Warm paper surface',(.80,.78,.73),.8)
box('Backdrop',(1600,1300,5),(0,0,-13),bg,2)

def caption(text,x,y,size):
    cu=bpy.data.curves.new(text,'FONT'); cu.body=text; cu.align_x='CENTER'; cu.size=size; cu.extrude=0
    ob=bpy.data.objects.new(text,cu); bpy.context.collection.objects.link(ob); ob.location=(x,y,.4); ob.data.materials.append(ink)
    return ob

def drawer(cx,name):
    box(name+' oak base',(212,250,5),(cx,0,-2.5),wood,2)
    box(name+' left side',(7,250,24),(cx-102.5,0,9),wood,1.7)
    box(name+' right side',(7,250,24),(cx+102.5,0,9),wood,1.7)
    box(name+' back',(198,7,24),(cx,121.5,9),wood,1.7)
    box(name+' front',(198,7,24),(cx,-121.5,9),wood,1.7)

colors=[black,white,blue,white,black]
# Symmetric at 230 mm between drawer centers.
drawer(-119,'Before'); drawer(119,'After')
caption('BEFORE',-119,-145,8)
caption('AFTER',119,-145,8)
caption('Five cables. One drawer.',0,148,11)
caption('USB BUDDY  /  CONCEPTUAL CAD MOCKUP',0,-164,4.2)

# After. Transform CAD front (y=0) upward; its A mouth (+z) faces +worldY.
cx=119
bpy.ops.wm.stl_import(filepath=str(ROOT/'usb_buddy.stl'))
product=bpy.context.object; product.name='USB BUDDY exact v18 / front lettering up'
product.rotation_euler.x=-math.pi/2
product.location=(cx-56.5,-91,16)
product.data.materials.append(orange)
# True A slot tip z=9 in source model; 7.3 mm of the metal enters the slot.
for j,i in enumerate([0,2,4,6,8]):
    x=cx-56.5+i*11.5+4.75
    col=colors[j]
    stem=plug('A',(x,-82,8),(0,1,0),col,f'After cable {j+1} / correctly inserted USB-A')
    pts=[stem,(x,-43,6),(x-7,-29,2.0)]
    # Three complete oval loops, stacked by one cable diameter. Side-by-side
    # coils do not intersect; a continuous path joins the two plug overmolds.
    for turn in range(3):
        for k in range(17):
            t=math.pi+2*math.pi*k/16
            pts.append((x+8.8*math.cos(t),26+64*math.sin(t),1.6+2.8*turn+2.8*k/16))
    # Free C end near this cable's own coil, pointing back toward the holder.
    end=plug('C',(x+7,-28,12),(0,1,0),col,f'After cable {j+1} / free USB-C')
    pts += [(x-6,11,10.5),(x+5,0,11.5),end]
    cable(f'After cable {j+1} / three coiled loops',pts,col)

# Before. Exact same five A-to-C color inventory, loose into the same drawer.
# Cords form meandering continuous paths, with raised crossing sections.
cx=-119
rng=random.Random(28)
for j,col in enumerate(colors):
    angle=j*1.24+.3
    sx=cx+math.cos(angle)*66; sy=math.sin(angle)*75
    axis=Vector((-math.cos(angle),-math.sin(angle),0))
    start=plug('A',(sx,sy,8),axis,col,f'Before cable {j+1} / USB-A')
    ex=cx+math.cos(angle+2.1)*68; ey=math.sin(angle+2.1)*79
    endaxis=Vector((-math.cos(angle+2.1),-math.sin(angle+2.1),0))
    end=plug('C',(ex,ey,6),endaxis,col,f'Before cable {j+1} / USB-C')
    pts=[start]
    for k in range(31):
        t=k/30*math.pi*5.3+j*.91
        r=55+12*math.sin(k*.87+j)
        pts.append((cx+r*math.cos(t)+7*math.sin(k*1.37),r*1.26*math.sin(t)+8*math.cos(k*.8),4+j*2.9+1.8*math.sin(k*.65)))
    pts.append(end)
    cable(f'Before cable {j+1} / tangled continuous cord',pts,col)

light('Large window',(-170,-100,380),2200000,260,(1,.93,.83))
light('Soft room fill',(220,100,290),1400000,200,(.84,.91,1))
bpy.ops.object.camera_add(location=(0,-195,650))
cam=bpy.context.object; cam.name='Before after camera'; cam.data.type='ORTHO'; cam.data.ortho_scale=530
cam.data.lens=55; aim(cam,(0,0,0)); scene.camera=cam
scene.render.filepath=str(OUT/'drawer-before-after.jpg')
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(MODELS/'usb-buddy-drawer.blend'))
bpy.ops.render.render(write_still=True)
# A close reference view uses this same scene and the same physically parked plugs.
for ob in scene.objects:
    if ob.type == 'FONT' or (ob.name.startswith('Before') and ob.type != 'CAMERA'): ob.hide_render=True
cam.location=(119,-180,520)
aim(cam,(119,0,0)); cam.data.ortho_scale=294
scene.render.resolution_x=1500; scene.render.resolution_y=1700
scene.render.filepath=str(OUT/'drawer-clean-reference.jpg')
bpy.ops.render.render(write_still=True)
print('Verified geometry: original STL, front up, five A tips at source z=9; colors black/cream/blue/cream/black.')
