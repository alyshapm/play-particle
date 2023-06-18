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
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

pygame.display.set_caption('Play-Particle')

screen.fill(WHITE)

def drawwidgets(*items):
    for item in items:
        if type(item) == cmp.slider:
            pygame.draw.line(screen, (100,100,100), (int(item.x0) + OFFW, -int(item.y) + OFFH), (int(item.x1) + OFFW, -int(item.y) + OFFH), 8)
            pygame.draw.circle(screen, item.color, (int(item.x) + OFFW, -int(item.y) + OFFH), int(item.size))

def update(background = WHITE):
    pygame.display.update()
    screen.fill(background)

def drawpool(pool):
    for p in pool.particles:
        pygame.draw.circle(screen, p.color, (int(p.x) + OFFW, -int(p.y) + OFFH), int(p.r))

    for b in pool.obstacles:
        if type(b) == cmp.heatplate or type(b) == prt.piston:
            if b.axis == 1:
                pygame.draw.line(screen, b.color, (int(b.x0) + OFFW, -int(b.y) + OFFH), (int(b.x1) + OFFW, -int(b.y) + OFFH), 15)
            elif b.axis == 0:
                pygame.draw.line(screen, b.color, (int(b.x) + OFFW, -int(b.y0) + OFFH), (int(b.x) + OFFW, -int(b.y1) + OFFH), 4)

    pygame.draw.rect(screen, pool.cont.color, offsetrect(pool.cont, OFFW, OFFH), 2)

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
        b.draw(screen, (0, 0, 0))

def draw_text(text, font, color, pos):
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect.center = pos
	screen.blit(text_surface, text_rect)

def draw_bar(value):
	# Calculate the height of the bar based on the value
	max_height = HEIGHT - 250
	bar_height = int((value / 500) * max_height)
	bar_width = 20

	# Calculate the position of the bar
	bar_x = 1700
	bar_y = HEIGHT - 100 - bar_height

	# Draw the background
	pygame.draw.rect(screen, (200, 200, 200), (bar_x, 150, bar_width, max_height))

	# Draw the bar
	pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
