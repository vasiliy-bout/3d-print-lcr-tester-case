#!/usr/bin/env python3
from api import CompoundZenObj
from case_model import CaseProperties, CaseBottom, CaseTop
from device_model import Battery, Device
from slices_model import *


def main():
    device = Device().transformed(move(CaseProperties.pcb_offset))
    battery = Battery().transformed(move(CaseProperties.battery_offset))
    case_bottom = CaseBottom(device, battery)
    case_top = CaseTop(device, battery)

    all_objects = CompoundZenObj(
        device,
        battery,
        case_top,
        case_bottom,
    )

    # trans = None
    # trans = SliceShape(device.button_cap)
    # trans = SliceShape(device.lcd_screen)
    trans = SliceShape(device.lcd_screen, normal_vector=(-1, 0, 0))

    all_objects.display(trans=trans)

    show(standalone=True)


if __name__ == '__main__':
    main()
