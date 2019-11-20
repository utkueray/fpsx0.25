import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *
import room, player, objLoader
import numpy as np
from timeit import default_timer as timer


x = 2.0
y = 1.0
z = 5.0

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
vertcont = vert

wall = True  # check if cursor hits the window borders
jump = False  # check if player wants to jump
speed = False  # check if slow down or fast
vel = 0.1  # walking velocity
jumpvel = 0.3  # jump velocity
c = 0

pygame.init()
size = 1080
display = (size, size)

pygame.display.set_mode(display, DOUBLEBUF | HWSURFACE | FULLSCREEN | OPENGL)
gluPerspective(90, (size / size), 0.1, 100.0)
start = timer()
end = timer()
thetax = 0
thetay = 0
def Crosshair(x, y, w):
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)
    glVertex2f(x-w, y)
    glVertex2f(x+w, y)
    glVertex2f(x, y-w)
    glVertex2f(x, y+w)
    glEnd()
while True:

    # clear environment
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # load map
    #room.loadFloor()
    room.loadWalls()
    #room.loadEntrance()
    objLoader.OBJ("cube.obj")



    # keyboard functions
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if keys[pygame.K_ESCAPE]:
            quit()

    # gettin hot

    if int(end-start+1) % 23 == 0 and speed:
        speed = False
    elif int(end-start+1) % 29 == 0 and not speed:
        speed = True
    if speed:
        vel = 0.05
        jumpvel = 0.1
    else:
        vel = 0.1
        jumpvel = 0.3


    print(int(end-start)+1)

    # Movement

    fwd = -vel * (keys[K_w] - keys[K_s])
    strafe = vel * (keys[K_a] - keys[K_d])

    if abs(fwd) or abs(strafe):
        try:
            player.move(fwd, strafe)
        except IndexError:
            pass

    if not jump:
        if keys[pygame.K_SPACE]:
            jump = True

    if jump:
        array = np.linspace(-1, 1)
        glTranslatef(0, jumpvel*np.linspace(-1, 1)[c], 0)
        c += 1
        if c == len(array):
            c = 0
            jump = False
    # Define mouse position and camera orientati on

    m = glGetDoublev(GL_MODELVIEW_MATRIX).flatten()
    pos = player.getposition()
    mouse_dx, mouse_dy = pygame.mouse.get_rel()
    mousepos = pygame.mouse.get_pos()
    pygame.mouse.set_visible(False)

    if wall:
        player.rotateworld(mouse_dx * 0.15, mouse_dy * 0.15)
        thetax = degrees(atan2(m[8], m[0]))
        thetay = degrees(atan2(-m[6], -m[8] * sin(radians(thetax)) + m[10] * cos(radians(thetax))))

    wall = True
    if mousepos[0] <= 1:
        pygame.mouse.set_pos(size, mousepos[1])
        wall = False
    if mousepos[0] >= size - 1:
        pygame.mouse.set_pos(0, mousepos[1])
        wall = False
    if mousepos[1] <= 1:
        pygame.mouse.set_pos(mousepos[0], size)
        wall = False
    if mousepos[1] >= size - 1:
        pygame.mouse.set_pos(mousepos[0], 0)
        wall = False

    # crosshair
    glDisable(GL_DEPTH_TEST)

    w = 1
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0.0, display[0], 0.0, display[1], -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    mX, mY = pygame.mouse.get_pos()
    Crosshair(display[0]/2, display[1]/2, 20)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    # update the display surface to screen
    pygame.display.flip()
    end = timer()

