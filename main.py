#!/usr/bin/env python3

from zencad import *

from api import SimpleZenObj, ZenModel
from config import EPS, EPS2
from pcb_model import Pcb, Lcd, LcdLight, LcdWires, LcdMount


def _x(size): return size[0]


def _y(size): return size[1]


def _z(size): return size[2]


socket_size = (33.0, 15.0, 12.7 - Pcb.width)

lever_r = 1.0
lever_l = 5.0
lever_offset = 7.7 - lever_r - Pcb.width
lever_cap_r = 2.5
lever_cap_l = 7.5

button_size = (14.0, 15.0, 5.0 - Pcb.width)
button_cap_r0 = 11.5 / 2.0
button_cap_h0 = 4.0
button_cap_r1 = 13.0 / 2.0
button_cap_h1 = 9.2 - Pcb.width
button_cap_offset_x = 0.5
button_cap_offset_y = 1.0

window_size = (8.5, 15.5, 0.1)
window_offset_x = 41.0
window_offset_y = 1.5

quartz_size = (4.0, 10.0, 4.0)
quartz_offset = (48.0, 28.3, -4)

smd_points_list = [
    points([
        (8.0, 1.0, 0.0), (8.0, 31.5, 0.0), (0.0, 31.5, 0.0),
        (0.0, 36.0, 0.0), (8.0, 38.0, 0.0), (22.0, 38.0, 0.0),
        (27.0, 51.0, 0.0), (43.0, 51.0, 0.0), (55.0, 42.0, 0.0),
        (55.0, 25.0, 0.0), (46.0, 19.0, 0.0), (29.0, 19.0, 0.0),
        (29.0, 1.0, 0.0)
    ]),
    points([
        (61.0, 0.0, 0.0), (61.0, 16.0, 0.0), (71.0, 16.0, 0.0), (71.0, 0.0, 0.0)
    ]),
    points([
        (63.0, 24.0, 0.0), (63.0, 28.0, 0.0), (68.0, 28.0, 0.0), (68.0, 24.0, 0.0)
    ]),
]
smd_h = 3

power_r = 3.5 / 2.0
power_h = 3.5
power_offset_x = 1.5 + power_r
power_offset_y = 27 + power_r

battery_size = (26.0, 51.0, 22.0)

pcb_margin = 0.4
battery_margin = 0.5

case_size_x = (pcb_margin + Pcb.size.x + pcb_margin + 4 +
               battery_margin + _x(battery_size) + battery_margin)
case_size_y = pcb_margin + Pcb.size.y + LcdWires.size.y + pcb_margin
case_size_z = EPS + _z(battery_size) + battery_margin
case_size = (case_size_x, case_size_y, case_size_z)
case_width = 3.1


def create_pcd_model():
    pcb = Pcb()
    lcd = Lcd()
    lcd_light = LcdLight()
    lcd_wires = LcdWires()
    lcd_mount = LcdMount()

    socket = box(size=socket_size)
    socket = socket.moveZ(Pcb.size.z)

    button = box(size=button_size)
    button = button.move(
        Pcb.size.x - _x(button_size),
        0.0,
        Pcb.size.z
    )

    cap = unify(
        cylinder(r=button_cap_r0, h=button_cap_h0 + EPS).moveZ(button_cap_h1 - EPS) +
        cylinder(r=button_cap_r1, h=button_cap_h1)
    )
    cap = cap.move(
        Pcb.size.x - button_cap_r1 - button_cap_offset_x,
        button_cap_r1 + button_cap_offset_y,
        Pcb.size.z
    )

    lever = unify(
        cylinder(r=lever_r, h=lever_l + EPS) +
        cylinder(r=lever_cap_r, h=lever_cap_l).moveZ(lever_l)
    )
    lever = lever.rotateY(deg(-90))
    lever = lever.move(0.0, lever_r, lever_offset + Pcb.size.z)

    window = box(size=window_size)
    window = window.move(
        window_offset_x,
        window_offset_y,
        Pcb.size.z
    )

    quartz = box(size=quartz_size).move(vector(quartz_offset))

    smd_areas = []
    for pts in smd_points_list:
        area = extrude(
            proto=polysegment(pts, closed=True).fill(),
            vec=smd_h * (-1.0)
        )
        smd_areas.append(area)

    power = cylinder(r=power_r, h=power_h)
    power = power.move(
        power_offset_x,
        power_offset_y,
        -power_h
    )

    model = ZenModel(
        pcb,
        lcd,
        lcd_light,
        lcd_wires,
        lcd_mount,
        SimpleZenObj(socket, color.cian),
        SimpleZenObj(lever, color.mech),
        SimpleZenObj(button, color.mech),
        SimpleZenObj(cap, color.blue),
        SimpleZenObj(window, color.mech),
        SimpleZenObj(quartz, color.mech),
        SimpleZenObj(power, color.red),
    )
    for area in smd_areas:
        model.add(SimpleZenObj(area, color.mech))
    return model


def create_battery_model():
    battery = box(size=battery_size)
    return ZenModel(
        SimpleZenObj(battery, color.mech)
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
        (pcb_margin + socket_size[0] + EPS, pcb_margin - EPS, 0.0),
        (pcb_margin + socket_size[0] + EPS, pcb_margin + socket_size[1] + EPS, 0.0),
        (pcb_margin - EPS, pcb_margin + socket_size[1] + EPS, 0.0),
        (pcb_margin - EPS, 2 * lever_r + EPS + pcb_margin, 0.0),
        (-case_width, 2 * lever_r + EPS + pcb_margin, 0.0),
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
                           case_size_z + case_width - Pcb.width - _z(socket_size)))
    battery_model.display(move(EPS + Pcb.size.x + EPS + 4 + EPS, EPS, EPS))
    case_bottom_model.display()
    case_top_model.display(move(0.0, 0.0, case_size_z))

    show(standalone=True)


if __name__ == '__main__':
    main()
