import renderer as gui
import particles as prt
import pygame
import sys

def set_solid_behavior(chamber):
	# Set particle behavior to solid/vibrating
	for p in chamber.particles:
		p.xv = 0
		p.yv = 0

# need revision
def set_gas_behavior(chamber):
	# Set particle behavior to gas/floating
	for p in chamber.particles:
		pass

# need revision
def set_liquid_behavior(chamber):
	# Set particle behavior to liquid
	for p in chamber.particles:
		# can make function in particles.py
		p.xv = 0
		p.yv = -1  # Example: Assign a constant downward velocity

# Creates first chamber object
chamber = prt.chamber(elasticity=0.99, gravity=0.01)
chamber.setdomain(((400, 200), (800, -200)))

# Creates second chamber object
chamber2 = prt.chamber(elasticity=1, gravity=0.001)
chamber2.setdomain(((-800, 200), (-400, -200)))

# Mouse
mouse_pos = {'x': 0, 'y': 0}
draggable = prt.grabparticle(mouse_pos, 30)
chamber.add(draggable)

# Initializes particles randomly
chamber.random(65, 5, 15)
chamber2.random(65, 20, 15)

# Needed for draggable particle
def store_mouse(pos):
	mouse_pos['x'] = pos[0]
	mouse_pos['y'] = pos[1]

chambers = [chamber, chamber2]

instruction = "Press the"
instruction2 = "Space Bar"
instruction3 = "to merge the containers!"

i = 0
while True:
	i += 1
	pygame.time.Clock().tick(144)
	# buttons = gui.drawbuttons()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		elif event.type == pygame.KEYDOWN:
			# Escape Key --> Quit
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

			# Space Bar --> Merge boxes
			if event.key == pygame.K_SPACE:
				if chamber2 in chambers:
					chamber.merge(chamber2)
					chamber.setdomain(((-800, 350), (800, -350)))
					chambers.remove(chamber2)
					chamber.elasticity = 0.9
					instruction = ""
					instruction2 = ""
					instruction3 = ""
					
					

		# elif event.type == pygame.MOUSEBUTTONDOWN:
		#     for button in buttons:
		#         if button.isOver(pygame.mouse.get_pos()):
		#             action = button.action
		#             print(f"{action} pressed")
		#             if action == 'CLEAR':
		#                 pass
		#             elif action == 'RANDOM':
		#                 pass
		#             elif action == 'ADD':
		#                 pass
		#             elif action == 'REMOVE':
		#                 pass

	store_mouse(gui.truemouse(pygame.mouse.get_pos()))

	title = pygame.font.Font(None, 80)
	header = pygame.font.Font(None, 50)
	text = pygame.font.Font(None, 36)
	subtitle = pygame.font.Font(None, 20)

	# Updates and renders all chambers
	for p in chambers:
		p.update()
		set_gas_behavior(p)
		gui.drawchamber(p)

	gui.draw_text("Brownian Playground", title, (13, 59, 102), (450, 150))
	gui.draw_text("Move your cursor to interact with the particles!", text, (249, 87, 56), (1480, 160))
	gui.draw_text("Press the escape key to exit", text, (120, 120, 120), (320, 1020))

	gui.draw_text("Slow", text, (1, 145, 195), (1260, 950))
	gui.draw_text("(Low Kinetic Energy)", subtitle, (1, 145, 195), (1260, 980))

	gui.draw_text("Fast", text, (209, 47, 45), (1760, 950))
	gui.draw_text("(High Kinetic Energy)", subtitle, (209, 47, 45), (1760, 980))
	
	gui.draw_gradient((1260, 1010, 500, 20), (0, 0, 255), (255, 0, 0))
	gui.draw_text("Particle Colour Legend", subtitle, (255,255,255), (1515, 1020))

	gui.draw_text(str(instruction), header, (249, 87, 56), (870, 520))
	gui.draw_text(str(instruction2), header, (13, 59, 102), (1040, 520))
	gui.draw_text(str(instruction3), header, (249, 87, 56), (960, 560))
	gui.update() # Updates screen