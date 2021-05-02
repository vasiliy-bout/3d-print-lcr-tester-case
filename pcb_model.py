from zencad import *

from api import Size, SimpleZenObj
from config import EPS, EPS2


class Pcb(SimpleZenObj):
    colour = color.yellow

    width = 1.2
    size = Size(72.5, 60.1, width)

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
    colour = color.green

    size = Size(58.6, 38.5, 6.6 - Pcb.width)
    offset = vector3(
        6.5,
        Pcb.size.y - size.y,
        Pcb.size.z
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
    width = 3.7 - Pcb.width
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

    points = points([
        (0.0, 0.0, 0.0), (0.0, 8.0, 0.0), (6.0, 8.0, 0.0), (6.0, 0.0, 0.0)
    ])
    width = 4.5
    offset = vector3(67.0, 35.0, -2.0)

    def __init__(self):
        mount = extrude(
            proto=polysegment(self.points, closed=True).fill(),
            vec=self.width
        )
        mount = mount.move(self.offset)
        super().__init__(mount)
