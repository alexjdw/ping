class Rect2D(ReprMixin):
    "A 2d rectangle made from a collection of four points."
    def __init__(self, points_list, color=(0,0,0)):
        self.points = points_list
        if len(points_list != 4):
            raise AttributeError("to form a square, include four points.")
        self.color = color

    def GLDraw(self):
        glBegin(GL_TRIANGLES)
        glColor3fv(self.color)
        for p in self.points:
            glVertex3fv(p.vertex)
        glEnd()

    def GLDraw_outline(self):
        glBegin(GL_LINES)
        glVertex3fv(self.points)
        glEnd()
