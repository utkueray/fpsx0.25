import pygame
from OpenGL.GL import *

x = 20.0
ytop = 10.0
yfloor = -1.0
z = 20.0


def loadFloor():
    textureSurface = pygame.image.load('floorTexture.jpg')
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-x, yfloor, -z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, yfloor, -z)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, yfloor, z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-x, yfloor, z)
    glEnd()


def loadWalls():
    textureSurface = pygame.image.load('wallTexture.jpg')
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glBegin(GL_QUADS)

    # right wall
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x, yfloor, -z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x, ytop, -z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, ytop, z)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, yfloor, z)

    # left wall

    glTexCoord2f(0.0, 0.0)
    glVertex3f(-x, yfloor, -z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-x, yfloor, z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-x, ytop, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-x, ytop, -z)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(-x, yfloor, -z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-x, ytop, -z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, ytop, -z)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, yfloor, -z)

    glEnd()



def loadEntrance():
    textureSurface = pygame.image.load('wallTexture.jpg')
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glBegin(GL_QUADS)

    # right wall
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-x, yfloor, z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x, yfloor, z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x, ytop, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-x, ytop, z)

    glEnd()