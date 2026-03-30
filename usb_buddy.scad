// USB BUDDY Ñ v1
// Combined USB-A (top) + USB-C (bottom) cable holder
// 10 pods on compliant flex strip
// Front face: U S B B U D D Y (8 pods) + 2 end pods
// Rear face: USB-C-> (left, normal) | label windows (middle) | <-USB-A (right, upside down)
// Each pod: USB-A slot on top, USB-C oval slot on bottom, shared middle wall

// ?? Shared params ??????????????????????????????????????????
num_slots  = 10;
wall       = 2.0;
strip_t    = 0.9;
gap        = 1.2;
depth      = 0.7;   // label emboss depth

// ?? USB-A slot ?????????????????????????????????????????????
a_w        = 12.0;   // slot width (Y)
a_h        = 5.5;    // slot height (X)
a_cap      = 2.0;    // grip cap above slot
a_floor    = 1.6;    // floor under A slot (= shared wall top)

// ?? USB-C slot ?????????????????????????????????????????????
c_w        = 8.31;   // oval width (Y)
c_h        = 3.2;    // oval height (X)
c_cap      = 2.0;    // grip cap above C slot
c_floor    = 1.6;    // floor under C slot (= pod base)

// ?? Pod dimensions ?????????????????????????????????????????
// Pod Y: must fit USB-A width (widest) + walls
pod_y      = a_w + wall * 2;              // 16.0mm

// Pod X: must fit USB-A height + walls
pod_x      = a_h + wall * 2;              // 9.5mm

// Pod Z stacking bottom to top:
//   strip_t (flex strip, separate)
//   c_floor (USB-C base)
//   c_h + c_cap (USB-C slot zone + grip)  = shared wall top = USB-A floor bottom
//   a_floor (shared wall = USB-A floor)
//   a_h + a_cap (USB-A slot zone + grip)
// Total pod height (above strip):
shared_wall = 1.6;   // middle wall: C cap doubles as A floor
pod_z       = c_floor + c_h + c_cap + a_h + a_cap;
// = 1.6 + 3.2 + 2.0 + 5.5 + 2.0 = 14.3mm

// Z positions (within pod, strip handled separately)
c_slot_z   = c_floor;                          // C slot starts here
c_top_z    = c_floor + c_h + c_cap;            // top of C zone = bottom of A floor
a_slot_z   = c_top_z + shared_wall;            // A slot starts here
a_top_z    = a_slot_z + a_h + a_cap;           // top of pod

pitch      = pod_x + gap;
strip_len  = num_slots * pod_x + (num_slots - 1) * gap;

vent_w     = 1.6;
vent_d     = pod_y - 4.0;

// ?? Letter map ?????????????????????????????????????????????
// Front face pods 0-9: _ U S B B U D D Y _
// Pod 0 and 9 = end markers (arrows or blank)
front_letters = ["", "U", "S", "B", "B", "U", "D", "D", "Y", ""];

// ?? Oval for USB-C ?????????????????????????????????????????
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

// ?? Label cuts ?????????????????????????????????????????????
module cut_front(txt, sz, cx, cz) {
    translate([cx, depth - 0.01, cz])
        rotate([90, 0, 0])
            linear_extrude(depth + 0.01)
                text(txt, size=sz, halign="center", valign="center",
                     font="Liberation Sans:style=Bold");
}

module cut_rear_normal(txt, sz, cx, cz) {
    translate([cx, pod_y - depth + 0.01, cz])
        rotate([-90, 0, 0])
            linear_extrude(depth + 0.01)
                text(txt, size=sz, halign="center", valign="center",
                     font="Liberation Sans:style=Bold");
}

module cut_rear_upsidedown(txt, sz, cx, cz) {
    translate([cx, pod_y - depth + 0.01, cz])
        rotate([-90, 0, 0])
            linear_extrude(depth + 0.01)
                rotate([0, 0, 180])
                    text(txt, size=sz, halign="center", valign="center",
                         font="Liberation Sans:style=Bold");
}

// Recessed label window on rear face
module label_window(cx, cz, w, h) {
    translate([cx - w/2, pod_y - 0.5, cz - h/2])
        rotate([-90, 0, 0])
            linear_extrude(0.6)
                square([w, h]);
}

// ?? Pod ????????????????????????????????????????????????????
module pod(idx) {
    fl = front_letters[idx];

    difference() {
        cube([pod_x, pod_y, pod_z]);

        // ?? USB-C slot (bottom zone) ??
        // Oval cuts from c_slot_z through c_h + c_cap (open top of C zone)
        translate([0, 0, c_slot_z])
            oval_centered(c_w, pod_x/2, pod_y/2, c_h + c_cap + 0.1);

        // ?? USB-A slot (top zone) ??
        // Rectangular slot cuts from a_slot_z through a_h + a_cap
        translate([wall, wall, a_slot_z])
            cube([a_h, a_w, a_h + a_cap + 0.1]);

        // ?? Floor vent through C floor ??
        translate([pod_x/2 - vent_w/2, pod_y/2 - vent_d/2, -0.1])
            cube([vent_w, vent_d, c_floor + 0.2]);

        // ?? Front face: USBBUDDY letters ??
        if (fl != "") {
            cut_front(fl, 4.5, pod_x/2, pod_z * 0.5);
        }

        // ?? Front face: end pod arrows ??
        if (idx == 0) {
            cut_front("C", 3.5, pod_x/2, pod_z * 0.65);
            cut_front("v", 3.0, pod_x/2, pod_z * 0.25);
        }
        if (idx == num_slots - 1) {
            cut_front("A", 3.5, pod_x/2, pod_z * 0.65);
            cut_front("^", 3.0, pod_x/2, pod_z * 0.25);
        }

        // ?? Rear face labels ??
        // Left 2 pods: USB-C -> (normal orientation)
        if (idx == 0) {
            cut_rear_normal("USB-C", 2.2, pod_x/2, pod_z * 0.65);
            cut_rear_normal(">>>",   2.0, pod_x/2, pod_z * 0.30);
        }
        if (idx == 1) {
            cut_rear_normal("insert", 1.6, pod_x/2, pod_z * 0.65);
            cut_rear_normal("below",  1.6, pod_x/2, pod_z * 0.30);
        }

        // Right 2 pods: USB-A upside down
        if (idx == num_slots - 1) {
            cut_rear_upsidedown("USB-A", 2.2, pod_x/2, pod_z * 0.65);
            cut_rear_upsidedown("<<<",   2.0, pod_x/2, pod_z * 0.30);
        }
        if (idx == num_slots - 2) {
            cut_rear_upsidedown("insert", 1.6, pod_x/2, pod_z * 0.65);
            cut_rear_upsidedown("above",  1.6, pod_x/2, pod_z * 0.30);
        }

        // Middle 6 pods rear: recessed label windows
        if (idx >= 2 && idx <= num_slots - 3) {
            label_window(pod_x/2, pod_z * 0.5, pod_x - wall, 4.0);
        }
    }
}

// ?? Compliant strip ????????????????????????????????????????
difference() {
    cube([strip_len, pod_y, strip_t]);
    for (i = [0 : num_slots - 1]) {
        ox = i * pitch;
        translate([ox + pod_x/2 - vent_w/2, pod_y/2 - vent_d/2, -0.1])
            cube([vent_w, vent_d, strip_t + 0.2]);
    }
}

// ?? Place pods ?????????????????????????????????????????????
for (i = [0 : num_slots - 1]) {
    translate([i * pitch, 0, strip_t])
        pod(i);
}
