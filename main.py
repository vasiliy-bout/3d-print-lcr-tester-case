#!/usr/bin/env python3
from api import CompoundZenObj
from case_model import CaseProperties, CaseBottom, CaseTop, CaseScrews
from device_model import Battery, Device
from slices_model import *


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
    )

    all_objects = CompoundZenObj(
        internals,
        case,
    )

    all_objects.display()

    show(standalone=True)


if __name__ == '__main__':
    main()
