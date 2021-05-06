#!/usr/bin/env python3
from api import CompoundZenObj
from case_model import CaseProperties, CaseBottom, CaseTop, CaseScrews
from device_model import Battery, Device, Pcb
from slices_model import *


# zencad.lazy.fastdo = True


def main():
    device = Device().transformed(move(CaseProperties.pcb_offset))
    battery = Battery().transformed(move(CaseProperties.battery_offset))
    case_bottom = CaseBottom(device, battery)
    case_top = CaseTop(device, battery)
    case_screws = CaseScrews()

    internals = CompoundZenObj(
        device,
        battery,
        case_screws,
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

    trans = SliceShape(device.lcd_lock2, normal_vector=(0, 0, -1))
    # trans = trans * SliceShape(device.lcd_lock1, normal_vector=(0, 1, 0))

    # trans = SlicePoint(Pcb.hole_vector_nw + CaseProperties.pcb_offset)
    # trans = SlicePoint(Pcb.hole_vector_nw + CaseProperties.pcb_offset, normal_vector=(-1, 0, 0))
    # trans = SlicePoint(Pcb.hole_vector_se + CaseProperties.pcb_offset)
    # trans = SlicePoint(Pcb.hole_vector_se + CaseProperties.pcb_offset, normal_vector=(-1, 0, 0))
    # trans = SlicePoint(CaseProperties.screw_black_offset)
    # trans = SlicePoint(CaseProperties.screw_black_offset, normal_vector=(-1, 0, 0))

    # trans = SlicePoint(CaseProperties.screw_black_offset, normal_vector=(0, 0, -1),
    #                    trans=lambda shape: shape.moveZ(-0.05))
    # trans = SlicePoint(vector3(0, 0, 0.01), normal_vector=(0, 0, -1))

    # trans = SlicePoint(vector3(0, 0, device.pcb.bbox().zmax + 0.1), normal_vector=(0, 0, -1))
    # trans = SlicePoint(vector3(0, 0, device.pcb.bbox().zmin - 0.1), normal_vector=(0, 0, 1))

    all_objects.display(trans=trans)

    show(standalone=True)


if __name__ == '__main__':
    main()
