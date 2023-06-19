import renderer as gui
import particles as prt
import pygame
import sys

# Creates first pool object
pool = prt.pool(e = 1, g = .05)
pool.setdomain(((-200, 500), (200, -500)))

mouse_pos = {'x':0, 'y':0}
draggable = prt.grabparticle(mouse_pos, 30)
pool.add(draggable)

# length = abs(500 - (-200))  # Calculate the length of the pool
# width = abs(200 - (-500))   # Calculate the width of the pool
# depth = 10                  # Assuming the depth of the pool is 10 units

# volume = length * width * depth

def store_mouse(pos):
	mouse_pos['x'] = pos[0]
	mouse_pos['y'] = pos[1]

piston = prt.piston(0, 500, 500, 400, 100)
pool.add(piston)
pool.random(100, 1, 15, rect = ((-200, 300), (200, -500)))

def merge():
	pool.setdomain(((-800,400), (800,-400)))
	piston.changelen(1600)
	pool.e = .99

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
			if event.key == pygame.K_SPACE:
				merge()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				click = True
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				click = False

	store_mouse(gui.truemouse(pygame.mouse.get_pos()))

	if click:
		piston.y = mouse_pos['y']
	
	pool.update()
	gui.drawpool(pool)

	# pressure = pool.pressure_accurate(pool.temperature_accurate(), volume)
	pressure = pool.pressure()

	title = pygame.font.Font(None, 80)
	header = pygame.font.Font(None, 50)
	text = pygame.font.Font(None, 36)

	gui.draw_text("Chamber Pressure", title, (13, 59, 102), (350, 440))
	gui.draw_text("Gas Simulator", title, (13, 59, 102), (350, 500))
	gui.draw_text("Watch how the pressure changes", text, (249, 87, 56), (350, 600))
	gui.draw_text("when the piston moves!", text, (249, 87, 56), (350, 630))

	gui.draw_text("Press the escape key to exit", text, (120, 120, 120), (350, 1020))

	gui.draw_text("Average Pressure*", text, (238, 150, 75), (1500, 520))
	gui.draw_text(str(pressure), header, (249, 87, 56), (1500, 560))
	gui.draw_bar(pressure)
	gui.draw_text("*Approximate, not to scale", text, (150, 150, 150), (1560, 1020))


	gui.update() # Updates screen