from zencad import *

from api import BBox


class SliceBase(object):
    def __init__(self, cut):
        self.cut = cut

    def __call__(self, shape):
        return shape ^ self.cut


class SliceShape(SliceBase):
    def __init__(self, shape, normal_vector=(0, 1, 0), trans=None):
        """
        :type shape: pyservoce.libservoce.Shape
        """
        rotate_trans = short_rotate((0, 0, -1), normal_vector)
        cut = rotate_trans(halfspace())
        bbox = BBox.from_zen_bbox(shape.bbox())
        cut = cut.move(bbox.center_offset)
        if trans is not None:
            cut = trans(cut)
        super().__init__(cut)
