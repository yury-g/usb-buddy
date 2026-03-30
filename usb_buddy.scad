// USB BUDDY Ñ v6
// Front: C | U S B B U D D Y | A
// Rear: y u r y g [BT] 2 0 2 6  Ñ Bluetooth symbol on pod 5

num_slots   = 10;
wall        = 2.0;
strip_t     = 0.9;
gap         = 1.2;
depth       = 0.7;

a_w         = 12.0;
a_h         = 5.5;
a_cap       = 2.0;
a_floor     = 1.6;

c_w         = 8.31;
c_h         = 3.2;
c_cap       = 2.0;
c_floor     = 1.6;

pod_y       = a_w + wall * 2;
pod_x       = a_h + wall * 2;
pod_z       = c_floor + c_h + c_cap + a_floor + a_h + a_cap;

c_slot_z    = c_floor;
a_slot_z    = c_floor + c_h + c_cap + a_floor;

pitch       = pod_x + gap;
strip_len   = num_slots * pod_x + (num_slots - 1) * gap;

vent_w      = 1.6;
vent_d      = pod_y - 4.0;

front_letters = ["", "U", "S", "B", "B", "U", "D", "D", "Y", ""];
rear_letters  = ["y", "u", "r", "y", "g", "", "2", "0", "2", "6"];

// Bluetooth symbol as 2D polygon, centered at origin, h = total height
module bt_symbol_2d(h) {
    s = h * 0.08;  // stroke width
    // Vertical spine
    translate([-s/2, -h/2])
        square([s, h]);
    // Upper-right arm: spine top -> right-middle -> spine center
    hull() {
        translate([-s/2, h*0.25])  square([s, s]);
        translate([h*0.32, h*0.0])  square([s, s]);
    }
    hull() {
        translate([h*0.32, h*0.0])  square([s, s]);
        translate([-s/2, -h*0.27]) square([s, s]);
    }
    // Lower-right arm: spine center -> right-lower -> spine bottom
    hull() {
        translate([-s/2, -h*0.27]) square([s, s]);
        translate([h*0.32, -h*0.48]) square([s, s]);
    }
    hull() {
        translate([h*0.32, -h*0.48]) square([s, s]);
        translate([-s/2, -h*0.5-s]) square([s, s]);
    }
}

module cut_front(txt, sz, cx, cz) {
    translate([cx, depth - 0.01, cz])
        rotate([90, 0, 0])
            linear_extrude(depth + 0.01)
                text(txt, size=sz, halign="center", valign="center",
                     font="Liberation Sans:style=Bold");
}

module cut_rear(txt, sz, cx, cz) {
    translate([cx, pod_y - depth + 0.01, cz])
        rotate([-90, 0, 0])
            linear_extrude(depth + 0.01)
                text(txt, size=sz, halign="center", valign="center",
                     font="Liberation Sans:style=Bold");
}

module cut_rear_bt(cx, cz, h) {
    translate([cx, pod_y - depth + 0.01, cz])
        rotate([-90, 0, 0])
            linear_extrude(depth + 0.01)
                translate([0, -h/2])
                    bt_symbol_2d(h);
}

module pod(idx) {
    fl = front_letters[idx];
    rl = rear_letters[idx];
    difference() {
        cube([pod_x, pod_y, pod_z]);

        // USB-C oval slot
        translate([0, 0, c_slot_z])
            oval_centered(c_w, pod_x/2, pod_y/2, c_h + c_cap + 0.1);

        // USB-A rect slot
        translate([wall, wall, a_slot_z])
            cube([a_h, a_w, a_h + a_cap + 0.1]);

        // Floor vent
        translate([pod_x/2 - vent_w/2, pod_y/2 - vent_d/2, -0.1])
            cube([vent_w, vent_d, c_floor + 0.2]);

        // Front: USBBUDDY
        if (fl != "") {
            cut_front(fl, 4.5, pod_x/2, pod_z * 0.5);
        }
        if (idx == 0) {
            cut_front("C", 3.2, pod_x/2, pod_z * 0.65);
            cut_front("v", 2.8, pod_x/2, pod_z * 0.22);
        }
        if (idx == num_slots - 1) {
            cut_front("A", 3.2, pod_x/2, pod_z * 0.78);
            cut_front("^", 2.8, pod_x/2, pod_z * 0.55);
        }

        // Rear: one char per pod, BT symbol on pod 5
        if (idx == 5) {
            cut_rear_bt(pod_x/2, pod_z * 0.5, 5.0);
        } else if (rl != "") {
            cut_rear(rl, 4.5, pod_x/2, pod_z * 0.5);
        }
    }
}

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
