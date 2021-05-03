#!/usr/bin/env python3

from zencad import *

from api import SimpleZenObj
from config import EPS, EPS2
from device_model import Pcb, LcdWires, Socket, Battery, Device

pcb_margin = 0.4
battery_margin = 0.5

case_size_x = (pcb_margin + Pcb.size.x + pcb_margin + 4 +
               battery_margin + Battery.size.x + battery_margin)
case_size_y = pcb_margin + Pcb.size.y + LcdWires.size.y + pcb_margin
case_size_z = EPS + Battery.size.z + battery_margin
case_size = (case_size_x, case_size_y, case_size_z)
case_width = 3.1


def create_case_bottom(device, battery):
    refs = [
        (case_size_x / 2, case_size_y / 2, case_size_z)
    ]
    case_proto = box(size=(case_size_x, case_size_y, case_size_z - EPS))
    case = thicksolid(proto=case_proto, t=case_width, refs=refs)

    bbox = device.socket.bbox().add_border(EPS)
    bbox_size = bbox.get_size()
    bbox_offset = bbox.get_offset()
    lever_hole = box(size=(
        case_width + EPS2,
        Socket.room_size.y + EPS2,
        Socket.room_size.z + EPS2
    )).move(vector3(
        -case_width - EPS,
        bbox_offset.y,
        bbox_offset.z + bbox_size.z - Socket.room_size.z - EPS2
    ))
    case = case - lever_hole

    return SimpleZenObj(case, color.white)


def create_case_top(device, battery):
    refs = [
        (case_size_x / 2, case_size_y / 2, 0.0)
    ]
    case_proto = box(size=(case_size_x, case_size_y, EPS))
    case = thicksolid(proto=case_proto, t=case_width, refs=refs)
    case = case.moveZ(case_size_z - EPS)

    bbox = device.socket.bbox().add_border(EPS)
    bbox_size = bbox.get_size()
    bbox_offset = bbox.get_offset()
    socket_hole = box(bbox_size).move(bbox_offset)
    lever_hole = box(size=(
        case_width + EPS2,
        Socket.room_size.y + EPS2,
        Socket.room_size.z + EPS2
    )).move(vector3(
        -case_width - EPS,
        bbox_offset.y,
        bbox_offset.z + bbox_size.z - Socket.room_size.z - EPS2
    ))
    case = case - socket_hole - lever_hole

    return SimpleZenObj(case, color.white)


def main():
    device = Device()
    battery = Battery()

    device = device.transformed(
        move(pcb_margin, pcb_margin, case_size_z + case_width - Pcb.size.z - Socket.size.z)
    )
    battery = battery.transformed(
        move(EPS + Pcb.size.x + EPS + 4 + EPS, EPS, EPS)
    )

    case_bottom = create_case_bottom(device, battery)
    case_top = create_case_top(device, battery)

    device.display()
    battery.display()
    case_bottom.display()
    case_top.display()

    show(standalone=True)


if __name__ == '__main__':
    main()
