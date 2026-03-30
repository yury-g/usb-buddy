// USB BUDDY Ñ v10f
// USB-C oval punches through floor + strip (exits bottom face = manifold)
// USB slots are the only airflow, no separate vents

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

// C slot exits bottom: from Z=-0.1 world through c_floor+strip_t+c_h+c_cap
c_slot_total = strip_t + c_floor + c_h + c_cap + 0.2;
a_slot_z    = c_floor + c_h + c_cap + a_floor;

pitch       = pod_x + gap;
strip_len   = num_slots * pod_x + (num_slots - 1) * gap;

front_letters = ["", "U", "S", "B", "B", "U", "D", "D", "Y", ""];
rear_letters  = ["y", "u", "r", "y", "g", "", "2", "0", "2", "6"];

module oval_thru(sw, cx, cy, h) {
    r=c_h/2; sep=sw-c_h;
    translate([cx,cy-sep/2,0]) hull(){
        cylinder(h=h,r=r,$fn=32);
        translate([0,sep,0]) cylinder(h=h,r=r,$fn=32);
    }
}

module cut_front(txt,sz,cx,cz) {
    translate([cx,depth-0.01,cz]) rotate([90,0,0]) linear_extrude(depth+0.01)
        text(txt,size=sz,halign="center",valign="center",font="Liberation Sans:style=Bold");
}

module cut_rear(txt,sz,cx,cz) {
    translate([cx,pod_y-depth+0.01,cz]) rotate([-90,0,0]) linear_extrude(depth+0.01)
        text(txt,size=sz,halign="center",valign="center",font="Liberation Sans:style=Bold");
}

module cut_rear_bt(cx,cz) {
    s=4.5; t=0.8; tx=10.0; ox=-tx/2;
    translate([cx,pod_y-depth+0.01,cz]) rotate([-90,0,0]) linear_extrude(depth+0.01) {
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
            translate([i*pitch,0,strip_t]) cube([pod_x,pod_y,pod_z]);
    }

    // Gaps above strip only
    for (i=[0:num_slots-2])
        translate([i*pitch+pod_x,0,strip_t-0.01])
            cube([gap,pod_y,pod_z+0.02]);

    for (i=[0:num_slots-1]) {
        fl=front_letters[i]; rl=rear_letters[i];

        // USB-C oval Ñ punches from Z=-0.1 all the way through floor+strip
        translate([i*pitch,0,-0.1])
            oval_thru(c_w, pod_x/2, pod_y/2, c_slot_total);

        translate([i*pitch,0,strip_t]) {
            // USB-A rect
            translate([wall,wall,a_slot_z]) cube([a_h,a_w,a_h+a_cap+0.1]);
            // Front
            if (fl!="") cut_front(fl,4.5,pod_x/2,pod_z*0.5);
            if (i==0){ cut_front("C",3.2,pod_x/2,pod_z*0.65); cut_front("v",2.8,pod_x/2,pod_z*0.22); }
            if (i==num_slots-1){ cut_front("A",3.2,pod_x/2,pod_z*0.78); cut_front("^",2.8,pod_x/2,pod_z*0.55); }
            // Rear
            if (i==5) cut_rear_bt(pod_x/2,pod_z*0.5);
            else if (rl!="") cut_rear(rl,4.5,pod_x/2,pod_z*0.5);
        }
    }
}
