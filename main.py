#!/usr/bin/env python3
from api import CompoundZenObj
from case_model import CaseProperties, CaseBottom, CaseTop, PcbScrews
from device_model import Battery, Device, Pcb
from slices_model import *


def main():
    device = Device().transformed(move(CaseProperties.pcb_offset))
    battery = Battery().transformed(move(CaseProperties.battery_offset))
    case_bottom = CaseBottom(device, battery)
    case_top = CaseTop(device, battery)
    screws = PcbScrews()

    internals = CompoundZenObj(
        device,
        battery,
        screws,
    )
    case = CompoundZenObj(
        case_top,
        case_bottom,
        # colour=color(1.0, 1.0, 1.0, 0.7)
    )

    all_objects = CompoundZenObj(
        internals,
        case,
    )

    trans = None
    # trans = SliceShape(device.button_cap)
    # trans = SliceShape(device.button_cap, normal_vector=(-1, 0, 0))
    # trans = SliceShape(device.lcd_screen)
    # trans = SliceShape(device.lcd_screen, normal_vector=(-1, 0, 0))
    # trans = SliceShape(device.contact_pads, normal_vector=(-1, 0, 0))

    # trans = trans * SliceShape(device.button_cap, normal_vector=(-1, 1, 0))

    # trans = SliceShape(device.lcd_lock2, normal_vector=(0, 0, -1))
    # trans = trans * SliceShape(device.lcd_lock1, normal_vector=(0, 1, 0))

    trans = SlicePoint(Pcb.hole_vector_nw + CaseProperties.pcb_offset)
    # trans = SlicePoint(Pcb.hole_vector_nw + CaseProperties.pcb_offset, normal_vector=(-1, 0, 0))
    # trans = SlicePoint(Pcb.hole_vector_se + CaseProperties.pcb_offset)
    # trans = SlicePoint(Pcb.hole_vector_se + CaseProperties.pcb_offset, normal_vector=(-1, 0, 0))

    all_objects.display(trans=trans)

    show(standalone=True)


if __name__ == '__main__':
    main()
