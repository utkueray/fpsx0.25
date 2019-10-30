from OpenGL.GL import *


def wallcollide(player, fwd, strafe):
    m = glGetDoublev(GL_MODELVIEW_MATRIX).flatten()
    pos = player.getposition()
    pos = pos*-1
    if player.checkwall()[0] and player.checkwall()[1]:
        glTranslatef(fwd * m[2], 0, fwd * m[10])
        glTranslatef(strafe * m[0], 0, strafe * m[8])
    else:
        if not player.checkwall()[0]:
            if pos[0] > player.mulx:
                d = pos[0] - player.mulx
                glTranslatef(-d - player.buffer, 0, fwd * m[10])
                glTranslatef(0, 0, strafe * m[8])
            elif pos[0] < -player.mulx:
                d = pos[0] + player.mulx
                glTranslatef(-d + player.buffer, 0, fwd * m[10])
                glTranslatef(0, 0, strafe * m[8])

        elif not player.checkwall()[1]:
            if pos[2] > player.mulz:
                d = pos[2] - player.mulz
                glTranslatef(fwd * m[2], 0, -d - player.buffer)
                glTranslatef(strafe * m[0], 0, 0)
            elif pos[2] < -player.mulz:
                d = pos[2] + player.mulz
                glTranslatef(fwd * m[2], 0, -d + player.buffer)