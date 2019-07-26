import pygame
import numpy as np
import glm
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
from OpenGL.arrays.vbo import VBO
from .Point3D import Point3D
from .Rect2D import Rect2D
from .Shape2D import Shape2D
from .. import shader_presets
from ..utils import ReprMixin


class Shape3D(ReprMixin):
    "A 3d shape made from a collection of 2d faces."
    def __init__(self,
                 shapes_list,
                 color=None,
                 mode=GL_TRIANGLES,
                 offset=None,
                 rotate=None,
                 scale=None):
        '''
        Builds a 3D shape from the given shape list with the given arguments.

        :param shapes_list: The faces of the shape.
        :param color: Applies a color to any vertex with no color data.
        :param mode: GL drawing mode constant, normally GL_TRIANGLES.
        :param offset: (x, y, z) offset in 3D space.
        '''
        self.shapes = shapes_list
        if color is not None:
            for s in self.shapes:
                for p in s.points:
                    if p.color is None:
                        p.color = color
        self.offset = offset if offset else glm.mat4()
        self.rotate = rotate if rotate else glm.mat4()
        self.scale = scale if scale else glm.mat4()
        self._matrix = None
        self.mode = mode
        self._VAO = None
        self._VBO_is_compiled = False
        # self._VBO_contexts = []

    def GLDraw(self):
        "Draws the shape. Old-style drawing mechanism. Deprecated."
        for s in self.shapes:
            s.GLDraw()

    def GLDraw_outline(self):
        "Old-style drawing mechanism. Draws the outline. Deprecated."
        for s in self.shapes:
            s.GLDraw_outline()

    def compile_VBO(self, force=False):
        "Compiles the verticies of all faces into a VBO and saves the ref."
        if self._VBO_is_compiled and not force:
            return
        vbos = []
        try:
            self._VBO_format = self.shapes[0].compile_VBO(force=True)
        except IndexError:
            raise ValueError("Shape3D tried to compile to VBO, but it didn't\
                              have any shapes.")
        for s in self.shapes:
            fmt = s.compile_VBO()
            if fmt != self._VBO_format and fmt is not None:
                # TODO figure out a good way of filling in the blanks?
                raise ValueError("While compiling a Shape3D to VBO, a Shape2D\
                    format mismatched with the format for the other shapes.")
            vbos.append(s._VBO)

        self._VBO = VBO(np.concatenate(vbos))
        self._VBO_is_compiled = True

    @property
    def model_matrix(self):
        '''
        The transform matrix is a way to transform of an object
        at draw time without overwriting all of its members.

        This is calculated lazily only if ._matrix doesn't exist, create it.
        Modifying the offset, rotate, or scale will reset the value of _matrix
        to None and cause it to recalculate the next time it's used. This
        avoids repetitive calculations for objects that don't move.
        '''
        if self._matrix is None:
            self._matrix = self.offset * self.rotate * self.scale
        return self._matrix

    @property
    def render_data(self):
        if not self._VBO_is_compiled:
            self.compile_VBO()
        return (self._VBO, self.mode)

    def move(self, x, y, z):
        "Moves the shape around the world."
        self.offset[3][0] = self.offset[3][0] + x
        self.offset[3][1] = self.offset[3][1] + y
        self.offset[3][2] = self.offset[3][2] + z
        self._matrix = None

    def move_relative_to_camera(self, right, up, back):
        "Moves the shape relative to the camera position."
        # TODO
        pass

    # The below three properties are used to in the transform matrix.
    # Resetting the matrix to None enables a lazy calculation.
    def get_offset(self):
        return self._offset

    def set_offset(self, val):
        self._matrix = None
        self._offset = val

    def get_rotate(self):
        return self._rotate

    def set_rotate(self, val):
        self._matrix = None
        self._rotate = val

    def get_scale(self):
        return self._scale

    def set_scale(self, val):
        self._matrix = None
        self._scale = val

    offset = property(get_offset, set_offset)
    rotate = property(get_rotate, set_rotate)
    scale = property(get_scale, set_scale)

    def gen_normals(self):
        """Generates a normal vector for each of the attached
        points if one hasn't been generated already."""
        pointd = {}
        for shape in self.shapes:
            count = 0
            verts = []
            for point in shape.points:
                if count < 3:
                    verts.append(point.vertex)
                    count += 1
            shape.normal = glm.normalize(
                glm.cross(
                    verts[1] - verts[0],
                    verts[2] - verts[0]
                    ))
            for point in shape.points:
                if point not in pointd:
                    pointd[point] = [shape.normal]
                else:
                    pointd[point].append(shape.normal)
            if count < 3:
                raise ValueError("Unable to calculate normal for shape with < 3 verticies. (It's not a viable surface)")
        for point, norms in pointd.items():
            if point.normal is None:
                point.normal = sum(verts) / len(verts)

    def center_and_normalize(self, scale=1.0):
        '''
        Scales down the object to fit in world space, 
        defaulting to a box from (1, 1, 1) to
        (-1, -1, -1)

        :param scale: Applies a scalar to the final result.
        '''
        count = 0
        center = glm.vec3(0., 0., 0.)
        farthest = 0.
        for shape in self.shapes:
            for point in shape.points:
                count += 1
                center += point.vertex
        center = center / float(count)

        # center the object
        for shape in self.shapes:
            for point in shape.points:
                point.vertex = point.vertex - center
                farthest = max([glm.sqrt(point.vertex.x ** 2 +
                                         point.vertex.y ** 2 +
                                         point.vertex.z ** 2),
                                farthest])
        # scale the objects verticies in relation to the furthest point from
        # the center
        scale = scale / farthest
        for shape in self.shapes:
            for point in shape.points:
                point.vertex = point.vertex * scale


# Alternate constructors
def box(width, height, depth, first_point, color=None):
    'Constructs a rectangular box.'
    h = glm.vec3(height, 0, 0)
    w = glm.vec3(0, width, 0)
    d = glm.vec3(0, 0, depth)
    p1 = glm.vec3(first_point.vertex)
    points = [p1,
              p1 + w,
              p1 + h,
              p1 + w + h,
              p1 + d,
              p1 + d + w,
              p1 + d + h,
              p1 + d + h + w]

    for index, point in enumerate(points):
        points[index] = Point3D(point[0], point[1], point[2], color)

    shapes = [
        Rect2D([points[0], points[1], points[2], points[3]]),
        Rect2D([points[1], points[5], points[3], points[7]]),
        Rect2D([points[4], points[0], points[6], points[2]]),
        Rect2D([points[4], points[5], points[0], points[1]]),
        Rect2D([points[2], points[3], points[6], points[7]]),
        Rect2D([points[5], points[4], points[7], points[6]]),
    ]

    return Shape3D(shapes, color)


def cube(length, first_point, color=None):
    'Constructs a cube.'
    return box(length, length, length, first_point, color)


def pyramid(base_len, base_wid, height, first_point, color=None):
    pass


def sphere(radius, first_point, detail=2, color=None):
    def middle_point(point_1, point_2):
        """ Find a middle point and project to the unit sphere """

        # We check if we have already cut this edge first
        # to avoid duplicated verts
        smaller_index = min(point_1, point_2)
        greater_index = max(point_1, point_2)

        key = '{0}-{1}'.format(smaller_index, greater_index)

        if key in middle_point_cache:
            return middle_point_cache[key]

        # If it's not in cache, then we can cut it
        vert_1 = verts[point_1]
        vert_2 = verts[point_2]
        middle = [sum(i)/2 for i in zip(vert_1.vertex, vert_2.vertex)]

        verts.append(icoso_vertex(*middle))

        index = len(verts) - 1
        middle_point_cache[key] = index

        return index

    def icoso_vertex(x, y, z):
        'Return vertex coordinates fixed to the unit sphere'
        length = glm.sqrt(x * x + y * y + z * z)

        return Point3D(
            x * radius / length,
            y * radius / length,
            z * radius / length,
        )

    middle_point_cache = {}
    PHI = (1 + glm.sqrt(5)) / 2
    verts = [
            icoso_vertex(-1,  PHI, 0),
            icoso_vertex( 1,  PHI, 0),
            icoso_vertex(-1, -PHI, 0),
            icoso_vertex( 1, -PHI, 0),

            icoso_vertex(0, -1, PHI),
            icoso_vertex(0,  1, PHI),
            icoso_vertex(0, -1, -PHI),
            icoso_vertex(0,  1, -PHI),

            icoso_vertex( PHI, 0, -1),
            icoso_vertex( PHI, 0,  1),
            icoso_vertex(-PHI, 0, -1),
            icoso_vertex(-PHI, 0,  1),
            ]

    faces = [
            # 5 faces around point 0
            [0, 11, 5],
            [0, 5, 1],
            [0, 1, 7],
            [0, 7, 10],
            [0, 10, 11],

            # Adjacent faces
            [1, 5, 9],
            [5, 11, 4],
            [11, 10, 2],
            [10, 7, 6],
            [7, 1, 8],

            # 5 faces around 3
            [3, 9, 4],
            [3, 4, 2],
            [3, 2, 6],
            [3, 6, 8],
            [3, 8, 9],

            # Adjacent faces
            [4, 9, 5],
            [2, 4, 11],
            [6, 2, 10],
            [8, 6, 7],
            [9, 8, 1]]

    for i in range(detail):
        faces_subdiv = []

        for tri in faces:
            v1 = middle_point(tri[0], tri[1])
            v2 = middle_point(tri[1], tri[2])
            v3 = middle_point(tri[2], tri[0])

            faces_subdiv.append([tri[0], v1, v3])
            faces_subdiv.append([tri[1], v2, v1])
            faces_subdiv.append([tri[2], v3, v2])
            faces_subdiv.append([v1, v2, v3])

        faces = faces_subdiv

    for i, face in enumerate(faces):
        # reuse faces to save a bit of memory here
        faces[i] = Shape2D([verts[point] for point in face])

    sphere = Shape3D(faces)
    sphere.gen_normals()
    # sphere.offset = glm.vec4(first_point.vertex, 1)
    return sphere