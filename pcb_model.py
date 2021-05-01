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
        pcb = box(size=self.size.tuple())

        hole_proto = cylinder(r=self.hole_r, h=self.size.z + EPS2).moveZ(-EPS)
        for v in self.hole_vectors:
            pcb = pcb - hole_proto.move(v)

        super().__init__(pcb)
