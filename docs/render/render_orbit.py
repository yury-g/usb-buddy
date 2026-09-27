"""Exact-STL floating studio orbit; outputs 120 seamless frames at 15 fps.

Run Blender with --background --threads 4 --python docs/render/render_orbit.py.
Use -- --preview for four inspection frames; -- --encode-only to encode an
existing sequence. The animated camera exposes the top, rear, underside and
both raised end labels without modifying the printable mesh.
"""
import bpy
import math
import os
import shutil
import subprocess
import sys
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
FRAMES = ROOT / '.preview' / 'orbit'
OUT = ROOT / 'docs' / 'images'
COUNT, FPS = 120, 15
FRAMES.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()


def encode():
    ffmpeg = os.environ.get('FFMPEG') or shutil.which('ffmpeg')
    if not ffmpeg:
        bundled = Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/lib'
        ffmpeg = next(bundled.glob('python*/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-*'), None)
    if not ffmpeg:
        raise RuntimeError('Set FFMPEG to the ffmpeg executable.')
    base = [str(ffmpeg), '-y', '-framerate', str(FPS), '-i', str(FRAMES / '%04d.png')]
    subprocess.run(base + ['-frames:v', str(COUNT), '-c:v', 'libx264', '-preset', 'slow',
                   '-crf', '19', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                   str(OUT / 'usb-buddy-orbit.mp4')], check=True)
    subprocess.run(base + ['-filter_complex',
        '[0:v]split[a][b];[a]palettegen=max_colors=160:stats_mode=diff[p];'
        '[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle',
        '-frames:v', str(COUNT), '-loop', '0', str(OUT / 'usb-buddy-orbit.gif')], check=True)


if '--encode-only' in sys.argv:
    encode()
    sys.exit(0)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.wm.stl_import(filepath=str(ROOT / 'usb_buddy.stl'))
product = bpy.context.object
product.name = 'USB Buddy / unmodified v18 printable STL'
minimum = Vector([min(v.co[i] for v in product.data.vertices) for i in range(3)])
maximum = Vector([max(v.co[i] for v in product.data.vertices) for i in range(3)])
product.location = -(minimum + maximum) / 2
print('Exact STL dimensions:', tuple(maximum - minimum), 'triangles:', len(product.data.polygons))
mat = bpy.data.materials.new('Matte tangerine PLA')
mat.use_nodes = True
principled = mat.node_tree.nodes.get('Principled BSDF')
principled.inputs['Base Color'].default_value = (.82, .17, .022, 1)
principled.inputs['Roughness'].default_value = .46
product.data.materials.clear()
product.data.materials.append(mat)

scene = bpy.context.scene
scene.name = 'USB Buddy / seamless floating orbit'
scene.render.engine = 'CYCLES'
scene.cycles.samples = 24
scene.cycles.use_denoising = True
scene.render.threads_mode = 'FIXED'
scene.render.threads = 4
scene.render.resolution_x = 1024
scene.render.resolution_y = 640
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'
scene.render.fps = FPS
scene.frame_start = 0
scene.frame_end = COUNT - 1
scene.view_settings.view_transform = 'AgX'
scene.world = bpy.data.worlds.new('Warm ivory studio')
scene.world.use_nodes = True
nodes = scene.world.node_tree.nodes
links = scene.world.node_tree.links
nodes.clear()
output = nodes.new('ShaderNodeOutputWorld')
mix = nodes.new('ShaderNodeMixShader')
ray = nodes.new('ShaderNodeLightPath')
ambient = nodes.new('ShaderNodeBackground')
ambient.inputs['Color'].default_value = (.67, .72, .80, 1)
ambient.inputs['Strength'].default_value = .35
backdrop = nodes.new('ShaderNodeBackground')
backdrop.inputs['Color'].default_value = (.66, .64, .60, 1)
backdrop.inputs['Strength'].default_value = 1
links.new(ray.outputs['Is Camera Ray'], mix.inputs[0])
links.new(ambient.outputs[0], mix.inputs[1])
links.new(backdrop.outputs[0], mix.inputs[2])
links.new(mix.outputs[0], output.inputs['Surface'])

bpy.ops.object.camera_add()
camera = bpy.context.object
camera.name = 'Full 360 orbit / periodic elevation'
camera.data.type = 'ORTHO'
camera.data.ortho_scale = 142
camera.data.lens = 50
scene.camera = camera


def softbox(name, energy, size, color):
    data = bpy.data.lights.new(name, 'AREA')
    data.energy, data.size, data.color = energy, size, color
    data.shape = 'DISK'
    obj = bpy.data.objects.new(name, data)
    scene.collection.objects.link(obj)
    return obj

key = softbox('Traveling broad key', 520000, 100, (1, .91, .80))
fill = softbox('Traveling soft fill', 230000, 100, (.78, .87, 1))
rim = softbox('Traveling edge softbox', 350000, 80, (1, .84, .65))

# Include the matching frame at t=1 for continuous saved animation curves, but
# export only 0..119 so the seam has the same timing as every other step.
for frame in range(COUNT + 1):
    phase = 2 * math.pi * frame / COUNT
    azimuth = math.radians(-60) + phase
    elevation = math.radians(5 + 45 * math.cos(phase))
    direction = Vector((math.cos(elevation) * math.cos(azimuth),
                        math.cos(elevation) * math.sin(azimuth), math.sin(elevation)))
    camera.location = direction * 240
    aim(camera, (0, 0, 0))
    camera.keyframe_insert('location', frame=frame)
    camera.keyframe_insert('rotation_euler', frame=frame)
    right = Vector((-math.sin(azimuth), math.cos(azimuth), 0))
    up = direction.cross(right)
    for obj, loc in ((key, direction * 95 - right * 70 + up * 110),
                     (fill, direction * 70 + right * 110 + up * 20),
                     (rim, -direction * 95 + right * 25 + up * 105)):
        obj.location = loc
        aim(obj, (0, 0, 0))
        obj.keyframe_insert('location', frame=frame)
        obj.keyframe_insert('rotation_euler', frame=frame)

scene.frame_set(0)
scene.render.filepath = str(FRAMES / '')
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / 'docs/models/usb-buddy-orbit.blend'))
preview = '--preview' in sys.argv
for frame in ([0, 30, 60, 90] if preview else range(COUNT)):
    scene.frame_set(frame)
    scene.render.filepath = str(FRAMES / f'{frame:04d}.png')
    bpy.ops.render.render(write_still=True)
if not preview:
    encode()
