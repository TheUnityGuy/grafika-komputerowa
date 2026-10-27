#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from random import randint

w_width = 400
w_height = 400
triangle_scale = 5.0

def startup():
    update_viewport(None, w_width, w_height)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

'''
#trojkaty na 3.0
def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_TRIANGLES)

    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(-20.0 * triangle_scale, -20.0 * triangle_scale)  # lewy dolny
    
    glColor3f(0.0, 1.0, 1.0)
    glVertex2f(20.0 * triangle_scale, -20.0 * triangle_scale)  # prawy dolny
    
    glColor3f(1.0, 0.0, 1.0)
    glVertex2f(0.0, 20.0 * triangle_scale)  # górny
    glEnd()

    glFlush()
'''

def genRandFlt():
    return float(randint(0, 100))/100

lg_color = tuple(genRandFlt() for _ in range(3))
pd_color = tuple(genRandFlt() for _ in range(3))
white = (1.0, 1.0, 1.0)
black = (0.0, 0.0, 0.0)
red = (1.0, 0.0, 0.0)
blue = (0.0, 0.0, 1.0)
green = (0.0, 1.0, 0.0)

def rysujProstokat(x, y, a, b, d=0.0, wht=False):
    #x, y = lewy dolny wierzcholek

    #lg = lewy gorny, pd = prawy dolny
    #te wierzcholki sa wspoldzielone wiec niech maja ten sam kolor dla dobrego mieszania

    if d != 0.0:
        a*=d
        b*=d
    
    c_lg = white if wht else lg_color
    c_pd = white if wht else pd_color
    c_blk = white if wht else black

    glBegin(GL_TRIANGLES)
    glColor3f(*c_blk)
    glVertex2f(x, y) #ld
    glColor3f(*c_pd)
    glVertex2f(x+a, y) #pd
    glColor3f(*c_lg)
    glVertex2f(x, y+b) #lg
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(*c_pd)
    glVertex2f(x+a, y) #pd
    glColor3f(*c_blk)
    glVertex2f(x+a, y+b) #pg
    glColor3f(*c_lg)
    glVertex2f(x, y+b) #lg
    glEnd()


def rysujSierpinski(depth, x, y, a, b):
    if depth == 0:
        return

    w=a/3.0
    h=b/3.0

    #rysujProstokat(x+w, y+h, w, h, wht=True)
    rysujProstokat(x+w, y+h, w, h, wht=False)

    n_depth = depth - 1
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            rysujSierpinski(n_depth, x + i * w, y + j * h, w, h)



def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    
    #zadanie na 4.0
    #rysujProstokat(-150, -100, 300, 200)

    #zadanie na 4.5
    rysujSierpinski(4, -200, -100, 400, 200)

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    #modyfikacja: rzutnia rozszerza sie wraz z rozszerzeniem okna, 
    #nie powoduje deformacji ksztaltow.
    base_half_w = w_width/2.0
    base_half_h = w_height/2.0

    if width <= height:
        glOrtho(-base_half_w, base_half_w, 
                -base_half_w / aspect_ratio, base_half_w / aspect_ratio, 
                1.0, -1.0)
    else:
        glOrtho(-base_half_h * aspect_ratio, base_half_h * aspect_ratio, 
                -base_half_h, base_half_h, 
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
