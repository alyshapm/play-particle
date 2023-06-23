import renderer as gui
import particles as prt
import pygame
import sys

# Creates the chamber object
chamber = prt.chamber(elasticity = 1, gravity = .05)
chamber.setdomain(((-200, 500), (200, -500)))

# Draggable Mouse
mouse_pos = {'x':0, 'y':0}
draggable = prt.grabparticle(mouse_pos, 30)
chamber.add(draggable)


# Volume for Boltzmann Calculation
# length = abs(500 - (-200))  # Calculate the length of the chamber
# width = abs(200 - (-500))   # Calculate the width of the chamber
# depth = 10                  # Assuming the depth of the chamber is 10 units

# volume = length * width * depth


# Stores mouse position for the draggable object
def store_mouse(pos):
	mouse_pos['x'] = pos[0]
	mouse_pos['y'] = pos[1]


# Initialize piston
piston = prt.piston(0, 500, 500, 400)

# Add piston to chamber
chamber.add(piston)

# Generate random particles in the chamber
chamber.random(100, 1, 15, rect = ((-200, 300), (200, -500)))


# Running Loop
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
			# Return to main menu
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				click = True
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				click = False

	# Store mouse position
	store_mouse(gui.truemouse(pygame.mouse.get_pos()))

	# Move piston according to y value of mouse (when dragging piston)
	if click:
		piston.y = mouse_pos['y']
	
	# Update the chamber accordingly
	chamber.update()
	gui.drawchamber(chamber)

	# Pressure inside the chamber
	# pressure = chamber.pressure_accurate(chamber.temperature_accurate(), volume)
	pressure = chamber.pressure()

	# Font Stylees for the Visualization
	title = pygame.font.Font(None, 80)
	header = pygame.font.Font(None, 50)
	text = pygame.font.Font(None, 36)

	# Title
	gui.draw_text("Chamber Pressure", title, (13, 59, 102), (350, 440))
	gui.draw_text("Gas Simulator", title, (13, 59, 102), (350, 500))

	# Description
	gui.draw_text("Watch how the pressure changes", text, (249, 87, 56), (350, 600))
	gui.draw_text("when the piston moves!", text, (249, 87, 56), (350, 630))

	# Instructions
	gui.draw_text("Press and hold your mouse", text, (238, 150, 75), (350, 800))
	gui.draw_text("to drag the piston", text, (238, 150, 75), (350, 830))

	# Escape Instructions
	gui.draw_text("Press the escape key to exit", text, (120, 120, 120), (350, 1020))

	# Average Pressure
	# Changes according to the pressure calculation in the chamber
	gui.draw_text("Average Pressure*", text, (238, 150, 75), (1500, 520))
	gui.draw_text(str(pressure), header, (249, 87, 56), (1500, 560))

	# Visualized Bar that represents the pressure changes
	gui.draw_bar(pressure)

	# Disclaimer
	gui.draw_text("*Approximate, not to scale", text, (150, 150, 150), (1560, 1020))

	# Updates sScreen
	gui.update() 