from OpenGL.GL import *
from math import cos, sin, atan2
from math import radians as rad


class PlayerBox:
    # bullet dimensions
    x = 1
    y = 3
    z = 1

    grid = [
        [x, -y, z],
        [x, -y, -z],
        [-x, -y, -z],
        [-x, -y, z],
        [x, y, z],
        [x, y, -z],
        [-x, y, -z],
        [-x, y, z]
    ]

    bedges = (
        (1, 2),
        (2, 6),
        (2, 3),
        (0, 1),
        (0, 3),
        (0, 4),
        (1, 5),
        (3, 7),
        (6, 5),
        (4, 5),
        (7, 4),
        (6, 7)
    )

    def __init__(self):

        self.bvertices = PlayerBox.grid
        self.bedges = PlayerBox.bedges
        self.thetax = 0
        self.thetay = 0
        self.bvel = 0.5
        self.pos = [0, 0, 0]

    def drawTarget(self):
        glLineWidth(3)
        glBegin(GL_LINES)
        for edge in self.bedges:
            for vertex in edge:
                glVertex3fv(self.bvertices[vertex])

        glEnd()

    def tmove(self, x, y, z):

        self.bvertices = list(map(lambda vert: (vert[0] + x,
                                                vert[1] + y,
                                                vert[2] + z), self.bvertices))
        self.pos[0] += x
        self.pos[1] += y
        self.pos[2] += z

    def trotate(self, thetax, thetay):
        self.thetax = thetax
        self.thetay = thetay
        self.bvertices = list(map(lambda vert: (vert[2] * cos(rad(thetax)) - vert[0] * sin(rad(thetax)),
                                                vert[0] * sin(rad(thetay)) + vert[1] * cos(rad(thetay)),
                                                vert[0] * cos(rad(thetax)) + vert[2] * sin(rad(thetax))),
                                  self.bvertices))