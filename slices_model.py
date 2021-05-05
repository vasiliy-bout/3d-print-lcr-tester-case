from zencad import *


class SliceBase(object):
    def __init__(self, cut):
        self.cut = cut

    def __call__(self, shape):
        return shape ^ self.cut


class SliceButtonCap(SliceBase):
    def __init__(self, device):
        """
        :type device: Device
        """
        cut = halfspace().rotateX(deg(90))
        cut = cut.moveY(device.button_cap.bbox().center_offset.y)
        super().__init__(cut)
