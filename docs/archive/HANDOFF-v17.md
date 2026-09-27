# USB BUDDY Ñ Handoff to Next Claude Session
## Project Location
Machine: Mac Mini (mininarwhal)
Path: ~/Documents/usb-buddy/
Git: initialized, currently at v17 (main branch)
Tag: v16-chamfer-good (last fully clean version)

## What This Is
USB BUDDY is a 10-pod cable organizer strip that holds both USB-A and USB-C cables.
- USB-A male connector inserts from the TOP of each pod
- USB-C male connector inserts from the BOTTOM of each pod
- Both slots share the same pod Ñ stacked vertically
- 10 pods connected by a flexible strip (0.9mm compliant hinge base)
- Prints flat on bed, used standing upright

## Current Design State (v17)
File: usb_buddy.scad + usb_buddy.stl

### Key Dimensions
- wall = 2.0mm
- strip_t = 1.2mm (thickened from 0.9 for strength)
- gap = 2.0mm between pods (widened for flex)
- ch = 2.0mm chamfer on vertical pod edges (starts at z=ch from base)
- pod_x = 9.5mm (along strip, sized to USB-A height + walls)
- pod_y = 16.0mm (front to back)
- pod_z = ~17.6mm total height

### Z Stack (pod-local, above strip):
- 0..1.6mm       = USB-C base floor
- 1.6..4.8mm     = USB-C oval slot (8.31mm wide x 3.2mm tall)
- 4.8..6.8mm     = USB-C cap/grip (2mm)
- 6.8..7.6mm     = 0.8mm separator (structural, internal air gap cut through it)
- 7.6..13.1mm    = USB-A rect slot (12.0mm wide x 5.5mm tall)
- 13.1..15.1mm   = USB-A cap/grip (2mm)

### Slot Dimensions (locked from physical fit test prints):
- USB-A: 12.0mm wide x 5.5mm tall (rectangular)
- USB-C: 8.31mm wide x 3.2mm tall (oval Ñ hull of two circles)

### Front Face Labels (USBBUDDY):
pods: [blank, U, S, B, B, U, D, D, Y, blank]
- Pod 0 (left end): C marker + v arrow (USB-C indicator, bottom insert)
- Pod 9 (right end): A marker + ^ arrow (USB-A indicator, top insert)

### Rear Face Labels:
pods: [y, u, r, y, g, blank, 2, 0, 2, 6]
reads: yuryg 2026

## Git History Summary
- v1: initial combined A+C design
- v5: yuryg_2026 rear labels
- v10f: no vents (USB slots ARE the airflow), Genus 0 manifold Ñ GOOD BASE
- v13: BT symbol removed, pod 5 rear blank
- v14: thin separator replaces blocking shelf
- v15: 1mm chamfer added
- v16: chamfer increased to 2mm Ñ TAG: v16-chamfer-good
- v17: strip 1.2mm, gap 2.0mm, chamfer starts at z=ch (current)

## Mesh Status
- manifold: NoError (printable)
- Genus: 10 (10 enclosed internal air cavities Ñ expected, not a print issue)
- Slicers (Bambu/Prusa) handle this fine

## Known Issues / Next Steps
1. Genus 10 is benign but worth resolving cleanly Ñ the air gap internal
   cavity creates enclosed voids. Could remove the air gap cut entirely
   (sep=0.8mm is thin enough electrically) or find a way to connect it
   to an outer face without breaching walls.
2. Labels on end pods (C/v and A/^) need position review Ñ may be
   too close together vertically given the new pod_z height.
3. Consider adding a small text label on the TOP EDGE of each pod
   (reads when looking down) Ñ good for desk use.
4. USB-C test strip (separate file in ~/Documents/usb-holders/) confirmed
   8.31mm as best fit from physical testing.
5. USB-A test strip confirmed 12.0mm as best fit.
6. Both test STLs in ~/Downloads/ with dated filenames.

## How to Push to GitHub (manual step needed)
gh CLI not installed on Mini. To push:
  cd ~/Documents/usb-buddy
  git remote add origin https://github.com/yury-g/usb-buddy.git
  git push -u origin main
  git push --tags

Or install gh CLI first:
  brew install gh
  gh auth login
  gh repo create usb-buddy --public --source=. --remote=origin --push

## Related Projects
- ~/Documents/usb-holders/ Ñ USB-A and USB-C fit test strips (v8-final, v10-final)
  Both have their own git repos. USB-A locked at 12.0mm, USB-C locked at 8.31mm.
- ~/Documents/sh1106-comparison/ Ñ SH1106 OLED comparison (parked)

## SSH Access (from M4 Air or anywhere)
ssh mininarwhal (via ~/.ssh/config alias)
or: ssh mininarwhal@192.168.1.26

## OpenSCAD Render Command
/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD --render -o usb_buddy.stl usb_buddy.scad

## File Write Pattern (AppleScript Ñ ONLY method that works)
set code to "// scad content here"
set fp to open for access (POSIX file "/Users/mininarwhal/Documents/usb-buddy/usb_buddy.scad") with write permission
set eof fp to 0
write code to fp
close access fp

## Design Philosophy
- Minimal material Ñ walls only as thick as needed for grip strength
- USB slots are the only airflow (no separate vents needed)
- Flex strip connects pods Ñ prints flat, flexes at gaps when standing
- Labels serve dual purpose: product identity (front) + maker mark (rear)
- 2mm chamfer on vertical edges for feel and print quality
