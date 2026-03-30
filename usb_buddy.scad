// USB BUDDY Ñ v12
// Both USB-A and USB-C open from TOP, side by side in Y direction
// Air gap between them (no PLA bridge)
// Strip along bottom (Z=0), prints flat, used standing upright
//
// Pod Y layout:
//   0..wall           = front outer wall
//   wall..wall+a_w    = USB-A slot (12.0mm)
//   wall+a_w..+wall   = divider wall
//   ..+air_gap        = 1mm air gap (open at top)
//   ..+wall           = divider wall
//   ..+c_w            = USB-C slot (8.31mm oval)
//   ..+wall           = rear outer wall
//
// Pod X: a_h + wall*2 = 9.5mm (along strip)
// Pod Z: slot depth + floor = 14.0 + 1.6 = 15.6mm

num_slots   = 10;
wall        = 2.0;
strip_t     = 0.9;
pod_gap     = 1.2;   // gap between pods along strip
depth       = 0.7;   // label emboss depth

a_w         = 12.0;
a_h         = 5.5;   // USB-A height (X axis)
a_depth     = 14.0;  // how deep slot goes down (Z)
a_floor     = 1.6;

c_w         = 8.31;
c_h         = 3.2;   // USB-C oval height (X axis)
c_depth     = 12.0;
c_floor     = 1.6;
air_gap     = 1.0;

// Pod dimensions
pod_x       = a_h + wall * 2;   // 9.5mm Ñ sized to USB-A height
pod_z       = a_floor + a_depth + 2.0;  // floor + slot + 2mm grip cap = 17.6mm

// Y positions
y_a_start   = wall;                      // USB-A slot start
y_a_end     = wall + a_w;               // USB-A slot end = wall + 12.0
y_gap_start = y_a_end + wall;           // air gap start
y_gap_end   = y_gap_start + air_gap;    // air gap end
y_c_start   = y_gap_end + wall;         // USB-C slot start
y_c_end     = y_c_start + c_w;         // USB-C slot end
pod_y       = y_c_end + wall;           // total pod depth = 30.31mm

pitch       = pod_x + pod_gap;
strip_len   = num_slots * pod_x + (num_slots - 1) * pod_gap;

front_letters = ["", "U", "S", "B", "B", "U", "D", "D", "Y", ""];
rear_letters  = ["y", "u", "r", "y", "g", "", "2", "0", "2", "6"];

// USB-C oval Ñ hull of two circles, opens from top downward
// Centered in X (pod_x/2), Y from y_c_start to y_c_end
module c_oval(h) {
    r   = c_h / 2;
    sep = c_w - c_h;
    cx  = pod_x / 2;
    cy  = y_c_start + c_w/2 - sep/2;
    translate([cx, cy, 0])
        hull() {
            cylinder(h=h, r=r, $fn=32);
            translate([0, sep, 0]) cylinder(h=h, r=r, $fn=32);
        }
}

module cut_front(txt,sz,cx,cz) {
    translate([cx, depth-0.01, cz]) rotate([90,0,0]) linear_extrude(depth+0.01)
        text(txt,size=sz,halign="center",valign="center",font="Liberation Sans:style=Bold");
}

module cut_rear(txt,sz,cx,cz) {
    translate([cx, pod_y-depth+0.01, cz]) rotate([-90,0,0]) linear_extrude(depth+0.01)
        text(txt,size=sz,halign="center",valign="center",font="Liberation Sans:style=Bold");
}

module cut_rear_bt(cx,cz) {
    s=4.5; t=0.8; tx=10.0; ox=-tx/2;
    translate([cx, pod_y-depth+0.01, cz]) rotate([-90,0,0]) linear_extrude(depth+0.01) {
        translate([ox-t/2,-s]) square([t,s*2]);
        hull(){translate([ox-t/2,-s]) square([t,t]); translate([ox+tx-t/2,-s/2-t/2]) square([t,t]);}
        hull(){translate([ox+tx-t/2,-s/2-t/2]) square([t,t]); translate([ox-t/2,-t/2]) square([t,t]);}
        hull(){translate([ox-t/2,-t/2]) square([t,t]); translate([ox+tx-t/2,s/2-t/2]) square([t,t]);}
        hull(){translate([ox+tx-t/2,s/2-t/2]) square([t,t]); translate([ox-t/2,s-t]) square([t,t]);}
    }
}

difference() {
    union() {
        cube([strip_len, pod_y, strip_t]);
        for (i=[0:num_slots-1])
            translate([i*pitch, 0, strip_t]) cube([pod_x, pod_y, pod_z]);
    }

    // Gaps between pods (above strip)
    for (i=[0:num_slots-2])
        translate([i*pitch+pod_x, 0, strip_t-0.01])
            cube([pod_gap, pod_y, pod_z+0.02]);

    for (i=[0:num_slots-1]) {
        fl=front_letters[i]; rl=rear_letters[i];
        ox = i*pitch;

        translate([ox, 0, strip_t]) {
            // USB-A slot Ñ opens from top, cuts down a_depth from top
            translate([wall, y_a_start, pod_z-a_depth])
                cube([a_h, a_w, a_depth+0.1]);

            // Air gap Ñ full width X, 1mm in Y, full depth from top to floor
            translate([wall, y_gap_start, c_floor])
                cube([pod_x-wall*2, air_gap, pod_z]);

            // USB-C oval Ñ opens from top, cuts down c_depth from top
            translate([0, 0, pod_z-c_depth])
                c_oval(c_depth+0.1);

            // Front face labels (Y=0)
            if (fl!="") cut_front(fl, 4.5, pod_x/2, strip_t+pod_z*0.5);
            if (i==0) {
                cut_front("A", 3.0, pod_x/2, strip_t+pod_z*0.75);
                cut_front("C", 3.0, pod_x/2, strip_t+pod_z*0.25);
            }
            if (i==num_slots-1) {
                cut_front("A", 3.0, pod_x/2, strip_t+pod_z*0.75);
                cut_front("C", 3.0, pod_x/2, strip_t+pod_z*0.25);
            }

            // Rear labels
            if (i==5) cut_rear_bt(pod_x/2, strip_t+pod_z*0.5);
            else if (rl!="") cut_rear(rl, 4.5, pod_x/2, strip_t+pod_z*0.5);
        }
    }
}
