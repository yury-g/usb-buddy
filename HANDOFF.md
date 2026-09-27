# USB Buddy — current design notes

## v19 · September 27, 2026

User-approved change: move the A/C instructions off the front onto the two
outer end faces. Use the same font and size, with raised letters and arrows.
The later user-approved revision raises the front USB BUDDY wordmark as well.
The rear maker/date mark remains recessed.

- Letters: Liberation Sans Bold, 4.2 mm end labels and 4.5 mm front wordmark.
- Relief: 0.6 mm, overlapping the body by 0.05 mm for a solid union.
- Left end: C and downward arrow. Right end: A and upward arrow.
- Original body: 113 × 16 × 16.3 mm.
- Including relief: 114.2 × 16.6 × 16.3 mm.
- Pod body: 9.5 × 16 × 15.1 mm, on a 1.2 mm base.
- Gap: 2 mm. Pod pitch: 11.5 mm. Count: 10.
- Slot dimensions unchanged: A 12 × 5.5 mm; C 8.31 × 3.2 mm.

## Validation and limits

OpenSCAD Manifold export reports NoError, genus 10. Blender geometry checks
confirm raised end bounds, blank front end pods, unchanged body height/depth,
and identical interior triangles compared with the preserved v17 STL.

The old notes reported physical testing for the A and C opening dimensions.
No new physical print or cable retention test has been performed for v19.
Check raised-label readability, print quality and retention with actual cables.

The source's cuts overlap to form a continuous stepped passage. The old
description of enclosed internal air cavities is not an accurate description
of the current mesh. The older height estimate of approximately 17.6 mm is also
superseded by the measured 16.3 mm body height including base.

## Visualization models

The front page uses the updated mint-green lifestyle hero, A/C insertion close-ups,
and mixed cable load: four complete A-to-C loops, six cables parked by A (three
with Micro-B loose ends), and two additional cables parked by C. The current CAD
product/cable renders and their two Blender scene files use v19. The hero was
edited with built-in image generation to show raised letters.

The drawer, orbit and evening lifestyle assets are retained v18 experiments,
removed from the README. Their saved scenes/images are not current model previews.

The current download is `usb_buddy_v19.stl`; `usb_buddy.stl` is an identical alias.
The v18 STL preserves the former recessed front wordmark. See
[validation details](docs/verification.md) for computational checks and limits.

## Earlier records

The unmodified [v17 handoff](docs/archive/HANDOFF-v17.md) and
[v17 README](docs/archive/README-v17.md) preserve the prior session history.
Some named fit-test files in those records are not included in this repository.
