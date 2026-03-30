# USB BUDDY

A 3D-printable combined USB-A + USB-C cable organizer strip.

10 pods on a compliant flex strip. USB-A inserts from the **top**, USB-C from the **bottom**. Prints flat, used standing upright. Each pod is a separate island connected by a thin flexible base.

## Design Features
- 10 pods, each holding one USB-A and one USB-C cable
- 2mm chamfered vertical edges
- Front face: **USBBUDDY** (one letter per pod)
- Rear face: **yuryg 2026** (maker mark)
- End pods labeled with connector type and direction
- 1.2mm flex strip base, 2.0mm gaps between pods
- Internal air separation between USB-A and USB-C zones
- USB slots are the only airflow (no separate vents)

## Slot Dimensions (locked from physical fit testing)
| Connector | Width | Height | Shape |
|---|---|---|---|
| USB-A | 12.0mm | 5.5mm | Rectangle |
| USB-C | 8.31mm | 3.2mm | Oval |

## Files
- `usb_buddy.scad` Ñ OpenSCAD source
- `usb_buddy.stl` Ñ Latest print-ready STL (v17)

---

## All STLs Made This Session

### USB-A Fit Test Strip
| File | Description | Date |
|---|---|---|
| `usba_cable_holder_v8final.stl` | USB-A fit test, 10 graduated slots 13.5?11.25mm | Mar 28, 2026 15:34 |
| `usba_cable_holder_v8_2026-03-28.stl` | USB-A locked at 12.0mm, v8 final production | Mar 28, 2026 15:35 |

### USB-C Fit Test Strips
| File | Description | Date |
|---|---|---|
| `usbc_fittest_8.65-7.30mm_v8_2026-03-28.stl` | USB-C fit test, 10 slots 8.65?7.30mm (0.15mm steps) | Mar 28, 2026 15:40 |
| `usbc_fittest_8.55-8.10mm_v9_2026-03-28.stl` | USB-C fit test, recentered 8.55?8.10mm (0.05mm steps) | Mar 28, 2026 17:20 |
| `usbc_fittest_8.55-8.10mm_v9b_2026-03-28.stl` | USB-C v9b Ñ open slot top restored, cap 2mm | Mar 28, 2026 17:23 |
| `usbc_fittest_8.45-8.27mm_v9c_2026-03-28.stl` | USB-C fine test, 8.45?8.27mm (0.02mm steps) | Mar 28, 2026 17:25 |
| `usbc_holder_8.31mm_v10final_2026-03-28.stl` | USB-C LOCKED 8.31mm, all 10 slots identical Ñ final | Mar 28, 2026 19:18 |

### USB Buddy (Combined)
| File | Description | Date |
|---|---|---|
| `usb_buddy_v13_2026-03-30.stl` | USB Buddy v13 Ñ BT symbol removed, clean rear | Mar 30, 2026 14:45 |
| `usb_buddy_v16_2mm_chamfer_2026-03-30.stl` | USB Buddy v16 Ñ 2mm chamfer, pre-strip-change | Mar 30, 2026 14:52 |
| `usb_buddy.stl` | USB Buddy v17 Ñ 1.2mm strip, 2mm gaps, CURRENT | Mar 30, 2026 14:59 |

---

## Print Settings (recommended)
- Material: PLA
- Layer height: 0.2mm
- Infill: 20%+
- Supports: None needed
- Orientation: Print flat (as designed), flex strip on bed

## How to Render
```bash
/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD --render -o usb_buddy.stl usb_buddy.scad
```

## Fit Test History
Starting from large and stepping down, physical cable testing found:
- **USB-A best fit: 12.0mm** (from 13.5?11.25mm range test)
- **USB-C best fit: 8.31mm** (narrowed through 3 rounds of testing)

## By
yury-g Ñ 2026
