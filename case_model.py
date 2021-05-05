from zencad import *

from api import SimpleZenObj, Size, BBox
from config import EPS, EPS2
from device_model import Pcb, Battery, LcdWires, Device, Socket, ButtonCap, LcdMount


class CaseProperties(object):
    pcb_margin = 1.0
    battery_margin = 0.5
    socket_margin = 0.3
    button_margin = 0.3
    screen_margin = 1.0

    battery_wall_width = 4
    battery_wall_offset_x = pcb_margin + LcdMount.offset.x + LcdMount.size.x + pcb_margin

    size = Size(
        battery_wall_offset_x + battery_wall_width + battery_margin + Battery.size.x +
        battery_margin,
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
        battery_wall_offset_x + battery_wall_width + battery_margin,
        EPS,
        EPS
    )


class CaseTop(SimpleZenObj):
    colour = color.white

    size = Size(CaseProperties.size.x, CaseProperties.size.y, EPS)
    offset_z = CaseProperties.size.z - size.z
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
        case = case.moveZ(self.offset_z)

        battery_wall = box(size=(
            CaseProperties.battery_wall_width,
            self.size.y + EPS2,
            EPS + EPS
        )).move(vector3(
            CaseProperties.battery_wall_offset_x,
            -EPS,
            self.offset_z
        ))
        case = case + battery_wall

        screen_frame_width = (CaseProperties.size.z -
                              device.lcd_screen.bbox().zmax - CaseProperties.screen_margin)
        screen_frame = box(size=(
            CaseProperties.battery_wall_offset_x - EPS2,
            self.size.y - EPS2,
            screen_frame_width + EPS
        )).move(vector3(
            EPS, EPS, CaseProperties.size.z - screen_frame_width
        ))
        screen_frame_filler = box(size=(
            CaseProperties.battery_wall_offset_x + EPS2,
            self.size.y + EPS2,
            self.size.z + EPS
        )).move(vector3(-EPS, -EPS, self.offset_z))
        case = case + screen_frame_filler + screen_frame

        case = unify(case)

        socket_bbox = device.socket.bbox().with_border(CaseProperties.socket_margin)
        lever_hole = box(size=(
            CaseProperties.width + CaseProperties.pcb_margin + EPS2,
            Socket.room_size.y + CaseProperties.socket_margin * 2,
            Socket.room_size.z + CaseProperties.socket_margin * 2
        )).move(vector3(
            -CaseProperties.width - EPS,
            socket_bbox.offset.y,
            socket_bbox.offset.z + socket_bbox.size.z - Socket.room_size.z -
            CaseProperties.socket_margin
        ))
        socket_hole = box(socket_bbox.size).move(socket_bbox.offset)
        case = case - socket_hole - lever_hole

        cap_bbox = device.button_cap.bbox()  # type: BBox
        cap_hole = cylinder(
            r=ButtonCap.radius + CaseProperties.button_margin,
            h=ButtonCap.height
        ).move(vector3(
            cap_bbox.center_offset.x,
            cap_bbox.center_offset.y,
            cap_bbox.zmax - ButtonCap.height
        ))
        case = case - cap_hole

        screen_bbox = device.lcd_screen.bbox()  # type: BBox
        screen_hole = box(size=(
            screen_bbox.size.x - EPS2,
            screen_bbox.size.y - EPS2,
            CaseProperties.size.z + CaseProperties.width - screen_bbox.zmax + EPS
        )).move(vector3(
            screen_bbox.xmin + EPS,
            screen_bbox.ymin + EPS,
            screen_bbox.zmax
        ))
        case = case - screen_hole

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

        battery_wall = box(size=(
            CaseProperties.battery_wall_width,
            self.size.y + EPS2,
            self.size.z + EPS
        )).move(vector3(
            CaseProperties.battery_wall_offset_x, -EPS, -EPS
        ))
        case = unify(case + battery_wall)

        socket_bbox = device.socket.bbox().with_border(CaseProperties.socket_margin)
        lever_hole = box(size=(
            CaseProperties.width + EPS2,
            Socket.room_size.y + CaseProperties.socket_margin * 2,
            Socket.room_size.z + CaseProperties.socket_margin * 2
        )).move(vector3(
            -CaseProperties.width - EPS,
            socket_bbox.offset.y,
            socket_bbox.offset.z + socket_bbox.size.z - Socket.room_size.z -
            CaseProperties.socket_margin
        ))
        case = case - lever_hole

        super().__init__(case)
