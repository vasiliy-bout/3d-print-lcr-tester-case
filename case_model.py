from zencad import *

from api import SimpleZenObj, Size
from config import EPS, EPS2
from device_model import Pcb, Battery, LcdWires, Device, Socket


class CaseProperties(object):
    pcb_margin = 0.4
    battery_margin = 0.5

    size = Size(
        pcb_margin + Pcb.size.x + pcb_margin + 4 + battery_margin + Battery.size.x + battery_margin,
        pcb_margin + Pcb.size.y + LcdWires.size.y + pcb_margin,
        EPS + Battery.size.z + battery_margin
    )
    width = 3.1

    pcb_offset = vector3(
        pcb_margin,
        pcb_margin,
        size.z + width - Pcb.size.z - Socket.size.z
    )

    battery_offset = vector3(
        pcb_margin + Pcb.size.x + pcb_margin + 4 + battery_margin,
        EPS,
        EPS
    )


class CaseTop(SimpleZenObj):
    colour = color.white

    size = Size(CaseProperties.size.x, CaseProperties.size.y, EPS)
    offset = vector3(0.0, 0.0, CaseProperties.size.z - EPS)
    bottom_center = (size.x / 2, size.y / 2, 0.0)

    def __init__(self, device, battery):
        """
        :type device: Device
        :type battery: Battery
        """
        case = thicksolid(
            proto=box(size=self.size),
            t=CaseProperties.width,
            refs=[self.bottom_center]
        )
        case = case.move(self.offset)

        bbox = device.socket.bbox().with_border(EPS)
        bbox_size = bbox.get_size()
        bbox_offset = bbox.get_offset()
        lever_hole = box(size=(
            CaseProperties.width + EPS2,
            Socket.room_size.y + EPS2,
            Socket.room_size.z + EPS2
        )).move(vector3(
            -CaseProperties.width - EPS,
            bbox_offset.y,
            bbox_offset.z + bbox_size.z - Socket.room_size.z - EPS2
        ))
        socket_hole = box(bbox_size).move(bbox_offset)
        case = case - socket_hole - lever_hole

        super().__init__(case)


class CaseBottom(SimpleZenObj):
    colour = color.white

    size = Size(CaseProperties.size.x, CaseProperties.size.y, CaseProperties.size.z - EPS)
    top_center = (size.x / 2, size.y / 2, size.z)

    def __init__(self, device, battery):
        """
        :type device: Device
        :type battery: Battery
        """
        case = thicksolid(
            proto=box(size=self.size),
            t=CaseProperties.width,
            refs=[self.top_center]
        )

        bbox = device.socket.bbox().with_border(EPS)
        bbox_size = bbox.get_size()
        bbox_offset = bbox.get_offset()
        lever_hole = box(size=(
            CaseProperties.width + EPS2,
            Socket.room_size.y + EPS2,
            Socket.room_size.z + EPS2
        )).move(vector3(
            -CaseProperties.width - EPS,
            bbox_offset.y,
            bbox_offset.z + bbox_size.z - Socket.room_size.z - EPS2
        ))
        case = case - lever_hole

        super().__init__(case)
