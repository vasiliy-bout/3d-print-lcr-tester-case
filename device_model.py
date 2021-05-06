from zencad import *

from api import Size, SimpleZenObj, CompoundZenObj
from config import EPS, EPS2, LEVER_ANGLE

# Fix the incorrectly named color
color.cyan = color.cian


class Pcb(SimpleZenObj):
    colour = color.yellow

    size = Size(72.5, 60.1, 1.3)

    hole_r = 3.5 / 2.0
    hole_vectors = vectors([
        (hole_r + 1.1, size.y - hole_r - 1.5, 0.0),
        (hole_r + 1.1, size.y - hole_r - 39.0, 0.0),
        (size.x - hole_r - 1.1, size.y - hole_r - 1.5, 0.0),
        (size.x - hole_r - 1.1, size.y - hole_r - 39.0, 0.0),
    ])

    def __init__(self):
        pcb = box(size=self.size)

        hole_proto = cylinder(r=self.hole_r, h=self.size.z + EPS2).moveZ(-EPS)
        for v in self.hole_vectors:
            pcb = pcb - hole_proto.move(v)

        super().__init__(pcb)


class Lcd(SimpleZenObj):
    colour = color(0.0, 0.4, 0.0)

    size = Size(58.6, 38.5, 6.6 - Pcb.size.z)
    offset = vector3(
        6.5,
        Pcb.size.y - size.y,
        Pcb.size.z
    )

    def __init__(self):
        lcd = box(size=self.size).move(self.offset)
        super().__init__(lcd)


class LcdScreen(SimpleZenObj):
    colour = color.green

    size = Size(54.0, 30.0, 0.4)
    offset = vector3(
        Lcd.offset.x + (Lcd.size.x - size.x) / 2.0,
        Lcd.offset.y + 1.0,
        Lcd.offset.z + Lcd.size.z
    )

    def __init__(self):
        lcd = box(size=self.size).move(self.offset)
        super().__init__(lcd)


class LcdLight(SimpleZenObj):
    colour = color.white

    points = points([
        (0.0, 0.0, 0.0),
        (0.0, 34.0, 0.0),
        (7.2, 22.0, 0.0),
        (7.2, 12.0, 0.0)
    ])
    width = 3.7 - Pcb.size.z
    offset = vector3(
        Lcd.offset.x + Lcd.size.x,
        Pcb.size.y - Lcd.size.y,
        Pcb.size.z
    )

    def __init__(self):
        light = extrude(
            proto=polysegment(self.points, closed=True).fill(),
            vec=self.width
        )
        light = light.move(self.offset)
        super().__init__(light)


class LcdWires(SimpleZenObj):
    colour = color.mech

    size = Size(9.5, 3.5, 7.0)
    offset = vector3(30.5, Pcb.size.y, 0.0)

    def __init__(self):
        wires = box(size=self.size).move(self.offset)
        super().__init__(wires)


class LcdMount(SimpleZenObj):
    colour = color.mech

    size = Size(6.0, 8.0, 4.5)
    offset = vector3(67.0, 35.0, -2.0)

    def __init__(self):
        mount = box(size=self.size).move(self.offset)
        super().__init__(mount)


class LcdLock1(SimpleZenObj):
    colour = color.mech

    radius = 2.5
    height = 3.0
    offset = vector3(
        63.0 + radius,
        24.0 + radius,
        -height
    )

    def __init__(self):
        lock = cylinder(r=self.radius, h=self.height).move(self.offset)
        super().__init__(lock)


class LcdLock2(SimpleZenObj):
    colour = color.mech

    radius = 3.0
    height = 1.0
    offset = vector3(8.0, 51.0, -height)

    def __init__(self):
        lock = cylinder(r=self.radius, h=self.height).move(self.offset)
        super().__init__(lock)


class Socket(SimpleZenObj):
    colour = color.cyan

    size = Size(33.0, 15.0, 12.7 - Pcb.size.z)
    offset = vector3(0.0, 0.0, Pcb.size.z)

    room_size = Size(5.7, 2.0, 6.3)

    def __init__(self):
        socket = box(size=self.size)
        room = box(size=self.room_size).moveZ(self.size.z - self.room_size.z)
        socket = socket - room
        socket = socket.move(self.offset)
        super().__init__(socket)


class SocketLever(SimpleZenObj):
    colour = color.mech

    radius = 1.7 / 2.0
    length = 11.0 - radius
    offset = vector3(
        Socket.room_size.x - radius,
        radius + 0.1,
        Pcb.size.z + Socket.size.z - Socket.room_size.z + radius
    )

    angle = deg(LEVER_ANGLE - 90)

    def __init__(self):
        lever = cylinder(r=self.radius, h=self.length)
        lever = lever.rotateY(self.angle)
        lever = lever.move(self.offset)
        super().__init__(lever)


class SocketLevelCap(SimpleZenObj):
    colour = color.cyan

    radius = 2.5
    length = 7.5

    def __init__(self):
        cap = cylinder(r=self.radius, h=self.length).moveZ(SocketLever.length)
        cap = cap.rotateY(SocketLever.angle)
        cap = cap.move(SocketLever.offset)
        super().__init__(cap)


class SocketTerminals(SimpleZenObj):
    colour = color.mech

    size = Size(17.5, 11.0, 2.5)
    offset = vector3(9.0, 2.0, -size.z)

    def __init__(self):
        terminals = box(self.size).move(self.offset)
        super().__init__(terminals)


class Button(SimpleZenObj):
    colour = color(0.2, 0.2, 0.2)

    size = Size(12.0, 12.0, 4.6 - Pcb.size.z)
    offset = vector3(
        Pcb.size.x - size.x - 1.1,
        1.8,
        Pcb.size.z
    )

    def __init__(self):
        button = box(size=self.size).move(self.offset)
        super().__init__(button)


class ButtonCap(SimpleZenObj):
    colour = color.blue

    radius = 11.5 / 2.0
    height = 4.0

    trim_radius = 13.0 / 2.0
    trim_height = 1.7

    leg_radius = 4.0
    leg_height = 9.1 - Button.size.z - Pcb.size.z - trim_height

    offset = vector3(
        Pcb.size.x - 7.1,
        7.8,
        Pcb.size.z + Button.size.z
    )

    def __init__(self):
        cap = unify(
            cylinder(r=self.radius, h=self.height).moveZ(self.trim_height + self.leg_height) +
            cylinder(r=self.trim_radius, h=self.trim_height).moveZ(self.leg_height) +
            cylinder(r=self.leg_radius, h=self.leg_height)
        )
        cap = cap.move(self.offset)
        super().__init__(cap)


class ButtonMount(SimpleZenObj):
    colour = color.mech

    size = Size(9.0, 15.5, 2.5)
    offset = vector3(Pcb.size.x - 11.5, 0.0, -size.z)

    def __init__(self):
        mount = box(self.size).move(self.offset)
        super().__init__(mount)


class ContactPads(SimpleZenObj):
    colour = color.mech

    size = Size(8.0, 15.5, 0.1)
    offset = vector3(41.3, 1.6, Pcb.size.z)

    def __init__(self):
        pads = box(self.size).move(self.offset)
        super().__init__(pads)


class Quartz(SimpleZenObj):
    colour = color.mech

    size = Size(4.0, 10.0, 4.0)
    offset = vector3(48.0, 28.3, -size.z)

    def __init__(self):
        quartz = box(size=self.size).move(self.offset)
        super().__init__(quartz)


class PowerTerminals(SimpleZenObj):
    colour = color.mech

    size = Size(5.0, 9.0, 1.5)
    offset = vector3(0.5, 26.5, -size.z)

    wires_radius = 3.5 / 2.0
    wires_height = 3.5
    wires_offset = vector3(
        offset.x + size.x / 2.0,
        offset.y + wires_radius,
        -wires_height
    )

    def __init__(self):
        terminals = (
                box(self.size).move(self.offset) +
                cylinder(r=self.wires_radius, h=self.wires_height).move(self.wires_offset)
        )
        super().__init__(terminals)


class SurfaceMount(SimpleZenObj):
    colour = color.mech

    points = points([
        (9.5, 19.0, 0.0), (9.5, 38.0, 0.0), (22.0, 38.0, 0.0),
        (27.0, 51.0, 0.0), (43.0, 51.0, 0.0), (55.0, 42.0, 0.0),
        (55.0, 25.0, 0.0), (46.0, 19.0, 0.0)
    ])
    width = 3

    def __init__(self):
        mount = extrude(
            proto=polysegment(self.points, closed=True).fill(),
            vec=self.width
        )
        mount = mount.moveZ(-self.width)
        super().__init__(mount)


class Battery(SimpleZenObj):
    colour = color.mech

    size = Size(26.0, 51.0, 22.0)

    def __init__(self):
        battery = box(self.size)
        super().__init__(battery)


class Device(CompoundZenObj):
    def __init__(self):
        super().__init__(
            pcb=Pcb(),
            lcd=Lcd(),
            lcd_screen=LcdScreen(),
            lcd_light=LcdLight(),
            lcd_wires=LcdWires(),
            lcd_mount=LcdMount(),
            lcd_lock1=LcdLock1(),
            lcd_lock2=LcdLock2(),
            socket=Socket(),
            socket_lever=SocketLever(),
            socket_lever_cap=SocketLevelCap(),
            socket_terminals=SocketTerminals(),
            button=Button(),
            button_cap=ButtonCap(),
            button_mount=ButtonMount(),
            contact_pads=ContactPads(),
            quarts=Quartz(),
            power_terminals=PowerTerminals(),
            surface_mount=SurfaceMount()
        )
