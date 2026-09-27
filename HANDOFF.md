# USB Buddy — current design notes

## v18 · September 27, 2026

User-approved change: move the A/C instructions off the front onto the two
outer end faces. Use the same font and size, with raised letters and arrows.
Keep the recessed USB BUDDY wordmark.

- Letters: Liberation Sans Bold, 4.2 mm nominal text size.
- Relief: 0.6 mm, overlapping the body by 0.05 mm for a solid union.
- Left end: C and downward arrow. Right end: A and upward arrow.
- Original body: 113 × 16 × 16.3 mm.
- Including relief: 114.2 × 16 × 16.3 mm.
- Pod body: 9.5 × 16 × 15.1 mm, on a 1.2 mm base.
- Gap: 2 mm. Pod pitch: 11.5 mm. Count: 10.
- Slot dimensions unchanged: A 12 × 5.5 mm; C 8.31 × 3.2 mm.

## Validation and limits

OpenSCAD Manifold export reports NoError, genus 10. Blender geometry checks
confirm raised end bounds, blank front end pods, unchanged height/depth,
and identical interior triangles compared with the preserved v17 STL.

The old notes reported physical testing for the A and C opening dimensions.
No new physical print or cable retention test has been performed for v18.
Check raised-label readability, print quality and retention with actual cables.

The source's cuts overlap to form a continuous stepped passage. The old
description of enclosed internal air cavities is not an accurate description
of the current mesh. The older height estimate of approximately 17.6 mm is also
superseded by the measured 16.3 mm body height including base.

## Visualization models

The Blender file has named scenes for one and ten A-to-C cable loops, one and
ten pairs of separate cables, a pod section, and three product colors.
The plugs and cables are illustrative models built for these renders; they
are not certified connector models or a physical fit validation.

In the modeled parked configuration, the A metal tip ends at z=9 mm and the C
tip at z=6.5 mm. This leaves a 2.5 mm gap in the visualization. The holder is
passive storage and does not electrically join either connector.

Drawer concepts are deferred at the user's request and are excluded from the
page. The only AI-generated published image is the clearly captioned sage
desk lifestyle view; mechanism images use the actual mesh.

## Earlier records

The unmodified [v17 handoff](docs/archive/HANDOFF-v17.md) and
[v17 README](docs/archive/README-v17.md) preserve the prior session history.
Some named fit-test files in those records are not included in this repository.
