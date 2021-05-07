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
    all_objects.display()
    show(standalone=True)


def create_model():
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
        top=case_top,
        bottom=case_bottom,
    )

    all_objects = CompoundZenObj(
        internals,
        case=case,
    )

    return all_objects


if __name__ == '__main__':
    main()
