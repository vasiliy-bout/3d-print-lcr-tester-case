#!/usr/bin/env python3
from api import CompoundZenObj
from case_model import CaseProperties, CaseBottom, CaseTop, CaseScrews
from device_model import Battery, Device
from slices_model import *

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--top')
    parser.add_argument('--bottom')
    parser.add_argument('--delta', type=float, default=0.02)
    args = parser.parse_args()

    run(args.top, args.bottom, args.delta)


def run(top_file, bottom_file, delta):
    all_objects = create_model()

    if not (top_file or bottom_file):
        display_model(all_objects)
    else:
        if top_file:
            export("top", all_objects.case.top.shape, top_file, delta)
        if bottom_file:
            export("bottom", all_objects.case.bottom.shape, bottom_file, delta)


def export(name, shape, path, delta):
    print(f'Writing "{name}" model to {path}...')
    to_stl(shape, path, delta)
    print('Ok')


def display_model(all_objects):
    trans = None
    # trans = debug_transformations(all_objects.internals.device)

    all_objects.hide('internals')
    all_objects.case.hide('top')

    all_objects.display(trans=trans)
    show(standalone=True)


def create_model():
    device = Device().transformed(move(CaseProperties.pcb_offset))
    battery = Battery().transformed(move(CaseProperties.battery_offset))
    case_bottom = CaseBottom(device, battery)
    case_top = CaseTop(device, battery)
    screws = CaseScrews()

    internals = CompoundZenObj(
        device=device,
        battery=battery,
        screws=screws,
    )
    case = CompoundZenObj(
        top=case_top,
        bottom=case_bottom,
    )
    all_objects = CompoundZenObj(
        internals=internals,
        case=case,
    )
    return all_objects


def debug_transformations(device):
    if device is None:
        return None

    trans = None

    # trans = SliceShape(device.button_cap)
    # trans = SliceShape(device.button_cap, normal_vector=(-1, 0, 0))
    # trans = SliceShape(device.lcd_screen)
    # trans = SliceShape(device.lcd_screen, normal_vector=(-1, 0, 0))
    # trans = SliceShape(device.contact_pads, normal_vector=(-1, 0, 0))
    # trans = trans * SliceShape(device.button_cap, normal_vector=(-1, 1, 0))
    # trans = SliceShape(device.lcd_lock2, normal_vector=(0, 0, -1))

    trans = SliceShape(device.lcd_wires, normal_vector=(-1, 0, 0))

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

    return trans


if __name__ == '__main__':
    main()
