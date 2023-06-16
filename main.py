import renderer as gui
import particles as prt
import pygame
import sys

def set_solid_behavior(pool):
    # Set particle behavior to solid/vibrating
    for p in pool.particles:
        p.xv = 0
        p.yv = 0

# need revision
def set_gas_behavior(pool):
    # Set particle behavior to gas/floating
    for p in pool.particles:
        pass

# need revision
def set_liquid_behavior(pool):
    # Set particle behavior to liquid
    for p in pool.particles:
        # can make function in particles.py
        p.xv = 0
        p.yv = -1  # Example: Assign a constant downward velocity

# Creates first pool object
pool = prt.pool(e=0.99, g=0.01)
pool.setdomain(((400, 200), (800, -200)))

# Creates second pool object
pool2 = prt.pool(e=1, g=0.001)
pool2.setdomain(((-800, 200), (-400, -200)))

# Mouse
mouse_pos = {'x': 0, 'y': 0}
draggable = prt.grabparticle(mouse_pos, 30)
pool.add(draggable)

# Initializes particles randomly
pool.random(60, 1, 15)
pool2.random(60, 20, 15)

# Needed for draggable particle
def store_mouse(pos):
    mouse_pos['x'] = pos[0]
    mouse_pos['y'] = pos[1]

pools = [pool, pool2]

i = 0
while True:
    i += 1
    pygame.time.Clock().tick(144)
    buttons = gui.drawbuttons()

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
                pool.merge(pool2)
                pool.setdomain(((-800, 400), (800, -400)))
                pools.remove(pool2)
                pool.e = 0.9

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.isOver(pygame.mouse.get_pos()):
                    action = button.action
                    print(f"{action} pressed")
                    if action == 'CLEAR':
                        pass
                    elif action == 'RANDOM':
                        pass
                    elif action == 'ADD':
                        pass
                    elif action == 'REMOVE':
                        pass

    store_mouse(gui.truemouse(pygame.mouse.get_pos()))

    # Updates and renders all pools
    for p in pools:
        p.update()
        print("pool temp: ", p.getmediantemp())   # Gets median 'temperature' (Velocity) of particles in pool
        set_gas_behavior(p)
        gui.drawpool(p)

    gui.update() # Updates screen