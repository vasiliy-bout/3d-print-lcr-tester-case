from zencad import *

from api import SimpleZenObj, Size, BBox, CompoundZenObj
from config import EPS, EPS2
from device_model import (
    Pcb, Battery, LcdWires, Device, Socket, ButtonCap, LcdMount, LcdLock1, LcdLock2, Screw,
    ScrewBlack
)


class CaseProperties(object):
    default_margin = 1.0

    pcb_margin = 1.8
    battery_margin = 0.4
    socket_margin = 0.36
    button_cap_margin = 0.36
    screen_margin = 1.0
    contact_pads_margin = 2.2
    screw_length_margin = 1.0

    screw_mount_width = 2.0
    case_mount_width = 2.0

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

    screw_black_offset_xy = vector3(
        size.x - case_mount_width - ScrewBlack.radius,
        case_mount_width + ScrewBlack.radius,
        0
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

        controls_frame = box(size=(
            CaseProperties.battery_wall_offset_x - EPS2,
            device.lcd.bbox().ymin - CaseProperties.default_margin - EPS,
            # full contact with PCB, no gaps
            CaseProperties.size.z - device.pcb.bbox().zmax + EPS
        )).move(vector3(
            EPS, EPS, device.pcb.bbox().zmax
        ))
        case = case + controls_frame

        for v in PcbScrews.vectors_dict.values():
            screw_mount_offset = vector3(
                v.x, v.y,
                device.pcb.bbox().zmax
            )
            screw_mount = cylinder(
                r=Screw.radius + CaseProperties.screw_mount_width,
                # full contact with PCB, no gaps
                h=CaseProperties.size.z - device.pcb.bbox().zmax + EPS
            ).move(screw_mount_offset)
            screw_hole = cylinder(
                r=Screw.radius,
                h=Screw.length - Pcb.size.z + CaseProperties.screw_length_margin
            ).move(screw_mount_offset)
            case = case + screw_mount - screw_hole

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
            r=ButtonCap.radius + CaseProperties.button_cap_margin,
            h=ButtonCap.height
        ).move(vector3(
            cap_bbox.center_offset.x,
            cap_bbox.center_offset.y,
            cap_bbox.zmax - ButtonCap.height
        ))
        case = case - cap_hole

        button_hole = box(size=(
            cap_bbox.size.x + CaseProperties.default_margin * 2,
            cap_bbox.size.y + CaseProperties.default_margin * 2,
            CaseProperties.size.z - device.pcb.bbox().zmax
        )).move(vector3(
            cap_bbox.offset.x - CaseProperties.default_margin,
            cap_bbox.offset.y - CaseProperties.default_margin,
            device.pcb.bbox().zmax
        ))
        case = case - button_hole

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

        contact_pads_bbox = device.contact_pads.bbox()  # type: BBox
        contact_pads_bbox = contact_pads_bbox.with_border_x(CaseProperties.contact_pads_margin)
        contact_pads_bbox = contact_pads_bbox.with_border_y(CaseProperties.contact_pads_margin)
        contact_pads_bbox = contact_pads_bbox.with_border_z(EPS)
        contact_pads_hole = box(size=(
            contact_pads_bbox.size.x,
            contact_pads_bbox.ymax + CaseProperties.width + EPS,
            CaseProperties.size.z + CaseProperties.width - contact_pads_bbox.zmin
        )).move(vector3(
            contact_pads_bbox.offset.x,
            -CaseProperties.width - EPS,
            contact_pads_bbox.zmin
        ))
        case = case - contact_pads_hole

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
        case = case + battery_wall

        pcb_bed = box(size=(
            CaseProperties.battery_wall_offset_x + EPS2,
            self.size.y + EPS2,
            device.pcb.bbox().zmin + EPS  # full contact with PCB, no gaps
        )).move(vector3(
            -EPS, -EPS, -EPS
        ))
        case = case + pcb_bed

        case = unify(case)

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

        contact_pads_bbox = device.contact_pads.bbox()  # type: BBox
        contact_pads_bbox = contact_pads_bbox.with_border_x(CaseProperties.contact_pads_margin)
        contact_pads_bbox = contact_pads_bbox.with_border_y(CaseProperties.contact_pads_margin)
        contact_pads_bbox = contact_pads_bbox.with_border_z(EPS)
        contact_pads_hole = box(size=(
            contact_pads_bbox.size.x,
            contact_pads_bbox.ymax + CaseProperties.width + EPS,
            CaseProperties.size.z + CaseProperties.width - contact_pads_bbox.zmin
        )).move(vector3(
            contact_pads_bbox.offset.x,
            -CaseProperties.width - EPS,
            contact_pads_bbox.zmin
        ))
        case = case - contact_pads_hole

        case = case - device.power_terminals.bbox().with_border(1.0).to_zen_box()
        case = case - device.surface_mount.bbox().with_border(1.0).to_zen_box()
        case = case - device.quarts.bbox().with_border(1.0).to_zen_box()
        case = case - device.lcd_mount.bbox().with_border(1.0).to_zen_box()
        case = case - device.socket_terminals.bbox().with_border(1.0).to_zen_box()
        case = case - device.button_mount.bbox().with_border(1.0).to_zen_box()

        lock_bbox = device.lcd_lock1.bbox()  # type: BBox
        case = case - (cylinder(r=LcdLock1.radius + 1.0, h=LcdLock1.height + 2 * 1.0, center=True)
                       .move(lock_bbox.center_offset))
        lock_bbox = device.lcd_lock2.bbox()  # type: BBox
        case = case - (cylinder(r=LcdLock2.radius + 1.0, h=LcdLock2.height + 2 * 1.0, center=True)
                       .move(lock_bbox.center_offset))

        for v in PcbScrews.vectors_dict.values():
            screw_hole_h = Screw.cap_h + CaseProperties.default_margin
            screw_hole = cylinder(
                r=Screw.cap_r + CaseProperties.default_margin,
                h=screw_hole_h
            ).move(v).moveZ(-screw_hole_h)
            case = case - screw_hole

        super().__init__(case)


class PcbScrews(CompoundZenObj):
    vectors_dict = {
        'screw_nw': CaseProperties.pcb_offset + Pcb.hole_vector_nw,
        'screw_se': CaseProperties.pcb_offset + Pcb.hole_vector_se,
    }

    def __init__(self):
        screw_dict = {
            k: Screw().transformed(move(v))
            for k, v in self.vectors_dict.items()
        }
        super().__init__(**screw_dict)


class CaseScrews(CompoundZenObj):
    vectors_dict = {
        'screw_ne': (CaseProperties.pcb_offset + vector3(0, 0, -CaseProperties.case_mount_width) +
                     Pcb.hole_vector_ne),
        'screw_sw': (CaseProperties.pcb_offset + vector3(0, 0, -CaseProperties.case_mount_width) +
                     Pcb.hole_vector_sw),
        'screw_black': (CaseProperties.pcb_offset +
                        vector3(0, 0, -CaseProperties.case_mount_width) +
                        CaseProperties.screw_black_offset_xy)
    }

    def __init__(self):
        screw_dict = {
            k: Screw().transformed(move(v))
            for k, v in self.vectors_dict.items()
        }
        super().__init__(**screw_dict)
