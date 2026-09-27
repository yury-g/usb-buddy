# v18 computational checks

Checked September 27, 2026. No physical print was made during this update.

## Geometry

- OpenSCAD Manifold backend: NoError, genus 10.
- One connected, closed mesh: 2,328 welded vertices, 4,692 faces.
- Zero nonmanifold edges.
- Overall bounds: 114.2 × 16 × 16.3 mm.
- Original connector interior faces match v17. The change removes the old
  front A/C instructions and adds 0.6 mm raised markings on the outer end faces.
- `usb_buddy.stl` and `usb_buddy_v18.stl` are identical copies of the current model.

## Reference slice

BambuStudio 02.00.03.54 completed the slice with exit code 0:

| Setting | Value |
| --- | --- |
| Reference printer profile | Bambu Lab A1, 0.4 mm nozzle |
| Filament | Generic PLA |
| Layer height | 0.2 mm |
| Infill | 20% |
| Orientation | Flat connecting strip on bed |
| Supports / raft / brim / skirt | Disabled |
| Layers | 81 |
| Estimated model filament | 16.63 g |
| Support metadata | support_used=false |

The reference profile is a computational check, not a requirement to own an A1.
The STL contains geometry only; it does not contain printer-specific G-code.

## Limits and messages

The slice reported no unsupported-region warning. Some paths are classified as
overhang walls, including raised-label paths, and internal paths include bridging
at z=7.2 mm. The physical appearance and retention still need a print check.

The successful slice logged seven internal `ZFiller: encounter idx from clip`
messages and a warning about the Generic PLA profile's 65°C textured-plate
temperature. It is therefore not described as a warning-free validation.

Support-free does not mean zero waste: ordinary printer priming can still consume
filament. No support structures, raft, brim, separate assembly or extra hardware
are specified for this design's reference configuration.
