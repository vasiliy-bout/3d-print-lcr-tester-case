#!/usr/bin/env python3

from zencad import *

from case_model import CaseProperties, CaseBottom, CaseTop
from device_model import Battery, Device


def main():
    device = Device().transformed(move(CaseProperties.pcb_offset))
    battery = Battery().transformed(move(CaseProperties.battery_offset))

    case_bottom = CaseBottom(device, battery)
    case_top = CaseTop(device, battery)

    device.display()
    battery.display()
    case_bottom.display()
    case_top.display()

    show(standalone=True)


if __name__ == '__main__':
    main()
