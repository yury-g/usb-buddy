// USB BUDDY Ñ v11b
// 1mm internal air gap between USB-C cap and USB-A floor
// Gap is internal cavity Ñ does NOT breach front or rear walls

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
air_gap     = 1.0;

pod_y       = a_w + wall * 2;
pod_x       = a_h + wall * 2;

c_top_z     = c_floor + c_h + c_cap;
a_floor_z   = c_top_z + air_gap;
a_slot_z    = a_floor_z + a_floor;
pod_z       = a_slot_z + a_h + a_cap;

pitch       = pod_x + gap;
strip_len   = num_slots * pod_x + (num_slots - 1) * gap;
c_slot_total = strip_t + c_floor + c_h + c_cap + 0.2;

front_letters = ["", "U", "S", "B", "B", "U", "D", "D", "Y", ""];
rear_letters  = ["y", "u", "r", "y", "g", "", "2", "0", "2", "6"];

module oval_thru(sw,cx,cy,h) {
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

    // Gaps between pods
    for (i=[0:num_slots-2])
        translate([i*pitch+pod_x,0,strip_t-0.01])
            cube([gap,pod_y,pod_z+0.02]);

    for (i=[0:num_slots-1]) {
        fl=front_letters[i]; rl=rear_letters[i];

        // USB-C oval through bottom
        translate([i*pitch,0,-0.1])
            oval_thru(c_w, pod_x/2, pod_y/2, c_slot_total);

        translate([i*pitch,0,strip_t]) {
            // Internal air gap Ñ stays within front+rear walls
            // X: wall to pod_x-wall (inside side walls)
            // Y: wall to pod_y-wall (inside front+rear walls)
            // Z: c_top_z to c_top_z+air_gap
            translate([wall, wall, c_top_z])
                cube([pod_x-wall*2, pod_y-wall*2, air_gap]);

            // USB-A rect slot
            translate([wall,wall,a_slot_z])
                cube([a_h,a_w,a_h+a_cap+0.1]);

            // Front labels Ñ positioned in USB-A zone (upper half)
            if (fl!="") cut_front(fl,4.5,pod_x/2,a_slot_z+a_h*0.5);
            if (i==0){
                cut_front("C",3.2,pod_x/2,c_floor+c_h*0.5);
                cut_front("v",2.0,pod_x/2,c_floor*0.4);
            }
            if (i==num_slots-1){
                cut_front("A",3.2,pod_x/2,a_slot_z+a_h*0.5);
                cut_front("^",2.0,pod_x/2,a_slot_z+a_h+a_cap*0.5);
            }

            // Rear labels
            if (i==5) cut_rear_bt(pod_x/2,pod_z*0.5);
            else if (rl!="") cut_rear(rl,4.5,pod_x/2,pod_z*0.5);
        }
    }
}
