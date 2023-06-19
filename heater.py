import renderer as gui
import particles as prt
import components as cmp
import pygame
import sys


# Creates first pool object
pool = prt.pool(elasticity = .9, gravity = .05)
pool.setdomain(((-300, 500), (300, -500)))
pool.random(60, 1, 15, rect = ((-200, 300), (200, -500)))

# Creating slider
slider = cmp.slider(650,0,(0,100),200, 20)

# Adding heatplate to pool
pool.add(cmp.heatplate(slider,'x',  0, -500, 600))

click = False
i = 0
while True:
	i+= 1
	pygame.time.Clock().tick(144)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				click = True
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				click = False

	pool.update()
	gui.drawpool(pool)

	slider.update(gui.truemouse(pygame.mouse.get_pos()), click)
	gui.drawwidgets(slider)

	title = pygame.font.Font(None, 80)
	header = pygame.font.Font(None, 50)
	text = pygame.font.Font(None, 36)

	temperature = pool.temperature()

	gui.draw_text("Temperature", title, (13, 59, 102), (350, 510))
	gui.draw_text("Simulator", title, (13, 59, 102), (350, 560))

	gui.draw_text("Press the escape key to exit", text, (120, 120, 120), (350, 1020))

	gui.draw_text("Move the slider to", header, (238, 150, 75), (1600, 400))
	gui.draw_text("change the temperature", header, (238, 150, 75), (1600, 440))

	gui.draw_text("Cold", text, (1, 145, 195), (1500, 600))
	gui.draw_text("Hot", text, (209, 47, 45), (1710, 600))

	gui.draw_text("Temperature*", text, (238, 150, 75), (1600, 750))
	gui.draw_text(str(temperature), header, (249, 87, 56), (1600, 810))
	gui.draw_text("*Approximate, not to scale", text, (150, 150, 150), (1600, 1020))

	gui.update() # Updates screen