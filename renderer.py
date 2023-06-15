import pygame, os
import time
import particles as prt

pygame.init()

WIDTH, HEIGHT = 1920, 1080
OFFW, OFFH = WIDTH//2, HEIGHT//2

WHITE = 255,255,255
os.environ['SDL_VIDEO_CENTERED'] = '1'
schermo = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

pygame.display.set_caption('particles')

schermo.fill(WHITE)

def update(background = WHITE):
	pygame.display.update()
	schermo.fill(background)

def drawpool(pool):
	for p in pool.particles:
		pygame.draw.circle(schermo, p.color, (int(p.x) + OFFW, -int(p.y) + OFFH), int(p.r))

	pygame.draw.rect(schermo, pool.cont.color, offsetrect(pool.cont, OFFW, OFFH), 2)

def offsetrect(rect, dx, dy):
	return (rect.x0 + dx, -rect.y0 + dy), (rect.x1 - rect.x0, -rect.y1 + rect.y0)

def truemouse(pos):
	return pos[0] - OFFW, pos[1] - OFFH