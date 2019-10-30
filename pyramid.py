from room import Room
import numpy as np
import random
from OpenGL.GL import *


class Pyramid(Room):

    def __init__(self):
        Room.__init__(self)

        self.pvertices = [
            [Room.x, 0, Room.z],
            [Room.x, 0, -Room.z],
            [-Room.x, 0, -Room.z],
            [-Room.x, 0, Room.z],
            [0, Room.y, 0]
        ]

        self.pedges = (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (0, 4),
            (1, 4),
            (2, 4),
            (3, 4)

        )

        self.psurfaces = (
            (1, 0, 4),
            (2, 1, 4),
            (3, 2, 4),
            (3, 0, 4)
        )
        self.square = 2

        self.pvertices = np.array(np.multiply(np.array(self.pvertices), self.mul))
        self.pvertices = np.array(np.multiply(np.array(self.pvertices), (self.square, 1, self.square)))

        Pyramid.randtransform(self)

        self.positionp = [-self.pvertices[4][0], self.pvertices[4][1], -self.pvertices[4][2]]

    def randtransform(self):
        fac = 1 / (Room.num-1)

        self.pvertices = np.multiply(self.pvertices, (fac, fac*10, fac))

        randposx = random.choice(Room.mesh[1][self.square:Room.num-self.square])[0]*self.mul + self.mulx*fac*self.square
        randposz = random.choice(Room.mesh[0][self.square:Room.num-self.square])[2]*self.mul + self.mulz*fac*self.square

        self.pvertices = list(map(lambda vert: (vert[0] + randposx, vert[1],
                                                vert[2] + randposz), self.pvertices))

    def drawpyramid(self):
        glBegin(GL_QUADS)
        glColor3fv((1, 1, 1))
        for surface in self.psurfaces:
            for vertex in surface:
                glVertex3fv(self.pvertices[vertex])
        glEnd()

        glLineWidth(3)
        glBegin(GL_LINES)
        for edge in self.pedges:
            glColor3fv((1, 0, 1))
            for vertex in edge:
                glVertex3fv(self.pvertices[vertex])

        glEnd()

    def checkpyramid(self, player):
        pos = player.getposition()
        apex = self.pvertices[4]
        distx = abs(abs(self.pvertices[0][0]) - abs(apex[0]))
        distz = abs(abs(self.pvertices[0][2]) - abs(apex[2]))

        pushx = abs(abs(apex[0]) - abs(pos[0]))

        k = [False, False]

        if apex[0] - distx < pos[0] < apex[0] + distx:
            k[0] = True

        if apex[2] - distz < pos[2] < apex[2] + distz:
            k[1] = True

        if k[0] and k[1]:
            if pos[0] > apex[0]:
                glTranslatef(-pushx - player.buffer, 0, 0)
            elif pos[0] < apex[0]:
                glTranslatef(pushx + player.buffer, 0, 0)

        return k[0] and k[1]



