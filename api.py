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
        self.__xmin = xmin
        self.__xmax = xmax
        self.__ymin = ymin
        self.__ymax = ymax
        self.__zmin = zmin
        self.__zmax = zmax

        self.__size = None
        self.__offset = None
        self.__center_offset = None

    @property
    def xmin(self):
        return self.__xmin

    @property
    def xmax(self):
        return self.__xmax

    @property
    def ymin(self):
        return self.__ymin

    @property
    def ymax(self):
        return self.__ymax

    @property
    def zmin(self):
        return self.__zmin

    @property
    def zmax(self):
        return self.__zmax

    @staticmethod
    def from_zen_bbox(bbox):
        """
        :type bbox: pyservoce.libservoce.boundbox
        :rtype: BBox
        """
        return BBox(bbox.xmin, bbox.xmax, bbox.ymin, bbox.ymax, bbox.zmin, bbox.zmax)

    @staticmethod
    def from_zen_shape(shape):
        """
        :type shape: pyservoce.libservoce.Shape
        :rtype: BBox
        """
        return BBox.from_zen_bbox(shape.bbox())

    def to_zen_box(self):
        return box(size=self.size).move(self.offset)

    def __add__(self, other):
        return BBox(
            min(self.__xmin, other.xmin), max(self.__xmax, other.xmax),
            min(self.__ymin, other.ymin), max(self.__ymax, other.ymax),
            min(self.__zmin, other.zmin), max(self.__zmax, other.zmax)
        )

    @property
    def size(self):
        """
        :rtype: Size
        """
        if not self.__size:
            self.__size = Size(
                self.__xmax - self.__xmin,
                self.__ymax - self.__ymin,
                self.__zmax - self.__zmin
            )
        return self.__size

    @property
    def offset(self):
        """
        :rtype: pyservoce.vector3
        """
        if not self.__offset:
            self.__offset = vector3(self.__xmin, self.__ymin, self.__zmin)
        return self.__offset

    @property
    def center_offset(self):
        """
        :rtype: pyservoce.vector3
        """
        if not self.__center_offset:
            self.__center_offset = vector3(
                (self.__xmax + self.__xmin) / 2.0,
                (self.__ymax + self.__ymin) / 2.0,
                (self.__zmax + self.__zmin) / 2.0
            )
        return self.__center_offset

    def with_border(self, width):
        return BBox(
            self.__xmin - width,
            self.__xmax + width,
            self.__ymin - width,
            self.__ymax + width,
            self.__zmin - width,
            self.__zmax + width
        )

    def with_border_x(self, width):
        return BBox(
            self.__xmin - width,
            self.__xmax + width,
            self.__ymin,
            self.__ymax,
            self.__zmin,
            self.__zmax
        )

    def with_border_y(self, width):
        return BBox(
            self.__xmin,
            self.__xmax,
            self.__ymin - width,
            self.__ymax + width,
            self.__zmin,
            self.__zmax
        )

    def with_border_z(self, width):
        return BBox(
            self.__xmin,
            self.__xmax,
            self.__ymin,
            self.__ymax,
            self.__zmin - width,
            self.__zmax + width
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

        :type trans: None | pyservoce.libservoce.transformation | \
                     (pyservoce.libservoce.Shape) -> pyservoce.libservoce.Shape
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

        :type trans: pyservoce.libservoce.transformation | \
                     (pyservoce.libservoce.Shape) -> pyservoce.libservoce.Shape
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
        self.__objects = list(args)
        self.__objects_dict = dict(**kwargs)
        self.__hidden = []

    def hide(self, name):
        self.__hidden.append(name)

    def __all_objects(self):
        return self.__objects + [o for o in self.__objects_dict.values()]

    def display(self, trans=None, colour=None):
        for o in self.__objects:
            o.display(trans, colour=colour or self.colour)

        for k, o in self.__objects_dict.items():
            if k not in self.__hidden:
                o.display(trans, colour=colour or self.colour)

    def bbox(self):
        boxes = [o.bbox() for o in self.__all_objects()]
        return BBox(
            min(b.xmin for b in boxes), max(b.xmax for b in boxes),
            min(b.ymin for b in boxes), max(b.ymax for b in boxes),
            min(b.zmin for b in boxes), max(b.zmax for b in boxes)
        )

    def transformed(self, trans):
        objects = [o.transformed(trans) for o in self.__objects]
        objects_dict = {k: v.transformed(trans) for k, v in self.__objects_dict.items()}
        return CompoundZenObj(*objects, colour=self.colour, **objects_dict)

    def __getitem__(self, item):
        """
        :type item: int | str
        :rtype: ZenObj
        """
        if isinstance(item, int):
            return self.__objects[item]
        else:
            return self.__objects_dict[item]

    def __getattr__(self, item):
        """
        :type item: str
        :rtype: ZenObj
        """
        return self.__objects_dict[item]


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
