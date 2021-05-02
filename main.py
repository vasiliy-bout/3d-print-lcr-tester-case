#!/usr/bin/env python3

from zencad import *

from api import SimpleZenObj, ZenModel
from config import EPS, EPS2
from device_model import (
    Pcb, Lcd, LcdLight, LcdWires, LcdMount, Socket, SocketLever, SocketLevelCap, Button, ButtonCap,
    ButtonMount, ContactPads, Quartz, PowerTerminals, SocketTerminals, LcdLock, SurfaceMount,
    Battery
)

pcb_margin = 0.4
battery_margin = 0.5

case_size_x = (pcb_margin + Pcb.size.x + pcb_margin + 4 +
               battery_margin + Battery.size.x + battery_margin)
case_size_y = pcb_margin + Pcb.size.y + LcdWires.size.y + pcb_margin
case_size_z = EPS + Battery.size.z + battery_margin
case_size = (case_size_x, case_size_y, case_size_z)
case_width = 3.1


def create_pcd_model():
    return ZenModel(
        Pcb(),
        Lcd(),
        LcdLight(),
        LcdWires(),
        LcdMount(),
        LcdLock(),
        Socket(),
        SocketLever(),
        SocketLevelCap(),
        SocketTerminals(),
        Button(),
        ButtonCap(),
        ButtonMount(),
        ContactPads(),
        Quartz(),
        PowerTerminals(),
        SurfaceMount(),
    )


def create_battery_model():
    return ZenModel(
        Battery()
    )


def create_case_bottom_model():
    refs = [
        (case_size_x / 2, case_size_y / 2, case_size_z)
    ]
    case_proto = box(size=(case_size_x, case_size_y, case_size_z - EPS))
    case = thicksolid(proto=case_proto, t=case_width, refs=refs)
    return ZenModel(
        SimpleZenObj(case, color.white)
    )


def create_case_top_model():
    refs = [
        (case_size_x / 2, case_size_y / 2, 0.0)
    ]
    case_proto = box(size=(case_size_x, case_size_y, EPS))
    case = thicksolid(proto=case_proto, t=case_width, refs=refs)
    case = case.moveZ(-EPS)

    socket_hole_points = points([
        (-case_width, 0.0, 0.0),
        (8.0, pcb_margin - EPS, 0.0),
        (pcb_margin + Socket.size.x + EPS, pcb_margin - EPS, 0.0),
        (pcb_margin + Socket.size.x + EPS, pcb_margin + Socket.size.y + EPS, 0.0),
        (pcb_margin - EPS, pcb_margin + Socket.size.y + EPS, 0.0),
        (pcb_margin - EPS, 2 * SocketLever.radius + EPS + pcb_margin, 0.0),
        (-case_width, 2 * SocketLever.radius + EPS + pcb_margin, 0.0),
    ])
    socket_hole = extrude(
        proto=polysegment(socket_hole_points, closed=True).fill(),
        vec=case_size_z + EPS2
    )
    socket_hole = socket_hole.moveZ(-EPS)
    case = case - socket_hole

    return ZenModel(
        SimpleZenObj(case, color.white)
    )


def main():
    pcb_model = create_pcd_model()
    battery_model = create_battery_model()
    case_bottom_model = create_case_bottom_model()
    case_top_model = create_case_top_model()

    pcb_model.display(move(pcb_margin,
                           pcb_margin,
                           case_size_z + case_width - Pcb.size.z - Socket.size.z))
    battery_model.display(move(EPS + Pcb.size.x + EPS + 4 + EPS, EPS, EPS))
    # case_bottom_model.display()
    # case_top_model.display(move(0.0, 0.0, case_size_z))

    show(standalone=True)


if __name__ == '__main__':
    main()
