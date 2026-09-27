"""Blender geometry checks for the v18 label-only revision."""
import bpy
from pathlib import Path
root = Path(__file__).resolve().parents[2]
bpy.ops.wm.stl_import(filepath=str(root / 'usb_buddy.stl'))
mesh = bpy.context.object.data
coords = [v.co for v in mesh.vertices]
assert min(v.x for v in coords) < -0.35, 'USB-C end label must be raised on left end'
assert max(v.x for v in coords) > 113.35, 'USB-A end label must be raised on right end'
assert abs(max(v.z for v in coords) - 16.3) < 0.001
assert abs(max(v.y for v in coords) - 16) < 0.001
assert not any(0.01 < v.y < 0.71 and
               (2.1 < v.x < 7.4 or 105.6 < v.x < 110.9) and v.z > 2.1
               for v in coords), 'Front end pods must have no recessed instruction labels'

def interior_triangles(m):
    out = set()
    for p in m.polygons:
        vertices = [m.vertices[i].co for i in p.vertices]
        if all(1 < v.x < 112 and 1 < v.y < 15 for v in vertices):
            out.add(tuple(sorted(tuple(round(c, 4) for c in v) for v in vertices)))
    return out
bpy.ops.wm.stl_import(filepath=str(root / 'usb_buddy_v17.stl'))
baseline = bpy.context.object.data
assert interior_triangles(mesh) == interior_triangles(baseline), 'Connector interiors changed'
print('PASS: raised end labels, clean front end pods, unchanged height/depth and connector interiors')
