from collections import namedtuple

from zencad import *

Size = namedtuple('Size', ['x', 'y', 'z'])


class BBox(object):
    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax):
        """
        :param xmin: float
        :param xmax: float
        :param ymin: float
        :param ymax: float
        :param zmin: float
        :param zmax: float
        """
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    @staticmethod
    def from_zen_bbox(bbox):
        """
        :type bbox: pyservoce.libservoce.boundbox
        :rtype: BBox
        """
        return BBox(bbox.xmin, bbox.xmax, bbox.ymin, bbox.ymax, bbox.zmin, bbox.zmax)

    def __add__(self, other):
        return BBox(
            min(self.xmin, other.xmin), max(self.xmax, other.xmax),
            min(self.ymin, other.ymin), max(self.ymax, other.ymax),
            min(self.zmin, other.zmin), max(self.zmax, other.zmax)
        )

    def get_size(self):
        return Size(
            self.xmax - self.xmin,
            self.ymax - self.ymin,
            self.zmax - self.zmin
        )

    def get_offset(self):
        return vector3(self.xmin, self.ymin, self.zmin)

    def with_border(self, width):
        return BBox(
            self.xmin - width,
            self.xmax + width,
            self.ymin - width,
            self.ymax + width,
            self.zmin - width,
            self.zmax + width
        )


class ZenObj(object):
    """
    :type colour: None | Color
    """
    colour = None

    def __init__(self, colour=None):
        """
        :type colour: None | Color
        """
        self.colour = colour or self.colour

    def set_color(self, colour):
        """
        :type colour: None | Color
        """
        self.colour = colour

    def display(self, trans=None, colour=None):
        """
        Subclasses override this method to display itself with the provided transformation
        and color. If `colour` is `None`, every object is displayed with it's own color.

        :type trans: None | pyservoce.libservoce.transformation
        :type colour: None | Color
        :rtype: None
        """
        pass

    def bbox(self):
        """
        :rtype: BBox
        """

    def transformed(self, trans):
        """
        Subclasses override this method to implement transformations.

        :type trans: pyservoce.libservoce.transformation
        :rtype: ZenObj
        """
        pass


class CompoundZenObj(ZenObj):
    def __init__(self, *args, colour=None, **kwargs):
        """
        :type args: ZenObj
        :type colour: None | Color
        :type kwargs: ZenObj
        """
        super().__init__(colour)
        self.objects = list(args)
        self.objects_dict = dict(**kwargs)

    def __all_objects(self):
        return self.objects + [o for o in self.objects_dict.values()]

    def display(self, trans=None, colour=None):
        for o in self.__all_objects():
            o.display(trans, colour=colour or self.colour)

    def bbox(self):
        boxes = [o.bbox() for o in self.__all_objects()]
        return BBox(
            min(b.xmin for b in boxes), max(b.xmax for b in boxes),
            min(b.ymin for b in boxes), max(b.ymax for b in boxes),
            min(b.zmin for b in boxes), max(b.zmax for b in boxes)
        )

    def transformed(self, trans):
        objects = [o.transformed(trans) for o in self.objects]
        objects_dict = {k: v.transformed(trans) for k, v in self.objects_dict.items()}
        return CompoundZenObj(*objects, colour=self.colour, **objects_dict)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.objects[item]
        else:
            return self.objects_dict[item]

    def __getattr__(self, item):
        return self.objects_dict[item]


class SimpleZenObj(ZenObj):
    def __init__(self, shape, colour=None):
        """
        :type shape: pyservoce.libservoce.Shape
        :type colour: None | Color
        """
        super().__init__(colour)
        self.shape = shape

    def display(self, trans=None, colour=None):
        display(trans(self.shape) if trans else self.shape,
                color=colour or self.colour)

    def bbox(self):
        return BBox.from_zen_bbox(self.shape.bbox())

    def transformed(self, trans):
        return SimpleZenObj(trans(self.shape), colour=self.colour)
