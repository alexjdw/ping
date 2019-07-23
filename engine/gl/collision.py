from .utils import ReprMixin


class CollisionSystem(ReprMixin):
    "A grouping of objects that can possibly collide."
    def __init__(self):
        self.areas = []

    def __setitem__(self, i, val):
        self.areas.__setitem__(i, val)

    def detect(self):
        collisions = []
        areas = self.areas.copy()

        while len(areas):
            a = areas.pop()
            for b in self.areas:
                if a.detect_collision(b):
                    collisions.append((a, b))

        for a, b in collisions:
            if self.handlers[a] is not None:
                self.handlers[a](a, b)
            if self.handlers[b] is not None:
                self.handlers[b](b, a)

    def add_collision(self, obj, handler=None):
        ''':param obj: The collision object (not the model)
        :param handler: A function to call on collision.'''
        assert hasattr(obj, 'detect_collision')
        self.handlers[obj] = handler

    def set_handler(self, obj, handler):
        self.handlers[obj] = handler

    def __getitem__(self, i):
        return self.areas[i]

    def __delitem__(self, i):
        del self.areas[i]

    def __len__(self):
        return len(self.areas)


class CollisionFrame(list, ReprMixin):
    'A class for holding multiple collision boxes.'
    def detect_collision(self, target):
        for item in self:
            if item.detect_collision():
                return True


class CollisionBox(ReprMixin):
    def __init__(self, width, height, depth,
                 suppress_no_collision_formula=False):
        self.base_offset = glm.vec3(0., 0., 0.)
        self.size = glm.vec3(float(width), float(height), float(depth))

        self.gluePoint = None
        self.glueShape = None
        self.glueOffset = None
        self.boundingBox = False
        self.supress = suppress_no_collision_formula

    def attach_to_point(self, point):
        self.gluePoint = point
        self.glueShape = None

    def attach_to_shape(self, shape):
        '''
        This function uses the shape's offset when calculating collision,
        but does not resize the collision box.
        '''
        self.gluePoint = None
        self.glueShape = shape

    def attach_as_bounding_box(self, shape, *points):
        '''
        Note: this is meant to dynamically set a bounding box for an
        object that deforms and is quite expensive. If possible, calculate
        a static bounding box ahead of time and use attach_to_point
        or attach_to_shape.

        :param shape: the shape to attach to.
        :param *points: points to check for minimum/maximum x, y, and z values.

        self.base_offset will still offset the bounding box, so set it to 0 0 0 if it's an issue.
        '''
        if len(points) < 2:
            raise ValueError("Points should be at least two items long; three is preferred. Otherwise, use CollsionBox.attach_to_point.")
        self.glueShape = shape
        self.boundingBox = True
        self.boundingPoints = points

    def detach(self):
        self.gluePoint = None
        self.glueShape = None
        self.boundingBox = False
        self.boundingPoints = None
        self.detect_collision = CollisionBox.detect_collision

    @classmethod
    def from_Shape3D(cls, shape):
        # TODO
        pass

    @property
    def base(self):
        base = self.base_offset
        if self.gluePoint is not None:
            base = gluePoint.vertex + base
        elif self.glueShape is not None:
            base = glueShape.offset + base
            if self.boundingBox:
                xmin = xmax = self.boundingPoints[0].vertex.x
                ymin = ymax = self.boundingPoints[0].vertex.y
                zmin = zmax = self.boundingPoints[0].vertex.z
                for p in self.boundingPoints:
                    xmin = min(xmin, p.vertex.x)
                    xmax = max(xmax, p.vertex.y)
                    ymin = min(ymin, p.vertex.y)
                    ymax = max(ymax, p.vertex.y)
                    zmin = min(zmin, p.vertex.z)
                    zmax = max(zmax, p.vertex.z)
                offset = glm.vec3(xmin, ymin, zmin)
                base = base + offset
                self.size = glm.vec3(xmax, ymax, zmax) - offset

        return base

    def detect_collision(self, target):
        if isinstance(target, CollisionBox):
            return box_box_collision(self, target)

        elif isinstance(target, CollisionSphere):
            pass
        elif not self.suppress_errors:
            raise TypeError("CollisionBox can't collide with target")
        return False


# ################### ###
# Collision functions ###
# ################### ###

def point_box_collision(p, b):
    v = p.vertex
    anear = a.base           # my near corner
    afar = anear + a.size    # my far corner
    return anear.x <= v.x and anear.y <= v.y and anear.z <= v.z and \
        afar.x >= v.x and afar.y >= v.y and afar.z >= v.z


def box_box_collision(a, b):
    'True if two 3d boxes intersect. Otherwise, False.'
    anear = a.base           # my near corner
    afar = anear + a.size    # my far corner
    bnear = b.base         # targetbox near corner
    bfar = bnear + b.size  # targetbox far corner
    return (anear.x <= bfar.x and afar.x >= bnear.x) and \
           (anear.x <= bfar.y and afar.y >= bnear.y) and \
           (anear.z <= bfar.z and afar.z >= bnear.z)


def box_sphere_collision(box, sph):
    # get box closest point to sph center by clamping
    near = box.base
    far = base + box.size
    x = max(base.x, min(sph.x, far.x))
    y = max(base.y, min(sph.y, far.y))
    z = max(base.z, min(sph.z, far.z))

    distance = (x - sph.x) ** 2 + \
               (y - sph.y) ** 2 + \
               (z - sph.z) ** 2

    return distance < sph.radius ** 2
