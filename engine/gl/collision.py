from .utils import ReprMixin
import glm


class CollisionSystem(ReprMixin):
    "A grouping of objects that can possibly collide."
    def __init__(self):
        self.areas = []

    def detect(self):
        collisions = []
        areas = self.areas.copy()

        while len(areas):
            a = areas.pop()
            for b in areas:
                assert a is not b
                if a.detect_collision(b):
                    collisions.append((a, b))

        for a, b in collisions:
            if a.handler is not None:
                a.handler(a, b)
            elif b.handler is not None:
                b.handler(b, a)

    def add(self, area):
        self.areas.append(area)

    def __getitem__(self, i):
        return self.areas[i]

    def __setitem__(self, i, val):
        self.areas.__setitem__(i, val)

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
    '''
    A rectangle used for collision, represented by a point, offset,
    and size. The rectangle lays flat in the coordinate system;
    this greatly improves speed and simplifies the math.
    '''
    @classmethod
    def from_shape(cls, shape, suppress_no_collision_formula=False):
        "Creates a static bounding box around the shape."
        mmin = glm.vec3(shape.shapes[0].points[0].vertex)
        mmax = glm.vec3(mmin)
        for face in shape.shapes:
            for point in face.points:
                v = point.vertex
                mmin.x = min(mmin.x, v.x)
                mmin.y = min(mmin.y, v.y)
                mmin.z = min(mmin.z, v.z)
                mmax.x = max(mmax.x, v.x)
                mmax.y = max(mmax.y, v.y)
                mmax.z = max(mmax.z, v.z)
        size = mmax - mmin
        box = cls(size.x, size.y, size.z, suppress_no_collision_formula)
        print("Bounding box created with sizes: \n", size, " and offset: \n", mmin)
        box.attach_to_shape(shape)
        box.base_offset = mmin
        return box

    def __init__(self, width, height, depth,
                 suppress_no_collision_formula=False):
        self.base_offset = glm.vec3(0., 0., 0.)
        self.size = glm.vec3(float(width), float(height), float(depth))

        self.gluePoint = None
        self.glueShape = None
        self.glueOffset = None
        self.boundingBox = False
        self.supress = suppress_no_collision_formula
        self.handler_targets = []
        self.handler=None

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

    def attach_as_animated_bounding_box(self, shape, *points):
        '''
        Note: this is meant to dynamically set a bounding box for an
        object that deforms and is quite expensive. For a static bounding
        box, use the alternate constructor. In production, you can optimize
        by making a series of static collision boxes that track with the
        animations.

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

    @property
    def base(self):
        if self.gluePoint is not None:
            base = self.gluePoint.vertex + self.base_offset
        elif self.glueShape is not None:
            base = self.glueShape.offset[3].xyz + self.base_offset
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
            return box_sphere_collision(self, target)
        elif not self.suppress_errors:
            raise TypeError("CollisionBox can't collide with target")
        return False  # no way to detect collision


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
    return anear.x <= bfar.x and afar.x >= bnear.x and \
           anear.y <= bfar.y and afar.y >= bnear.y and \
           anear.z <= bfar.z and afar.z >= bnear.z


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
