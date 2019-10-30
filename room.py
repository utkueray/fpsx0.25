import numpy as np
from OpenGL.GL import *
from math import atan2


class Room:

    x = 10
    y = 3
    z = 10

    num = 5

    grid = [
        [x, 0, z],
        [x, 0, -z],
        [-x, 0, -z],
        [-x, 0, z],
        [x, y, z],
        [x, y, -z],
        [-x, y, -z],
        [-x, y, z]

    ]

    mesh = [list(zip([x]*num, [0]*num, np.linspace(-z, z, num))),
            list(zip(np.linspace(-x, x, num), [0]*num, [-z]*num)),
            list(zip([-x]*num, [0]*num, np.linspace(-z, z, num))),
            list(zip(np.linspace(-x, x, num), [0]*num, [z]*num)),
            list(zip([x]*num, [y]*num, np.linspace(-z, z, num))),
            list(zip(np.linspace(-x, x, num), [y]*num, [-z]*num)),
            list(zip([-x]*num, [y]*num, np.linspace(-z, z, num))),
            list(zip(np.linspace(-x, x, num), [y]*num, [z]*num)),
            list(zip([x]*num, np.linspace(0, y, num), [z]*num)),
            list(zip([x]*num, np.linspace(0, y, num), [-z]*num)),
            list(zip([-x]*num, np.linspace(0, y, num), [-z]*num)),
            list(zip([-x]*num, np.linspace(0, y, num), [z]*num))]

    colors = [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1)
    ]

    edges = (
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
        self.mul = 800
        self.mulx = Room.x*self.mul
        self.mulz = Room.z*self.mul
        self.muly = Room.y*self.mul
        self.mesh = list(np.multiply(np.array(Room.mesh), self.mul))
        self.colors = Room.colors
        self.edges = Room.edges
        self.grid = list(np.multiply(np.array(Room.grid), self.mul))
        self.cont = self.grid

    def move(self, x, y, z):

        self.mesh = list(map(lambda vert: (x - vert[0],
                                           y - vert[1],
                                           z - vert[2]), self.mesh))

    def draw(self):
        glLineWidth(3)
        glBegin(GL_LINES)
        for edge in self.edges:
            glColor3f(1, 1, 1)

            for vertex in edge:
                glVertex3fv(self.grid[vertex])

        glEnd()

    def drawroom(self):
        glLineWidth(100)
        glBegin(GL_LINES)
        Room.surface(self, 0, 2, (0, 0, 1))
        Room.surface(self, 1, 3, (0, 0, 1))
        Room.surface(self, 0, 4, (0, 1, 0))
        Room.surface(self, 1, 5, (0, 1, 0))
        Room.surface(self, 2, 6, (0, 1, 0))
        Room.surface(self, 3, 7, (0, 1, 0))
        Room.surface(self, 4, 6, (1, 0.8, 0.8))
        Room.surface(self, 5, 7, (1, 0.8, 0.8))
        Room.surface(self, 8, 9, (0, 1, 0))
        Room.surface(self, 9, 10, (0, 1, 0))
        Room.surface(self, 10, 11, (0, 1, 0))
        Room.surface(self, 11, 8, (0, 1, 0))
        glEnd()

    def surface(self, e1, e2, color):
        glColor3fv(color)
        for i in range(Room.num):
            for j in (e1, e2):
                glVertex3fv(self.mesh[j][i])

    def rotateworld(self, anglex, angley):
        buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
        c = (-1 * np.mat(buffer[:3, :3]) * np.mat(buffer[3, :3]).T).reshape(3, 1)
        glTranslate(c[0], c[1], c[2])
        m = buffer.flatten()
        glRotate(anglex, m[1], m[5], m[9])  # [1]
        glRotate(angley, m[0], m[4], m[8])  # [1]
        glRotate(atan2(-m[4], m[5]) * 57.29577, m[2], m[6], m[10])
        glTranslate(-c[0], -c[1], -c[2])
