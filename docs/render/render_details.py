"""Render insertion close-ups and a realistic mixed cable inventory.

Uses the existing scene-building functions without running their batch export.
"""
from pathlib import Path
import os
helper=Path(__file__).with_name('render_cables.py')
exec(compile(helper.read_text().split('counts={}')[0], str(helper), 'exec'))

def arrow(tip,direction,length=5):
    axis=Vector(direction)
    bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=1,radius2=0,
        depth=2,location=Vector(tip)-axis)
    o=bpy.context.object
    o.name='Insertion direction / arrowhead'
    o.rotation_euler=axis.to_track_quat('Z','Y').to_euler()
    o.data.materials.append(blue)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.28,depth=length-1,
        location=Vector(tip)-axis*(length+1)/2)
    o=bpy.context.object
    o.name='Insertion direction / stem'
    o.rotation_euler=axis.to_track_quat('Z','Y').to_euler()
    o.data.materials.append(blue)

def finish(scene,name):
    scene.render.threads_mode='FIXED'
    scene.render.threads=4
    scene.cycles.samples=48
    scene.render.filepath=str(OUT/(name+'.jpg'))
    if not os.getenv('USB_DETAIL_ONLY') or os.environ['USB_DETAIL_ONLY']==name:
        bpy.ops.render.render(write_still=True)

scene,obj=setup('detail-usb-a')
end=plug('A',(-5.75,0,25),(0,0,1),black,'USB-A / aligned for insertion')
cable('USB-A / cable',[end,(-5.75,0,66)],black)
arrow((-5.75,0,17.2),(0,0,-1),6)
scene.camera.location=(29,-83,72)
aim(scene.camera,(-5.75,0,28))
scene.camera.data.ortho_scale=77
scene.render.resolution_x=1400
scene.render.resolution_y=1300
finish(scene,'detail-usb-a')

scene,obj=setup('detail-usb-c')
end=plug('C',(-5.75,0,-7),(0,0,-1),white,'USB-C / aligned for insertion')
cable('USB-C / cable',[end,(-5.75,0,-38)],white)
arrow((-5.75,0,-.8),(0,0,1),5)
scene.camera.location=(22,-85,-56)
aim(scene.camera,(-5.75,0,-9))
scene.camera.data.ortho_scale=66
scene.render.resolution_x=1400
scene.render.resolution_y=1300
for o in scene.objects:
    if o.name.startswith('Studio backdrop'):
        o.hide_render=True
    if o.type=='LIGHT' and o.name.startswith('Key'):
        o.location=(-30,-75,-95)
        aim(o,(-5.75,0,-6))
finish(scene,'detail-usb-c')

def micro_usb(tip,axis,color,name):
    root=bpy.data.objects.new(name,None)
    bpy.context.collection.objects.link(root)
    root.location=tip
    root.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler()
    section=[(-1,-3.4),(-1,3.4),(.9,2.7),(.9,-2.7)]
    verts=[(x,y,z) for z in [0,6] for x,y in section]
    faces=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    mesh=bpy.data.meshes.new(name+' trapezoidal shell')
    mesh.from_pydata(verts,[],faces)
    shell=bpy.data.objects.new(name+' Micro-B shell',mesh)
    bpy.context.collection.objects.link(shell)
    shell.parent=root
    shell.data.materials.append(silver)
    box(name+' dark tip',(1.0,5.4,.09),(-.1,0,-.02),dark,.25,root)
    box(name+' molded housing',(5,10,10),(0,0,11),color,1.1,root)
    box(name+' strain relief',(3.8,4.5,5),(0,0,18.5),color,.8,root)
    return Vector(tip)+Vector(axis)*21

scene,obj=setup('mixed-cable-load')
for i in range(10):
    x=-56.5+i*11.5+4.75
    color=[black,blue,black,white][i%4]
    top=plug('A',(x,0,9),(0,0,1),color,f'Mixed pod {i+1} / A parked')
    if i<4:
        bottom=plug('C',(x,0,6.5),(0,0,-1),color,f'Mixed pod {i+1} / C parked')
        cable(f'Mixed pod {i+1} / continuous A-to-C loop',[
            top,(x,0,55),(x,18,65),(x,72,65),(x,90,48),
            (x,90,-17),(x,72,-35),(x,18,-35),(x,0,-28),bottom],color)
    else:
        if i in [4,6,8]:
            far=micro_usb((x,130,39),(0,-1,0),color,f'Mixed pod {i+1} / free Micro-B end')
        else:
            far=plug('C',(x,130,39),(0,-1,0),color,f'Mixed pod {i+1} / free C end')
        cable(f'Mixed pod {i+1} / single cable',[
            top,(x,0,56),(x,20,67),(x,70,67),(x,92,53),(x,99,40),far],color)
        if i in [8,9]:
            bottom=plug('C',(x,0,6.5),(0,0,-1),white,f'Mixed pod {i+1} / second C parked')
            far=plug('A',(x,138,-27),(0,-1,0),white,f'Mixed pod {i+1} / second free A end')
            cable(f'Mixed pod {i+1} / second independent cable',[
                bottom,(x,0,-30),(x,20,-42),(x,73,-42),(x,94,-30),far],white)
scene.camera.location=(150,-190,145)
aim(scene.camera,(0,48,12))
scene.camera.data.ortho_scale=232
scene.render.resolution_x=2000
scene.render.resolution_y=1400
finish(scene,'mixed-cable-load')
bpy.ops.wm.save_as_mainfile(filepath=str(MODELS/'usb-buddy-details.blend'))
print('Mixed load: 4 looped A-to-C cables; 3 A-to-Micro-B and 3 A-to-C cables parked by A; 2 additional cables parked by C. Total 12 cables,16 parked ends,10 occupied pods.')
