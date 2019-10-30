from room import Room
from math import sqrt, sin, cos
from math import radians as rad
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


class Player(Room):
    x = 5
    y = 5
    z = 100

    vert = [
        [0, y, -z],
        [0, -y, -z],
        [x, 0, -z],
        [-x, 0, -z]
    ]
    edge = (
        (0, 1),
        (2, 3)
    )

    def __init__(self, display=(1, 1), fov=90):
        Room.__init__(self)
        self.vert = Player.vert
        self.vertcont = self.vert
        self.edge = Player.edge
        self.buffer = 2
        self.crossd = Player.z
        self.starty = 400
        self.jumpvel = 30
        self.relvel = self.jumpvel
        gluPerspective(fov, (display[0] / display[1]), 0.1, 10000)
        glTranslatef(0, -self.starty, 0)
        Player.movecross(self, 0, self.starty, -self.crossd)

    def gravity(self, mul):
        glTranslatef(0, self.jumpvel*mul, 0)

    def checkwall(self):

        k = [False, False]
        if -self.mulx < Player.getposition(self)[0] < self.mulx:
            k[0] = True
        if -self.mulz < Player.getposition(self)[2] < self.mulz:
            k[1] = True

        return k

    def crosshair(self):
        glLineWidth(3)
        glBegin(GL_LINES)
        glColor3fv((0.047, 0.55, 0.97))
        for i in self.edge:
            for p in i:
                glVertex3fv(self.vert[p])
        glEnd()

    def movecross(self, x, y, z):
        self.vert = list(map(lambda vert: (vert[0] + x,
                                           vert[1] + y,
                                           vert[2] + z), self.vert))

    def updatecross(self, thetax, thetay):
        self.vert = self.vertcont
        pos = Player.getposition(self)
        Player.rotatecross(self, thetax, thetay)
        Player.movecross(self, pos[0], pos[1], pos[2])

    def rotatecross(self, thetax, thetay):
        self.vert = list(map(lambda vert: (vert[0]*cos(rad(thetax)) - vert[2]*sin(rad(thetax)),
                                           vert[1]*cos(rad(thetay)) - vert[2]*sin(rad(thetay)),
                                           vert[2] * cos(rad(thetax)) + vert[0] * sin(rad(thetax))), self.vert))

    def getposition(self):
        buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
        c = (-1 * np.mat(buffer[:3, :3]) * np.mat(buffer[3, :3]).T).reshape(3, 1)
        return c
