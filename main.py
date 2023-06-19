import pygame
import sys
import os
import renderer as gui

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Play Particle Menu")

# Define button properties
button_width = 500
button_height = 80
button_padding = 20

# Define font
font = pygame.font.Font(None, 40)

# Define buttons
buttons = [
    {
        "text": "Brownian Playground",
        "path": "playground.py",
        "position": (WIDTH / 2, HEIGHT / 2 - button_height - button_padding)
    },
    {
        "text": "Temperature",
        "path": "heater.py",
        "position": (WIDTH / 2, HEIGHT / 2)
    },
    {
        "text": "Pressure",
        "path": "pressure.py",
        "position": (WIDTH / 2, HEIGHT / 2 + button_height + button_padding)
    },
    {
        "text": "Exit",
        "path": None,
        "position": (WIDTH / 2, HEIGHT / 2 + 2 * (button_height + button_padding))
    },
]

# Game loop
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				mouse_pos = pygame.mouse.get_pos()
				for button in buttons:
					button_rect = pygame.Rect(
						button["position"][0] - button_width / 2,
						button["position"][1] - button_height / 2,
						button_width,
						button_height,
					)
					if button_rect.collidepoint(mouse_pos):
						if button["path"] is None:
							running = False
							pygame.quit()
							sys.exit()
						else:
							os.system(f"python {button['path']}")

	# Clear the screen
	screen.fill((255,255,255))

	title = pygame.font.Font(None, 80)
	header = pygame.font.Font(None, 50)
	text = pygame.font.Font(None, 36)

	gui.draw_text("Welcome to Play Particle", title, (13, 59, 102), (960, 200))

	# Draw buttons
	for button in buttons:
		button_rect = pygame.Rect(
			button["position"][0] - button_width / 2,
			button["position"][1] - button_height / 2,
			button_width,
			button_height,
		)
		pygame.draw.rect(screen, (249, 87, 56), button_rect)
		text_surface = font.render(button["text"], True, (255,255,255))
		text_rect = text_surface.get_rect(center=button["position"])
		screen.blit(text_surface, text_rect)

	# Update the display
	pygame.display.flip()
