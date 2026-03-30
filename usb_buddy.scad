// USB BUDDY Ñ v14
// USB-A top, USB-C bottom
// Thin 0.8mm separator between zones (structural only, air gap cut through it laterally)
// No blocking shelf Ñ separator is just the wall thickness needed for manifold geometry

num_slots   = 10;
wall        = 2.0;
strip_t     = 0.9;
gap         = 1.2;
depth       = 0.7;

a_w         = 12.0;
a_h         = 5.5;
a_cap       = 2.0;

c_w         = 8.31;
c_h         = 3.2;
c_cap       = 2.0;
c_floor     = 1.6;
sep         = 0.8;   // thin separator between C cap and A slot Ñ structural only

pod_y       = a_w + wall * 2;
pod_x       = a_h + wall * 2;

// Z stack:
// 0..c_floor       = C base floor
// c_floor..+c_h    = C oval slot
// +c_h..+c_cap     = C cap (grip)
// +c_cap..+sep     = thin separator (0.8mm)
// +sep..+a_h       = A slot
// +a_h..+a_cap     = A cap (grip)
c_top_z     = c_floor + c_h + c_cap;
a_slot_z    = c_top_z + sep;
pod_z       = a_slot_z + a_h + a_cap;

// C oval punches from bottom through c_floor+c_h+c_cap only (stops at separator)
c_slot_h    = strip_t + c_floor + c_h + c_cap + 0.1;

// Air gap: cut through separator laterally (front+rear faces open)
// This opens the 0.8mm sep layer to airflow without making it a full floor
air_slot_h  = sep + 0.1;

pitch       = pod_x + gap;
strip_len   = num_slots * pod_x + (num_slots - 1) * gap;

front_letters = ["", "U", "S", "B", "B", "U", "D", "D", "Y", ""];
rear_letters  = ["y", "u", "r", "y", "g", "", "2", "0", "2", "6"];

module oval_thru(sw, cx, cy, h) {
    r=c_h/2; s=sw-c_h;
    translate([cx,cy-s/2,0]) hull(){
        cylinder(h=h,r=r,$fn=32);
        translate([0,s,0]) cylinder(h=h,r=r,$fn=32);
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

        // USB-C oval Ñ up from bottom through C zone, stops at separator
        translate([i*pitch,0,-0.1])
            oval_thru(c_w, pod_x/2, pod_y/2, c_slot_h);

        translate([i*pitch,0,strip_t]) {
            // Air slot through separator Ñ open front to rear
            // Cut full interior width, front face to rear face
            translate([wall, wall, c_top_z])
                cube([pod_x-wall*2, pod_y-wall*2, air_slot_h]);

            // USB-A rect slot from top down
            translate([wall, wall, a_slot_z])
                cube([a_h, a_w, a_h+a_cap+0.1]);

            // Front labels
            if (fl!="") cut_front(fl,4.5,pod_x/2,a_slot_z+a_h*0.45);
            if (i==0){
                cut_front("C",3.2,pod_x/2,c_floor+c_h*0.5);
                cut_front("v",2.0,pod_x/2,c_floor*0.45);
            }
            if (i==num_slots-1){
                cut_front("A",3.2,pod_x/2,a_slot_z+a_h*0.5);
                cut_front("^",2.0,pod_x/2,a_slot_z+a_h+a_cap*0.5);
            }

            // Rear labels
            if (rl!="") cut_rear(rl,4.5,pod_x/2,pod_z*0.5);
        }
    }
}
