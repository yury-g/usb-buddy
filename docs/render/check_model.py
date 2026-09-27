"""Blender geometry checks for the v19 raised-wordmark revision."""
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
assert abs(min(v.y for v in coords) + 0.6) < 0.001
for i in range(1, 9):
    assert any(v.y < -0.59 and i*11.5 < v.x < i*11.5+9.5 for v in coords), 'Each wordmark letter must be raised'
import bmesh
bm=bmesh.new(); bm.from_mesh(mesh)
assert all(e.is_manifold for e in bm.edges), 'Mesh must be closed and manifold'
remaining=set(bm.verts); components=0
while remaining:
    components+=1; stack=[remaining.pop()]
    while stack:
        for edge in stack.pop().link_edges:
            for vertex in edge.verts:
                if vertex in remaining:
                    remaining.remove(vertex); stack.append(vertex)
assert components == 1, 'Letters must be fused to the body'
print(f'Mesh: {len(bm.verts)} vertices, {len(bm.faces)} faces, one component, all edges manifold')
bm.free()
assert not any(0.01 < v.y < 0.71 and
               (2.1 < v.x < 7.4 or 105.6 < v.x < 110.9) and v.z > 2.1
               for v in coords), 'Front end pods must have no recessed instruction labels'

def interior_triangles(m):
    out = set()
    for p in m.polygons:
        vertices = [m.vertices[i].co for i in p.vertices]
        # The exterior underside can be retriangulated during a label union.
        # Compare the actual opening walls and internal faces, not that flat base.
        if (any(v.z > 0.001 for v in vertices) and
                all(1 < v.x < 112 and 1 < v.y < 15 for v in vertices)):
            out.add(tuple(sorted(tuple(round(c, 4) for c in v) for v in vertices)))
    return out
bpy.ops.wm.stl_import(filepath=str(root / 'usb_buddy_v17.stl'))
baseline = bpy.context.object.data
assert interior_triangles(mesh) == interior_triangles(baseline), 'Connector interiors changed'
print('PASS: raised end labels, clean front end pods, raised front wordmark, unchanged body and connector interiors')
