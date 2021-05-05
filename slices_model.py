from zencad import *

from api import BBox


class SliceBase(object):
    def __init__(self, cut):
        self.cut = cut

    def __call__(self, shape):
        return shape ^ self.cut


class SliceShape(SliceBase):
    def __init__(self, shape):
        """
        :type shape: pyservoce.libservoce.Shape
        """
        cut = halfspace().rotateX(deg(90))
        bbox = BBox.from_zen_bbox(shape.bbox())
        cut = cut.moveY(bbox.center_offset.y)
        super().__init__(cut)
