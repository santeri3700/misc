#!/usr/bin/env python3
import usb.core
import usb.util

# Write method. 1 = HID Write (URB_INTERRUPT), 2 = Control Transfer (URB_CONTROL)
write_method = 1

# Vendor ID
dev_vid = 0x1b1c

# Product ID
dev_pid = 0x1b3e

# Interface (for RGB packet data etc)
dev_interface = 2

try:
    # Find the device
    dev = usb.core.find(idVendor=dev_vid, idProduct=dev_pid)
except Exception as e:
    print("Error while finding device: " + str(e))
    exit(1)

if not dev:
    print("USB device not found!")
    exit(1)

try:
    # Detach the currently used kernel driver
    for config in dev:
        for i in range(config.bNumInterfaces):
            if dev.is_kernel_driver_active(interface=i):
                dev.detach_kernel_driver(interface=i)

    # Sometimes you have to explicitly claim an interface. Try it if claiming fails with your device.
    #usb.util.claim_interface(device=dev, interface=dev_interface)

    # Commonly, an interface has only one alternate setting and this call is not necessary. Try it if claiming fails with your device.
    #dev.set_interface_altsetting(interface=dev_interface, alternate_setting=0)

    print("Driver detached and claimed! Mouse will be unusable for a moment.")
except Exception as e:
    print("Error while claiming device: " + str(e))
    exit(1)

# Prepare RGB control packet

# Color white = #FFFFFF (0xff 0xff 0xff)
red = 0xff
grn = 0x00
blu = 0xff

# Data with color variables. Packet based on Corsair Scimitar PRO RGB data.
packet = [
0x07, 0x22, 0x0f, 0x01, 0x03, red, grn, blu, 0x02, red, grn, blu, 0x04, red, grn, blu,
0x01, red, grn, blu, 0x05, red, grn, blu, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
]

try:
    # Send the data to the device (1000ms timeout)

    if write_method == 1:
        # Method 1: HID Write. Use this if your device is controlled with "URB_INTERRUPT" packets.
        dev.write(endpoint=dev_interface, data=packet, timeout=1000)
        print("Sent packet!")
    elif write_method == 2:
        # Method 2: Control Transfer. Use this if your device is controlled with "URB_CONTROL" packets.
        dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0307, wIndex=0x0001, data_or_wLength=packet, timeout=1000)
        print("Sent packet!")
    else:
        print("Invalid write method!")
except Exception as e:
    print("Error while sending packet: " + str(e))
    exit(1)

try:
    # Release the device and load the default driver
    usb.util.release_interface(device=dev, interface=dev_interface)

    for config in dev:
        for i in range(config.bNumInterfaces):
            dev.attach_kernel_driver(interface=i)


    print("Driver reattached! Device should be usable again.")
except usb.USBError as e:
    # Ignore error code 16 (Resource busy)
    if e.backend_error_code == -6:
        pass
    else:        
        print("Error while reattaching driver: " + str(e))
        exit(1)

print("Bye!")