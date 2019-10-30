import pygame
from pygame.locals import *
from OpenGL.GL import *
from player import Player
from pyramid import Pyramid
from bullet import Bullet
import numpy as np
import random
from misc import wallcollide
from math import cos, sin, atan2
from math import radians as rad
from math import degrees as deg


def main():
    size = 1080
    display = (size, size)
    pygame.display.set_mode(display, DOUBLEBUF | HWSURFACE | FULLSCREEN | OPENGL)

    player = Player()

    clock = pygame.time.Clock()
    exit = True # check if its time to exit
    wall = True #check if cursor hits the window borders
    sens = 0.25 # mouse sense
    vel = 20 # walking velocity
    thetax = 0
    thetay = 0
    jump = False

    bcheck = True

    randpyramid = random.choice([i for i in range(2, 7)])
    pyramid_list = []
    for i in range(randpyramid):
        x = Pyramid()
        pyramid_list.append(x)
    c = 0

    bullet_list = []

    while exit:

        clock.tick(144) #fps / hz

        for event in pygame.event.get():
            print(event) # current

        # Define mouse position and camera orientation

        m = glGetDoublev(GL_MODELVIEW_MATRIX).flatten()
        pos = player.getposition()
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        mousepos = pygame.mouse.get_pos()
        pygame.mouse.set_visible(False)


        # Define keys and getting direction of movement

        keys = pygame.key.get_pressed()
        fwd = -vel * (keys[K_w]-keys[K_s])
        strafe = vel * (keys[K_a]-keys[K_d])

        if abs(fwd) or abs(strafe):
            try:
                wallcollide(player, fwd, strafe)
            except IndexError:
                pass

        if keys[pygame.K_ESCAPE]:
            quit()

        if pygame.mouse.get_pressed() == (0, 0, 0):
            bcheck = True

        if bcheck:
            if pygame.mouse.get_pressed() == (1, 0, 0):
                b = Bullet()
                b.brotate(thetax, thetay)
                b.bmove(pos[0], pos[1], pos[2])
                bullet_list.append(b)
                bcheck = False

        if not jump:
            if keys[pygame.K_SPACE]:
                jump = True

        if jump:
            array = np.linspace(-1, 1)
            player.gravity(array[c])
            c += 1
            if c == len(array):
                c = 0
                jump = False

        if wall:
            player.rotateworld(mouse_dx*sens, mouse_dy*sens)
            thetax = deg(atan2(m[8], m[0]))
            thetay = deg(atan2(-m[6], -m[8]*sin(rad(thetax)) + m[10]*cos(rad(thetax))))

        if keys[pygame.K_UP]:
            player.rotateworld(0, -0.4)
            player.updatecross(0, -0.4)
        if keys[pygame.K_RIGHT]:
            player.rotateworld(0.4, 0)
            player.updatecross(0.4, 0)
        if keys[pygame.K_DOWN]:
            player.rotateworld(0, 0.4)
            player.updatecross(0, 0.4)
        if keys[pygame.K_LEFT]:
            player.rotateworld(-0.4, 0)
            player.updatecross(-0.4, 0)

        wall = True
        if mousepos[0] <= 1:
            pygame.mouse.set_pos(size, mousepos[1])
            wall = False
        if mousepos[0] >= size-1:
            pygame.mouse.set_pos(0, mousepos[1])
            wall = False
        if mousepos[1] <= 1:
            pygame.mouse.set_pos(mousepos[0], size)
            wall = False
        if mousepos[1] >= size-1:
            pygame.mouse.set_pos(mousepos[0], 0)
            wall = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        player.drawroom()
        player.draw()
        
        """for i in pyramid_list:
            i.drawpyramid()
            i.checkpyramid(player)"""

        for i in bullet_list:
            i.bmove(i.bvel*sin(rad(i.thetax)), -i.bvel*sin(rad(i.thetay)), -i.bvel*cos(rad(i.thetax)))
            i.drawbullet()
            try:
                if abs(i.pos[0]) > i.mulx:
                    bullet_list.remove(i)
                if abs(i.pos[2]) > i.mulz:
                    bullet_list.remove(i)
                if abs(i.pos[1]) > i.muly or i.pos[1] < 0:
                    bullet_list.remove(i)
            except ValueError:
                pass

        player.updatecross(thetax, -thetay)
        player.crosshair()

        if keys[K_KP_ENTER]:
            pygame.event.set_grab(True)
            pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
            pygame.mouse.set_pos(size / 2, size / 2)
            player.rotateworld(-thetax, -thetay)
            thetax, thetay = 0, 0
            player.crosshair()

        pygame.display.flip()
        print(player.getposition())


if __name__ == "__main__":
    main()
    pygame.quit()
    quit()
