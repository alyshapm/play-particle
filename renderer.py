import pygame, os
import time
import particles as prt
import components as cmp
from button import *

pygame.init()

WIDTH, HEIGHT = 1920, 1080
OFFW, OFFH = WIDTH//2, HEIGHT//2

WHITE = 255,255,255
os.environ['SDL_VIDEO_CENTERED'] = '1'
schermo = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

pygame.display.set_caption('particles')

schermo.fill(WHITE)

def drawwidgets(*items):
    for item in items:
        if type(item) == cmp.slider:
            pygame.draw.line(schermo, (100,100,100), (int(item.x0) + OFFW, -int(item.y) + OFFH), (int(item.x1) + OFFW, -int(item.y) + OFFH), 8)
            pygame.draw.circle(schermo, item.color, (int(item.x) + OFFW, -int(item.y) + OFFH), int(item.size))

def update(background = WHITE):
    pygame.display.update()
    schermo.fill(background)

def drawpool(pool):
    for p in pool.particles:
        pygame.draw.circle(schermo, p.color, (int(p.x) + OFFW, -int(p.y) + OFFH), int(p.r))

    for b in pool.obstacles:
        if type(b) == cmp.heatplate or type(b) == prt.piston:
            if b.axis == 1:
                pygame.draw.line(schermo, b.color, (int(b.x0) + OFFW, -int(b.y) + OFFH), (int(b.x1) + OFFW, -int(b.y) + OFFH), 15)
            elif b.axis == 0:
                pygame.draw.line(schermo, b.color, (int(b.x) + OFFW, -int(b.y0) + OFFH), (int(b.x) + OFFW, -int(b.y1) + OFFH), 4)

    pygame.draw.rect(schermo, pool.cont.color, offsetrect(pool.cont, OFFW, OFFH), 2)

def offsetrect(rect, dx, dy):
    return (rect.x0 + dx, -rect.y0 + dy), (rect.x1 - rect.x0, -rect.y1 + rect.y0)

def truemouse(pos):
    return pos[0] - OFFW, pos[1] - OFFH

def drawbuttons():
    clear_button = button(WIDTH//2 - 315, 1045, 140, 50, 'CLEAR', 'CLEAR')
    add_button = button(WIDTH//2 - 115, 1045, 140, 50, 'ADD', 'ADD')
    remove_button = button(WIDTH//2 + 85, 1045, 140, 50, 'REMOVE', 'REMOVE')
    random_button = button(WIDTH//2 + 285, 1045, 140, 50, 'RANDOM', 'RANDOM')

    buttons = [clear_button, random_button, add_button, remove_button]
    
    for b in buttons:
        b.draw(schermo, (0, 0, 0))
