from OpenGL.GL import *
from math import *
import numpy as np



def rotateworld(anglex, angley):
    buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
    c = (-1 * np.mat(buffer[:3, :3]) * np.mat(buffer[3, :3]).T).reshape(3, 1)
    glTranslate(c[0], c[1], c[2])  # becomes third person if removed
    m = buffer.flatten()
    glRotate(anglex, m[1], m[5], m[9])  # [1]
    glRotate(angley, m[0], m[4], m[8])  # [1]
    glRotate(atan2(-m[4], m[5]) * 57.29577, m[2], m[6], m[10])
    glTranslate(-c[0], -c[1], -c[2])


def getposition():
    buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
    c = (-1 * np.mat(buffer[:3, :3]) * np.mat(buffer[3, :3]).T).reshape(3, 1)
    return c


def crosshair(edge,vert):
    glLineWidth(3)
    glBegin(GL_LINES)
    glColor3fv((0.047, 0.55, 0.97))
    for i in edge:
        for p in i:
            glVertex3fv(vert[p])
    glEnd()


def movecross(vert2,x, y, z):
    vert2 = list(map(lambda vert2: (vert2[0] + x,
                                       vert2[1] + y,
                                       vert2[2] + z), vert2))


def move(fwd, strafe):
    m = glGetDoublev(GL_MODELVIEW_MATRIX).flatten()
    pos = getposition()
    pos = pos * -1
    glTranslatef(fwd * m[2], 0, fwd * m[10])
    glTranslatef(strafe * m[0], 0, strafe * m[8])


def rotatecross(vert2, thetax, thetay):
    vert2 = list(map(lambda vert2: (vert2[0] * cos(radians(thetax)) - vert2[2] * sin(radians(thetax)),
                                    vert2[1] * cos(radians(thetay)) - vert2[2] * sin(radians(thetay)),
                                    vert2[2] * cos(radians(thetax)) + vert2[0] * sin(radians(thetax))), vert2))

def updatecross():
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_LIGHTING)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-100, 100, -100, 100,5,50)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glVertex3f(20.0, 20.0, 0.0)
    glVertex3f(20.0, -20.0, 0.0)
    glVertex3f(-20.0, -20.0, 0.0)
    glVertex3f(-20.0, 20.0, 0.0)
    glEnd()
