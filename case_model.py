from math import cos

from zencad import *

from api import SimpleZenObj, Size, BBox, CompoundZenObj
from config import EPS, EPS2
from device_model import (
    Pcb, Battery, LcdWires, Device, Socket, ButtonCap, LcdMount, LcdLock1, LcdLock2, ScrewBase,
    ScrewSilver, ScrewBlack, PowerTerminals
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
    screw_radius_margin = 0.2
    screw_cap_margin = 0.5

    smd_margin = 3.0

    screw_mount_width = 2.0
    case_mount_width = 1.5
    case_mount_height = 2.0

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

    screw_black_mount_rounding_width = 1.0
    screw_black_mount_width = (ScrewBlack.cap_r * 2 + screw_cap_margin * 4 + case_mount_width +
                               screw_black_mount_rounding_width * 2)
    screw_black_offset = vector3(
        size.x - screw_cap_margin * 2 - ScrewBlack.cap_r - screw_black_mount_rounding_width,
        screw_cap_margin * 2 + ScrewBlack.cap_r + screw_black_mount_rounding_width,
        pcb_offset.z + Pcb.size.z - case_mount_height
    )

    battery_offset = vector3(
        battery_wall_offset_x + battery_wall_width + battery_margin,
        screw_black_mount_width + EPS,
        EPS
    )
    battery_frame_height = 1.5
    battery_frame_width = 1.5


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

        battery_frame = box(size=(
            CaseProperties.size.x - CaseProperties.battery_wall_offset_x -
            CaseProperties.battery_wall_width - EPS2,
            CaseProperties.size.y - EPS2,
            CaseProperties.battery_frame_height + EPS
        )) - box(size=(
            CaseProperties.size.x - CaseProperties.battery_wall_offset_x -
            CaseProperties.battery_wall_width,
            CaseProperties.size.y - EPS2 - CaseProperties.battery_frame_width * 2,
            CaseProperties.battery_frame_height + EPS2
        )).move(vector3(-EPS, CaseProperties.battery_frame_width, -EPS))

        battery_frame = battery_frame.move(vector3(
            CaseProperties.battery_wall_offset_x + CaseProperties.battery_wall_width + EPS,
            EPS,
            CaseProperties.size.z - CaseProperties.battery_frame_height
        ))
        case = case + battery_frame

        for info in CaseScrews.screw_info_dict.values():
            screw_mount_offset = vector3(
                info.screw_offset.x, info.screw_offset.y,
                device.pcb.bbox().zmax
            )
            screw_mount = cylinder(
                r=info.screw_class.radius + CaseProperties.screw_mount_width,
                # full contact with PCB, no gaps
                h=CaseProperties.size.z - device.pcb.bbox().zmax + EPS
            ).move(screw_mount_offset)
            case = case + screw_mount

            screw_layer_width = device.pcb.bbox().zmax - info.screw_offset.z
            screw_hole = cylinder(
                r=info.screw_class.radius,
                h=info.screw_class.length - screw_layer_width + CaseProperties.screw_length_margin
            ).move(screw_mount_offset)
            case = case - screw_hole

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

        lcd_screen_bbox = device.lcd_screen.bbox()  # type: BBox
        case = fillet(case, r=CaseProperties.width / 2, refs=points([
            (contact_pads_bbox.center_offset.x, contact_pads_bbox.ymax,
             CaseProperties.size.z + CaseProperties.width),
            (contact_pads_bbox.xmin, 1, CaseProperties.size.z + CaseProperties.width),
            (contact_pads_bbox.xmax, 1, CaseProperties.size.z + CaseProperties.width),
            (cap_bbox.center_offset.x, cap_bbox.center_offset.y, cap_bbox.zmax),
            (lcd_screen_bbox.xmin, lcd_screen_bbox.center_offset.y,
             CaseProperties.size.z + CaseProperties.width),
            (lcd_screen_bbox.xmax, lcd_screen_bbox.center_offset.y,
             CaseProperties.size.z + CaseProperties.width),
            (lcd_screen_bbox.center_offset.x, lcd_screen_bbox.ymin,
             CaseProperties.size.z + CaseProperties.width),
            (lcd_screen_bbox.center_offset.x, lcd_screen_bbox.ymax,
             CaseProperties.size.z + CaseProperties.width),
        ]))

        socket_bbox = device.socket.bbox()  # type: BBox
        case = fillet(case, r=1.4, refs=points([
            (socket_bbox.xmin, socket_bbox.center_offset.y, socket_bbox.zmax),
            (socket_bbox.xmax, socket_bbox.center_offset.y, socket_bbox.zmax),
            (socket_bbox.center_offset.x, socket_bbox.ymin, socket_bbox.zmax),
            (socket_bbox.center_offset.x, socket_bbox.ymax, socket_bbox.zmax),
            (0.01, socket_bbox.ymin + Socket.room_size.y + CaseProperties.socket_margin,
             socket_bbox.zmax),
        ]))

        case = fillet(case, r=1.0, refs=points([
            (0, 0, CaseProperties.size.z - 0.5),
            (0, CaseProperties.size.y, CaseProperties.size.z - 0.5),
            (CaseProperties.battery_wall_offset_x,
             0, CaseProperties.size.z - 0.5),
            (CaseProperties.battery_wall_offset_x,
             CaseProperties.size.y, CaseProperties.size.z - 0.5),
            (CaseProperties.battery_wall_offset_x + CaseProperties.battery_wall_width,
             0, CaseProperties.size.z - 0.5),
            (CaseProperties.battery_wall_offset_x + CaseProperties.battery_wall_width,
             CaseProperties.size.y, CaseProperties.size.z - 0.5),
            (CaseProperties.size.x, 0, CaseProperties.size.z - 0.5),
            (CaseProperties.size.x, CaseProperties.size.y, CaseProperties.size.z - 0.5),
        ]))

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

        screw_black_mount = box(size=(
            CaseProperties.screw_black_mount_width + EPS,
            CaseProperties.screw_black_mount_width + EPS,
            device.pcb.bbox().zmax + EPS
        )).move(vector3(
            CaseProperties.size.x - CaseProperties.screw_black_mount_width,
            -EPS,
            -EPS
        ))
        case = case + screw_black_mount

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

        contact_pads_hole = box(size=(
            contact_pads_bbox.size.x,
            contact_pads_bbox.size.y - CaseProperties.pcb_margin - CaseProperties.default_margin,
            CaseProperties.smd_margin
        )).move(vector3(
            contact_pads_bbox.offset.x,
            contact_pads_bbox.offset.y + CaseProperties.pcb_margin + CaseProperties.default_margin,
            device.pcb.bbox().zmin - CaseProperties.smd_margin
        ))
        case = case - contact_pads_hole

        power_terminals_bbox = device.power_terminals.bbox()  # type: BBox
        surface_mount_bbox = device.surface_mount.bbox()  # type: BBox
        lcd_mount_bbox = device.lcd_mount.bbox()  # type: BBox
        smd_hole_points = points([
            (power_terminals_bbox.xmin - CaseProperties.default_margin,
             power_terminals_bbox.ymax + CaseProperties.default_margin,
             0),
            (surface_mount_bbox.xmin - CaseProperties.default_margin,
             surface_mount_bbox.ymax + CaseProperties.default_margin,
             0),
            (surface_mount_bbox.xmax + CaseProperties.default_margin,
             surface_mount_bbox.ymax + CaseProperties.default_margin,
             0),
            (lcd_mount_bbox.xmax + CaseProperties.default_margin,
             lcd_mount_bbox.ymax + CaseProperties.default_margin,
             0),
            (lcd_mount_bbox.xmax + CaseProperties.default_margin,
             lcd_mount_bbox.ymin - CaseProperties.default_margin,
             0),
            (surface_mount_bbox.xmax + CaseProperties.default_margin,
             surface_mount_bbox.ymin - CaseProperties.default_margin,
             0),
            (surface_mount_bbox.xmin - CaseProperties.default_margin,
             surface_mount_bbox.ymin - CaseProperties.default_margin,
             0),
            (surface_mount_bbox.xmin - CaseProperties.default_margin,
             power_terminals_bbox.ymin - CaseProperties.default_margin,
             0),
            (power_terminals_bbox.xmin - CaseProperties.default_margin,
             power_terminals_bbox.ymin - CaseProperties.default_margin,
             0)
        ])
        smd_hole = extrude(
            proto=polysegment(smd_hole_points, closed=True).fill(),
            vec=CaseProperties.smd_margin
        ).moveZ(device.pcb.bbox().zmin - CaseProperties.smd_margin)
        case = case - smd_hole

        for obj in [
            device.quarts,
            device.socket_terminals,
            device.button_mount,
        ]:
            case = case - obj.bbox().with_border(CaseProperties.default_margin).to_zen_box()

        lock_bbox = device.lcd_lock1.bbox()  # type: BBox
        case = case - (cylinder(r=LcdLock1.radius + CaseProperties.default_margin,
                                h=LcdLock1.height + 2 * CaseProperties.default_margin, center=True)
                       .move(lock_bbox.center_offset))
        lock_bbox = device.lcd_lock2.bbox()  # type: BBox
        case = case - (cylinder(r=LcdLock2.radius + CaseProperties.default_margin,
                                h=LcdLock2.height + 2 * CaseProperties.default_margin, center=True)
                       .move(lock_bbox.center_offset))

        lcd_wires_bbox = device.lcd_wires.bbox()  # type: BBox
        lcd_wires_bbox = lcd_wires_bbox.with_border_x(CaseProperties.default_margin)
        lcd_wires_bbox = lcd_wires_bbox.with_border_y(CaseProperties.default_margin)
        lcd_wires_hole = box(size=(
            lcd_wires_bbox.size.x, lcd_wires_bbox.size.y,
            lcd_wires_bbox.size.z + CaseProperties.smd_margin
        )).move(vector3(
            lcd_wires_bbox.offset.x, lcd_wires_bbox.offset.y,
            lcd_wires_bbox.offset.z - CaseProperties.smd_margin
        ))
        case = case - lcd_wires_hole

        power_terminals_bbox = device.power_terminals.bbox()  # type: BBox
        power_terminals_bbox = power_terminals_bbox.with_border(CaseProperties.default_margin)
        battery_wires_hole = cylinder(
            r=PowerTerminals.wires_radius + CaseProperties.default_margin,
            h=device.pcb.bbox().zmin
        ).move(vector3(
            CaseProperties.pcb_offset.x + PowerTerminals.wires_offset.x,
            CaseProperties.pcb_offset.y + PowerTerminals.wires_offset.y,
            0.0
        ))
        case = case - battery_wires_hole

        battery_wires_channel = box(size=(
            (CaseProperties.battery_offset.x - power_terminals_bbox.xmin) / cos(deg(-15)),
            PowerTerminals.wires_radius * 2 + CaseProperties.default_margin * 2,
            CaseProperties.size.z + EPS2
        )).moveY(
            -PowerTerminals.wires_radius - CaseProperties.default_margin
        ).rotateZ(
            deg(-15)
        ).move(vector3(
            CaseProperties.pcb_offset.x + PowerTerminals.wires_offset.x,
            CaseProperties.pcb_offset.y + PowerTerminals.wires_offset.y,
            0.0
        ))
        case = case - battery_wires_channel

        for info in CaseScrews.screw_info_dict.values():
            screw_hole_h = info.screw_offset.z + CaseProperties.width + EPS
            screw_mount = cone(
                r1=(info.screw_class.cap_r + CaseProperties.screw_cap_margin * 2 +
                    CaseProperties.case_mount_width),
                r2=(info.screw_class.cap_r + CaseProperties.screw_cap_margin +
                    CaseProperties.case_mount_width),
                h=screw_hole_h + CaseProperties.case_mount_height - CaseProperties.width
            ).move(info.screw_offset).moveZ(-screw_hole_h + CaseProperties.width)
            case = case + screw_mount

            screw_hole = cone(
                r1=info.screw_class.cap_r + CaseProperties.screw_cap_margin * 2,
                r2=info.screw_class.cap_r + CaseProperties.screw_cap_margin,
                h=screw_hole_h
            ).move(info.screw_offset).moveZ(-screw_hole_h)
            case = case - screw_hole

            screw_hole = cylinder(
                r=info.screw_class.radius + CaseProperties.screw_radius_margin,
                h=CaseProperties.case_mount_height + EPS2
            ).move(info.screw_offset).moveZ(-EPS)
            case = case - screw_hole

        case = unify(case)

        case = fillet(case, r=CaseProperties.width / 2, refs=points([
            (contact_pads_bbox.center_offset.x, -CaseProperties.width, contact_pads_bbox.zmin),
            (contact_pads_bbox.xmin, -CaseProperties.width, contact_pads_bbox.zmin + 1),
            (contact_pads_bbox.xmax, -CaseProperties.width, contact_pads_bbox.zmin + 1),
        ]))

        socket_bbox = device.socket.bbox()  # type: BBox
        case = fillet(case, r=1.4, refs=points([
            (-CaseProperties.width, socket_bbox.ymin, CaseProperties.size.z - 1),
            (-CaseProperties.width,
             socket_bbox.ymin + Socket.room_size.y + CaseProperties.socket_margin,
             CaseProperties.size.z - 1),
            (-CaseProperties.width,
             socket_bbox.ymin + (Socket.room_size.y + CaseProperties.socket_margin) / 2.0,
             CaseProperties.size.z + CaseProperties.width - Socket.room_size.z),
        ]))

        case = fillet(case, r=1.0, refs=points([
            (
                info.screw_offset.x, info.screw_offset.y,
                -CaseProperties.width - 1
            )
            for info in CaseScrews.screw_info_dict.values()
        ]))

        case = fillet(case, r=1.4, refs=points([
            (CaseProperties.battery_wall_offset_x + CaseProperties.battery_wall_width, 0, 5),
            (CaseProperties.battery_wall_offset_x + CaseProperties.battery_wall_width, 7, 5),
            (CaseProperties.battery_wall_offset_x + CaseProperties.battery_wall_width, 10, 5),
            (CaseProperties.battery_wall_offset_x + CaseProperties.battery_wall_width,
             CaseProperties.size.y, 5),
            (CaseProperties.size.x, CaseProperties.size.y, 5),
            (CaseProperties.size.x - CaseProperties.screw_black_mount_width,
             CaseProperties.screw_black_mount_width, 5),
            (CaseProperties.size.x - CaseProperties.screw_black_mount_width / 2,
             CaseProperties.screw_black_mount_width, device.pcb.bbox().zmax),
            (CaseProperties.size.x - CaseProperties.screw_black_mount_width,
             CaseProperties.screw_black_mount_width / 2, device.pcb.bbox().zmax),
        ]))

        super().__init__(case)


class ScrewInfo(object):
    def __init__(self, screw_class, screw_offset):
        """
        :type screw_class: type[ScrewBase]
        :type screw_offset: pyservoce.libservoce.vector3
        """
        self.screw_class = screw_class
        self.screw_offset = screw_offset


class CaseScrews(CompoundZenObj):
    screw_info_dict = {
        'screw_nw': ScrewInfo(ScrewSilver,
                              CaseProperties.pcb_offset + Pcb.hole_vector_nw +
                              vector3(0, 0, -CaseProperties.case_mount_height)),
        'screw_se': ScrewInfo(ScrewSilver,
                              CaseProperties.pcb_offset + Pcb.hole_vector_se +
                              vector3(0, 0, -CaseProperties.case_mount_height)),
        'screw_ne': ScrewInfo(ScrewSilver,
                              CaseProperties.pcb_offset + Pcb.hole_vector_ne +
                              vector3(0, 0, -CaseProperties.case_mount_height)),
        'screw_sw': ScrewInfo(ScrewSilver,
                              CaseProperties.pcb_offset + Pcb.hole_vector_sw +
                              vector3(0, 0, -CaseProperties.case_mount_height)),
        'screw_black': ScrewInfo(ScrewBlack,
                                 CaseProperties.screw_black_offset)
    }  # type: dict[str, ScrewInfo]

    def __init__(self):
        screw_dict = {
            k: info.screw_class().transformed(move(info.screw_offset))
            for k, info in self.screw_info_dict.items()
        }
        super().__init__(**screw_dict)
