// USB Buddy cross-section Ñ long axis slice at Y=pod_y/2
difference() {
    import("/Users/mininarwhal/Documents/usb-buddy/usb_buddy.stl", convexity=10);
    translate([-5, -1, -5])
        cube([500, 9.0, 100]);
}
