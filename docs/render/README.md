# Reproduce the product and cable views

The main images are deterministic Blender renders of `usb_buddy.stl`.
`render_cables.py` creates reusable illustrative USB-A and USB-C plug assemblies,
continuous Bezier cable curves, lighting, cameras and named scenes, then saves
`docs/models/usb-buddy-cable-scenes.blend` and JPEGs under `docs/images/`.

Requirements: OpenSCAD with the Manifold backend and Blender 5.1 or compatible.
Commands below run from the repository root; use your installed executable paths.

```sh
openscad --backend=Manifold --render -o usb_buddy.stl usb_buddy.scad
blender --background --python-exit-code 1 --python docs/render/check_model.py
blender --background --python-exit-code 1 --python docs/render/render_cables.py
```

The check fails on the original v17 STL because its instruction labels are
recessed on the front. On v18 it checks the end embossing and unchanged connector
interiors against `usb_buddy_v17.stl`.

## Scene inventory

| Scene | Cables | Parked ends | Occupied pods |
| --- | ---: | ---: | ---: |
| 01-cable-loop | 1 continuous A-to-C cable | 2 | 1 |
| 10-cable-loop | 10 continuous A-to-C cables | 20 | 10 |
| 01-cable-pair | 1 A-to-C cable + 1 C-to-C cable | 2 | 1 |
| 10-cable-pair | 10 A-to-C cables + 10 C-to-C cables | 20 | 10 |

These scenes use millimeters as their modeling coordinate units. Connector shells,
overmolds and cable lengths are illustrative. The file preserves named plug parts
and editable cable curves; select a named scene in Blender to explore a layout.

`pod-cutaway` removes the front half of one actual pod to show the seated tips.
The other scenes are `product-orange`, `product-sage` and `product-graphite`.
The older `render_product.py` is a simple CAD reference-render helper.

## Lifestyle image

`docs/images/lifestyle-sage.jpg` was generated with the built-in image generation
tool using the v18 sage CAD render as its reference. It is explicitly labeled as
a visualization in the README. The final prompt is in
[`lifestyle-prompt.txt`](lifestyle-prompt.txt). Earlier v17 and drawer experiments
are not part of the published asset set.
