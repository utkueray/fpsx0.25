from OpenGL.GLU import *
from OpenGL import GLUT as glut
from math import *
import room, player
import numpy as np
from pygame.locals import *
from timeit import default_timer as timer
from ObjLoader import *
from bullet import Bullet

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

pygame.display.set_mode(display, DOUBLEBUF | FULLSCREEN | OPENGL)
gluPerspective(90, (size / size), 0.1, 500.0)
start = timer()
end = timer()
thetax = 0
thetay = 0

def Crosshair(x, y, w):
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)
    glVertex2f(x - w, y)
    glVertex2f(x + w, y)
    glVertex2f(x, y - w)
    glVertex2f(x, y + w)
    glEnd()


# add object
sky = OBJ('SnowTerrain.obj')
m4 = OBJ("M4a1.obj")
house = OBJ("OldHouse.obj")

glTranslatef(10, -3, 10)
bullet_list = []

clock = pygame.time.Clock()


def drawText(value, x, y, windowHeight, windowWidth, step=18):
    """Draw the given text at given 2D position in window
    """
    glMatrixMode(GL_PROJECTION)
    # For some reason the GL_PROJECTION_MATRIX is overflowing with a single push!
    # glPushMatrix()
    matrix = glGetDouble(GL_PROJECTION_MATRIX)

    glLoadIdentity()
    glOrtho(0.0, windowHeight or 32, 0.0, windowWidth or 32, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2i(x, y)
    lines = 10
    ##	import pdb
    ##	pdb.set_trace()
    for character in value:
        if character == '\n':
            glRasterPos2i(x, y - (lines * 18))
        else:
            glut.glutBitmapCharacter(glut.fonts.GLUT_BITMAP_9_BY_15, ord(character))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    # For some reason the GL_PROJECTION_MATRIX is overflowing with a single push!
    # glPopMatrix();
    glLoadMatrixd(matrix)  # should have un-decorated alias for this...

    glMatrixMode(GL_MODELVIEW)


while True:
    clock.tick()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # load map
    room.loadFloor()

    # keyboard functions
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if keys[pygame.K_ESCAPE]:
            quit()

    # gettin hot

    if int(end - start + 1) % 23 == 0 and speed:
        speed = False
    elif int(end - start + 1) % 29 == 0 and not speed:
        speed = True
    if speed:
        vel = 0.05
        jumpvel = 0.1
    else:
        vel = 0.1
        jumpvel = 0.3

    # Movement

    fwd = -vel * (keys[K_w] - keys[K_s])
    strafe = vel * (keys[K_a] - keys[K_d])

    if abs(fwd) or abs(strafe):
        try:
            player.wallcollide(fwd, strafe)
        except IndexError:
            pass

    if not jump:
        if keys[pygame.K_SPACE]:
            jump = True

    if jump:
        array = np.linspace(-1, 1)
        glTranslatef(0, jumpvel * np.linspace(-1, 1)[c], 0)
        c += 1
        if c == len(array):
            c = 0
            jump = False

    # Define mouse position and camera orientation

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

    # firing

    if pygame.mouse.get_pressed() == (1, 0, 0):
        b = Bullet()
        b.brotate(thetax, thetay)
        b.bmove(pos[0], pos[1], pos[2])
        bullet_list.append(b)

    for i in bullet_list:
        i.bmove(i.bvel * sin(radians(i.thetax)), -i.bvel * sin(radians(i.thetay)), -i.bvel * cos(radians(i.thetax)))
        i.drawbullet()
        try:
            if abs(i.pos[0]) > 50:
                bullet_list.remove(i)
            if abs(i.pos[2]) > 50:
                bullet_list.remove(i)
            if abs(i.pos[1]) > 50 or i.pos[1] < 0:
                bullet_list.remove(i)
        except ValueError:
            pass


    # add objects
    glCallList(sky.gl_list)

    glPushMatrix()
    buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
    s = (-1 * np.mat(buffer[:3, :3]) * np.mat(buffer[3, :3]).T).reshape(3, 1)
    glTranslate(s[0], 2.75, s[2])  # becomes third person if removed
    glTranslatef(0, jumpvel * np.linspace(-1, 1)[c], 0)
    m = buffer.flatten()
    glRotate(-thetax, m[1], m[5], m[9])  # [1]
    glRotate(thetay + 180, m[0], m[4], m[8])  # [1]
    glRotate(atan2(-m[4], m[5]) * 57.29577, m[2], m[6], m[10])
    glCallList(m4.gl_list)
    glPopMatrix()

    glCallList(house.gl_list)

    # crosshair
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0.0, display[0], 0.0, display[1], -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    Crosshair(size / 2, size / 2, 15)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    drawText(str(int(clock.get_fps())), 1, 95, 100, 100)
    drawText("Health: "+str(int(100)), 90, 5, 100, 100)

    end = timer()

    pygame.display.flip()

