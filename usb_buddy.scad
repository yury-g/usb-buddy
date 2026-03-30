// USB BUDDY Ñ v2
// Front: C | U S B B U D D Y | A  (end pods have connector markers)
// Rear: blank (write-in later)
// USB-A slot: 12.0mm wide x 5.5mm tall, locked from final print
// USB-C slot: 8.31mm oval x 3.2mm tall, locked from final print
// wall=2.0, floor=1.6, cap=2.0 both ends
// Islands on 0.9mm flex strip, floor vent only

num_slots   = 10;
wall        = 2.0;
strip_t     = 0.9;
gap         = 1.2;
depth       = 0.7;

// USB-A dims (final printed)
a_w         = 12.0;
a_h         = 5.5;
a_cap       = 2.0;
a_floor     = 1.6;

// USB-C dims (final printed)
c_w         = 8.31;
c_h         = 3.2;
c_cap       = 2.0;
c_floor     = 1.6;

// Pod footprint Ñ sized to fit USB-A (widest)
pod_y       = a_w + wall * 2;     // 16.0mm front to back
pod_x       = a_h + wall * 2;     // 9.5mm along strip

// Pod Z stack (bottom to top, above strip):
//   c_floor = 1.6   USB-C base floor
//   c_h     = 3.2   USB-C slot zone
//   c_cap   = 2.0   USB-C grip cap = shared middle wall top
//   a_floor = 1.6   shared middle wall (USB-A floor)
//   a_h     = 5.5   USB-A slot zone
//   a_cap   = 2.0   USB-A grip cap
pod_z       = c_floor + c_h + c_cap + a_floor + a_h + a_cap;  // 15.9mm

c_slot_z    = c_floor;
a_slot_z    = c_floor + c_h + c_cap + a_floor;

pitch       = pod_x + gap;
strip_len   = num_slots * pod_x + (num_slots - 1) * gap;

vent_w      = 1.6;
vent_d      = pod_y - 4.0;

front_letters = ["", "U", "S", "B", "B", "U", "D", "D", "Y", ""];

module oval_centered(sw, cx, cy, h) {
    r   = c_h / 2;
    sep = sw - c_h;
    translate([cx, cy - sep/2, 0])
        hull() {
            cylinder(h = h, r = r, $fn = 32);
            translate([0, sep, 0])
                cylinder(h = h, r = r, $fn = 32);
        }
}

module cut_front(txt, sz, cx, cz) {
    translate([cx, depth - 0.01, cz])
        rotate([90, 0, 0])
            linear_extrude(depth + 0.01)
                text(txt, size=sz, halign="center", valign="center",
                     font="Liberation Sans:style=Bold");
}

module pod(idx) {
    fl = front_letters[idx];
    difference() {
        cube([pod_x, pod_y, pod_z]);

        // USB-C oval slot Ñ bottom zone, cuts through c_h + c_cap (open top of C)
        translate([0, 0, c_slot_z])
            oval_centered(c_w, pod_x/2, pod_y/2, c_h + c_cap + 0.1);

        // USB-A rectangular slot Ñ top zone, cuts through a_h + a_cap (open top)
        translate([wall, wall, a_slot_z])
            cube([a_h, a_w, a_h + a_cap + 0.1]);

        // Floor vent through C floor only
        translate([pod_x/2 - vent_w/2, pod_y/2 - vent_d/2, -0.1])
            cube([vent_w, vent_d, c_floor + 0.2]);

        // Front face: USBBUDDY letters (pods 1-8)
        if (fl != "") {
            cut_front(fl, 4.5, pod_x/2, pod_z * 0.5);
        }

        // Front face: end pod connector markers
        if (idx == 0) {
            cut_front("C", 3.2, pod_x/2, pod_z * 0.65);
            cut_front("v", 2.8, pod_x/2, pod_z * 0.22);
        }
        if (idx == num_slots - 1) {
            cut_front("A", 3.2, pod_x/2, pod_z * 0.78);
            cut_front("^", 2.8, pod_x/2, pod_z * 0.55);
        }

        // Rear face: BLANK Ñ nothing cut here
    }
}

// Compliant strip
difference() {
    cube([strip_len, pod_y, strip_t]);
    for (i = [0 : num_slots - 1]) {
        ox = i * pitch;
        translate([ox + pod_x/2 - vent_w/2, pod_y/2 - vent_d/2, -0.1])
            cube([vent_w, vent_d, strip_t + 0.2]);
    }
}

// Pods
for (i = [0 : num_slots - 1]) {
    translate([i * pitch, 0, strip_t])
        pod(i);
}
