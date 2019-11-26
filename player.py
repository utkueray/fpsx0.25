from OpenGL.GL import *
from math import *
import numpy as np
import room

margin = 0.3

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


def crosshair(edge, vert):
    glLineWidth(3)
    glBegin(GL_LINES)
    glColor3fv((0.047, 0.55, 0.97))
    for i in edge:
        for p in i:
            glVertex3fv(vert[p])
    glEnd()


def move(fwd, strafe):  # add collision detection
    m = glGetDoublev(GL_MODELVIEW_MATRIX).flatten()
    glTranslatef(fwd * m[2], 0, fwd * m[10])
    glTranslatef(strafe * m[0], 0, strafe * m[8])


def checkwall():
    k = [False, False]
    if -room.x+margin<= getposition()[0] <= room.x-margin:
        k[0] = True
    if -room.z+margin <= getposition()[2] <= room.z-margin:
        k[1] = True

    return k


def wallcollide(fwd, strafe):
    m = glGetDoublev(GL_MODELVIEW_MATRIX).flatten()
    pos = getposition()
    pos = pos * -1
    if checkwall()[0] and checkwall()[1]:
        glTranslatef(fwd * m[2], 0, fwd * m[10])
        glTranslatef(strafe * m[0], 0, strafe * m[8])
    else:
        if not checkwall()[0]:
            if pos[0] > room.x-margin:
                d = pos[0] - room.x
                glTranslatef(-d-margin, 0, fwd * m[10])
                glTranslatef(0, 0, strafe * m[8])
            elif pos[0] < -room.x+margin:
                d = pos[0] + room.x
                glTranslatef(-d+margin, 0, fwd * m[10])
                glTranslatef(0, 0, strafe * m[8])

        elif not checkwall()[1]:
            if pos[2] > room.z-margin:
                d = pos[2] - room.z
                glTranslatef(fwd * m[2], 0, -d-margin)
                glTranslatef(strafe * m[0], 0, 0)
            elif pos[2] < -room.z+margin:
                d = pos[2] + room.z
                glTranslatef(fwd * m[2], 0, -d+margin)
