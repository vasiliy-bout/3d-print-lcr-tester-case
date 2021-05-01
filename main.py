#!/usr/bin/env python3

from zencad import *


def _x(size): return size[0]


def _y(size): return size[1]


def _z(size): return size[2]


# All sizes are in millimeters
eps = 0.2
eps2 = eps * 2

pcb_width = 1.2
pcb_size = (72.5, 60.1, pcb_width)
hole_r = 3.5 / 2.0
hole_offset_x = 1.1
hole_offset_y = 1.5
hole_offset_y2 = 39.0

lcd_offset_left = 6.5
lcd_size = (58.6, 38.5, 6.6 - pcb_width)
lcd_light_points = points([
    (0.0, 0.0, 0.0),
    (0.0, 34.0, 0.0),
    (7.2, 22.0, 0.0),
    (7.2, 12.0, 0.0)
])
lcd_light_h = 3.7 - pcb_width

lcd_wires_size = (9.5, 3.5, 7.0)
lcd_wires_offset = 30.5

socket_size = (33.0, 15.0, 12.7 - pcb_width)

lever_r = 1.0
lever_l = 5.0
lever_offset = 7.7 - lever_r - pcb_width
lever_cap_r = 2.5
lever_cap_l = 7.5

button_size = (14.0, 15.0, 5.0 - pcb_width)
button_cap_r0 = 11.5 / 2.0
button_cap_h0 = 4.0
button_cap_r1 = 13.0 / 2.0
button_cap_h1 = 9.2 - pcb_width
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
    points([
        (67.0, 35.0, 0.0), (67.0, 43.0, 0.0), (73.0, 43.0, 0.0), (73.0, 35.0, 0.0)
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

case_size_x = (pcb_margin + _x(pcb_size) + pcb_margin + 4 +
               battery_margin + _x(battery_size) + battery_margin)
case_size_y = pcb_margin + _y(pcb_size) + _y(lcd_wires_size) + pcb_margin
case_size_z = eps + _z(battery_size) + battery_margin
case_size = (case_size_x, case_size_y, case_size_z)
case_width = 3.1


def create_pcd_model():
    pcb = box(size=pcb_size)
    hole_proto = cylinder(r=hole_r, h=_z(pcb_size) + eps2).moveZ(-eps)
    pcb = pcb - hole_proto.move(hole_r + hole_offset_x,
                                _y(pcb_size) - hole_r - hole_offset_y,
                                0.0)
    pcb = pcb - hole_proto.move(hole_r + hole_offset_x,
                                _y(pcb_size) - hole_r - hole_offset_y2,
                                0.0)
    pcb = pcb - hole_proto.move(_x(pcb_size) - hole_r - hole_offset_x,
                                _y(pcb_size) - hole_r - hole_offset_y,
                                0.0)
    pcb = pcb - hole_proto.move(_x(pcb_size) - hole_r - hole_offset_x,
                                _y(pcb_size) - hole_r - hole_offset_y2,
                                0.0)

    lcd = box(size=lcd_size)
    lcd = lcd.move(
        lcd_offset_left,
        _y(pcb_size) - _y(lcd_size),
        _z(pcb_size)
    )
    lcd_light = extrude(
        proto=polysegment(lcd_light_points, closed=True).fill(),
        vec=lcd_light_h
    )
    lcd_light = lcd_light.move(
        lcd_offset_left + _x(lcd_size),
        _y(pcb_size) - _y(lcd_size),
        _z(pcb_size)
    )
    lcd_wires = box(size=lcd_wires_size)
    lcd_wires = lcd_wires.move(
        lcd_wires_offset,
        _y(pcb_size),
        0.0
    )

    socket = box(size=socket_size)
    socket = socket.moveZ(_z(pcb_size))

    button = box(size=button_size)
    button = button.move(
        _x(pcb_size) - _x(button_size),
        0.0,
        _z(pcb_size)
    )

    cap = unify(
        cylinder(r=button_cap_r0, h=button_cap_h0 + eps).moveZ(button_cap_h1 - eps) +
        cylinder(r=button_cap_r1, h=button_cap_h1)
    )
    cap = cap.move(
        _x(pcb_size) - button_cap_r1 - button_cap_offset_x,
        button_cap_r1 + button_cap_offset_y,
        _z(pcb_size)
    )

    lever = unify(
        cylinder(r=lever_r, h=lever_l + eps) +
        cylinder(r=lever_cap_r, h=lever_cap_l).moveZ(lever_l)
    )
    lever = lever.rotateY(deg(-90))
    lever = lever.move(0.0, lever_r, lever_offset + _z(pcb_size))

    window = box(size=window_size)
    window = window.move(
        window_offset_x,
        window_offset_y,
        _z(pcb_size)
    )

    quartz = box(size=quartz_size).move(vector(quartz_offset))

    smd_areas = []
    for points in smd_points_list:
        area = extrude(
            proto=polysegment(points, closed=True).fill(),
            vec=smd_h * (-1.0)
        )
        smd_areas.append(area)

    power = cylinder(r=power_r, h=power_h)
    power = power.move(
        power_offset_x,
        power_offset_y,
        -power_h
    )

    model = [
        (pcb, color.yellow),
        (lcd, color.green),
        (lcd_light, color.white),
        (lcd_wires, color.mech),
        (socket, color.cian),
        (lever, color.mech),
        (button, color.mech),
        (cap, color.blue),
        (window, color.mech),
        (quartz, color.mech),
        (power, color.red),
    ]
    for area in smd_areas:
        model.append((area, color.mech))
    return model


def create_battery_model():
    battery = box(size=battery_size)
    return [
        (battery, color.mech)
    ]


def create_case_bottom_model():
    refs = [
        (case_size_x / 2, case_size_y / 2, case_size_z)
    ]
    case_proto = box(size=(case_size_x, case_size_y, case_size_z - eps))
    case = thicksolid(proto=case_proto, t=case_width, refs=refs)
    return [
        (case, color.white)
    ]


def create_case_top_model():
    refs = [
        (case_size_x / 2, case_size_y / 2, 0.0)
    ]
    case_proto = box(size=(case_size_x, case_size_y, eps))
    case = thicksolid(proto=case_proto, t=case_width, refs=refs)
    case = case.moveZ(-eps)

    socket_hole_points = points([
        (-case_width, 0.0, 0.0),
        (8.0, pcb_margin - eps, 0.0),
        (pcb_margin + socket_size[0] + eps, pcb_margin - eps, 0.0),
        (pcb_margin + socket_size[0] + eps, pcb_margin + socket_size[1] + eps, 0.0),
        (pcb_margin - eps, pcb_margin + socket_size[1] + eps, 0.0),
        (pcb_margin - eps, 2 * lever_r + eps + pcb_margin, 0.0),
        (-case_width, 2 * lever_r + eps + pcb_margin, 0.0),
    ])
    socket_hole = extrude(
        proto=polysegment(socket_hole_points, closed=True).fill(),
        vec=case_size_z + eps2
    )
    socket_hole = socket_hole.moveZ(-eps)
    case = case - socket_hole

    return [
        (case, color.white)
    ]


def display_model(model, offset_vector=None):
    for obj, c in model:
        if offset_vector:
            obj = obj.move(offset_vector)
        display(obj, color=c)


def main():
    pcb_model = create_pcd_model()
    battery_model = create_battery_model()
    case_bottom_model = create_case_bottom_model()
    case_top_model = create_case_top_model()

    display_model(pcb_model, vector3(pcb_margin,
                                     pcb_margin,
                                     case_size_z + case_width - pcb_width - _z(socket_size)
                                     ))
    display_model(battery_model, vector3(eps + _x(pcb_size) + eps + 4 + eps, eps, eps))
    display_model(case_bottom_model)
    display_model(case_top_model, vector3(0.0, 0.0, case_size_z))

    show(standalone=True)


if __name__ == '__main__':
    main()
