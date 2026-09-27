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
recessed on the front. On v19 it checks front/end embossing, a single closed component and unchanged connector
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

## Insertion details and mixed load

```sh
blender --background --python-exit-code 1 --python docs/render/render_details.py
```

This adds separate USB-A and USB-C insertion close-ups and `mixed-cable-load`:
four looped A-to-C cables, three A-to-Micro-B cables, three additional A-to-C
cables, and two additional cables parked by C ends. The Micro-B ends are free;
the model does not gain a micro-USB socket. The editable scenes are in
`docs/models/usb-buddy-details.blend`.

## Archived v18 orbit and drawer

The saved orbit, drawer and evening lifestyle assets are retained v18 experiments,
not linked from the README. Regenerating them uses the current STL.

`render_orbit.py` renders the exact current STL with a looping camera orbit,
including an underside view. Its docstring contains the render and encoding
commands. Deliverables are an eight-second animated GIF, an H.264 MP4 and an
editable Blender scene. Encoding uses FFmpeg.

`render_drawer.py` builds the same oak drawer twice, with five tangled cables
on one side and five color-matched organized cables on the other. The actual
v18 model lies on its back, with the wordmark facing up and the USB-A openings
facing toward the cable coils. This is a conceptual CAD mockup, not a photograph.

## Lifestyle image

`docs/images/lifestyle-sage.jpg` was edited with the built-in image generation
tool to show the v19 raised wordmark, preserving the approved scene. The README
labels it as a visualization. `lifestyle-evening.jpg` remains an unused v18 image.
The current hero edit prompt is in [`lifestyle-v19-prompt.txt`](lifestyle-v19-prompt.txt).
Original prompts are in
[`lifestyle-prompt.txt`](lifestyle-prompt.txt) and
[`lifestyle-evening-prompt.txt`](lifestyle-evening-prompt.txt).
Earlier v17 and AI drawer experiments are not part of the published asset set.
