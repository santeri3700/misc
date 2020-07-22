#!/usr/bin/env python2
import usb.core
import usb.util

input_r = int(input("R: "))
input_g = int(input("G: "))
input_b = int(input("B: "))

error = True
if 0 <= input_r <= 255:
    if 0 <= input_g <= 255:
        if 0 <= input_b <= 255:
            color_r = input_r
            color_g = input_g
            color_b = input_b
            error = False

if error == True:
    print("Invalid rgb value(s)!")
    exit(1)

# Find the device
# Holtek Semiconductor, Inc. USB Gaming Mouse -- ID 04d9:a070 Holtek Semiconductor, Inc.
dev = usb.core.find(idVendor=0x04d9, idProduct=0xa070)

# Detach the currently used kernel driver (hid_holtek_mouse)
dev.detach_kernel_driver(1)
usb.util.claim_interface(dev,1)
dev.set_interface_altsetting(interface=1,alternate_setting=0)

colors = [int(color_r), int(color_g), int(color_b)]

print(colors)

# Prepare data
#  SET  RGB  ???  RED  GRN  BLU   ??   ??
# 0x07 0x0a 0x00 0xFF 0xFF 0xFF 0x00 0x00
data = [0x07, 0x0a, 0x00] + colors + [0x00, 0x00]

#print(data)

# Send the data to the mouse
dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0307, wIndex=0x0001, data_or_wLength=data,timeout=1000)

# Release the device and load the default driver
usb.util.release_interface(dev,1)
dev.attach_kernel_driver(1)
