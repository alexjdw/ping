'''.obj file loader from https://www.pygame.org/wiki/OBJFileLoader'''

import pygame
from OpenGL.GL import *
from .drawable import Point3D, Shape2D, Shape3D


def MTL(filename):
    contents = {}
    mtl = None
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise ValueError("mtl file doesn't start with newmtl stmt")
        elif values[0] == 'map_Kd':
            # load the texture referred to by this declaration
            mtl[values[0]] = values[1]
            surf = pygame.image.load(mtl['map_Kd'])
            image = pygame.image.tostring(surf, 'RGBA', 1)
            ix, iy = surf.get_rect().size
            texid = mtl['texture_Kd'] = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                GL_UNSIGNED_BYTE, image)
        else:
            mtl[values[0]] = map(float, values[1:])
    return contents


# TODO: Convert to VBO format.
class OBJ:
    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = map(float, values[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = map(float, values[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(map(float, values[1:3]))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = MTL(values[1])
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))

        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords, material = face

            mtl = self.mtl[material]
            if 'texture_Kd' in mtl:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                # just use diffuse colour
                glColor(*mtl['Kd'])

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()


def OBJ_to_shape(self, filename, swapyz=False, suppress_not_implemented=True):
    '''
    Loads a wavefront file and returns a Shape3D.

    :param filename: The absolute path of the file to load.
    :param swapxyz: Swaps the y and z axes.
    :param suppress_not_implemented: If a .obj file format feature is not
      implemented, throw a NotImplementedError when this is True. We haven't
      implemented the full .obj scope, so generally you should set this to
      True. False is useful to see why parts of your model aren't loading or to
      potentially detect invalid .obj files.
    '''

    # TODO: Add additonal support for .obj files.
    # TODO: Add material support to the Shape2D class.

    # These functions handle one declaration in the obj file.
    # example: 'v .1 .2 .3' calls addVertex('v', '.1', '.2', '.3')

    def addVertex(state, values):
        v = map(float, values[1:4])
        if swapyz:
            v = (v[0], v[2], v[1])
        state['points'].append(Point3D(*v))

    def addNormal(state, values):
        v = map(float, values[1:4])
        if state.swapyz:
            v = v[0], v[2], v[1]
        state['normals'].append(v)

    def addTexture(state, values):
        state['texcoords'].append(map(float, values[1:3]))

    def setMaterial(self, values):
        state['curmat'] = values[1]

    def setMTL(self, values):
        state['mtl'] = MTL(values[1])

    def addPolygon(self, values):
        pcoords = []
        texcoords = []
        tex_arg = None
        norms = []
        norms_arg = None
        for v in values[1:]:
            # Split the vert/texture/normal triplet into the elements,
            # which refer to the index of their corresponding point object.
            items = v.split('/')
            items = [int(i) for i in items]
            pcoords.append(state['points'][items[0] - 1])
            if len(items) >= 2 and len(items[1]) > 0:
                texcoords.append(state['texcoords'](items[1]))
                tex_arg = texcoords
            if len(items) >= 3 and len(items[2]) > 0:
                norms.append(state['normals'](items[2]))
                norms_arg = norms
        state['shapes'].append(
            Shape2D(points,
                    texcoords=tex_arg,
                    normals=norms_arg,
                    mode=GL_POLYGON
                    )
            )

    state = {
        points: [],
        normals: [],
        texcoords: [],
        shapes: [],
        curmat: None,  # the currently selected material
        swapxyz: swapxyz
    }

    calls = {  # 'a': b means b is called for lines starting with 'a'.
        'v': addVertex,
        'vn': addNormal,
        'vt': addTexture,
        'usemtl': setMaterial,
        'usemat': setMaterial,
        'f': addPolygon}

    with open(filename, "r") as f:
        for line in f:
            if line.startswith('#'):  # line is a comment
                continue
            values = line.split()
            if not values:  # line is blank
                continue

            # call appropriate function
            try:
                calls[values[0]](state, values)
            except KeyError:
                if not suppress_not_implemented:
                    raise NotImplementedError(
                        f"Unable to parse .obj files with {values[0]} elements.\
                            To suppress this warning, pass \
                            suppress_not_implemented=True."
                        )

    normsarg, texarg = False, False
    if len(state['normals']):
        normsarg = True
    if len(state['texcoords']):
        texarg = True

    return Shape3D(state['shapes'],
                   enable_texture=texarg,
                   enable_normals=normsarg)
