import math
from random import randint, uniform
from numpy import sign
import components as cmp

# e = collision elasticity --> how much kinetic energy is conserved in a collision
# g = gravity
# n = num of particles 
# v = maximum speed
# r = radius

class particle:
	def __init__(self, pos, vel, r, mass=1):
		self.x = pos[0]
		self.y = pos[1]
		self.xv = vel[0]
		self.yv = vel[1]
		self.r = r
		self.color = (255,0,0)
		self.container = None
		self.mass = mass

	# Update particles 
	def update(self, G):
		self.yv -= G
		self.x += self.xv
		self.y += self.yv
		self.speed = math.sqrt(self.xv**2 + self.yv**2)
		self.color = getcolor(self.speed)

	def collide(self, body, E):
		dx, dy = self.x - body.x, self.y - body.y
		d = math.sqrt(dx**2 + dy**2)

		if d < self.r + body.r:
			dvx, dvy = self.xv - body.xv, self.yv - body.yv
			sin, cos = dx/d, dy/d 
			dr = (self.r + body.r - d) / 2
			dx2, dy2 = sin * dr, cos * dr

			self.x += dx2
			self.y += dy2
			body.x -= dx2
			body.y -= dy2

			h = (dx * dvx + dy * dvy) / d
			new_dvx, new_dvy = -h * sin * E, -h * cos * E

			self.xv += new_dvx
			self.yv += new_dvy
			body.xv -= new_dvx
			body.yv -= new_dvy

class grabparticle(particle):
	def __init__(self, mouse, r):
		super(grabparticle, self).__init__((0,0), (0,0), r)
		self.mouse = mouse
		self.color = (100,100,255)
		self.speed = 1

	def confine(self, piston):
		if self.x < piston.x0:
			self.x = piston.x0
		elif self.x > piston.x1:
			self.x = piston.x1
		if self.y < piston.y0:
			self.y = piston.y0
		elif self.y > piston.y1:
			self.y = piston.y1

	def update(self, G):
		self.xv = self.mouse['x'] - self.x
		self.yv = -self.mouse['y'] - self.y
		self.x += self.xv
		self.y += self.yv
		if isinstance(self.container, piston):
			self.confine(self.container)

def clamp(n, min, max):
	if min < n < max:
		return n
	elif n >= max:
		return max
	else:
		return min

# Get RGB colours for the particle colours
def getrgb(factor, color_1, color_2):
	return tuple([c2*factor + c1*(1-factor) for c1, c2 in zip(color_1, color_2)])

# Get colours based on the speed
def getcolor(speed):
	return getrgb(clamp(speed/15, 0, 1), (0,0,255), (255,0,0))

class obstacle:
	color = (0,0,0)
	updatable = False
	e = 1
	def collide(self, p, E):
		pass

class container(obstacle):
	def __init__(self, rect):
		self.rect = rect
		self.x0 = rect[0][0]
		self.y0 = rect[0][1]
		self.x1 = rect[1][0]
		self.y1 = rect[1][1]

	def collide(self, p, E):
		if p.y + p.r > self.y0:
			p.y -= p.r + p.y - self.y0
			p.yv = -p.yv * E
		elif p.y - p.r < self.y1:
			p.y += p.r - p.y + self.y1
			p.yv = -p.yv * E
		if p.x + p.r > self.x1:
			p.x -= p.r + p.x - self.x1
			p.xv = -p.xv * E
		elif p.x - p.r < self.x0:
			p.x += p.r - p.x + self.x0
			p.xv = -p.xv * E

class piston(obstacle):
	updatable = True
	def __init__(self, x, y, l, mass, axis = 1):
		self.v = 0
		self.mass = mass
		if axis == 1 or axis == 'x':
			self.axis = 1
			self.y = y
			self.x_ = x
			self.x0 = x - l/2
			self.x1 = x + l/2
		elif axis == 0 or axis == 'y':
			self.axis = 0
			self.x = x
			self.y_ = y
			self.y0 = y - l/2
			self.y1 = y + l/2
		else:
			print("Invalid Axis")

	def update(self, gravity):
		if self.axis == 1:
			self.v -= gravity
			self.y += self.v
		else:
			self.y += self.v

	def change_length(self, l):
		if self.axis == 1:
			self.x0 = self.x_ - l/2
			self.x1 = self.x_ + l/2
		else:
			self.y0 = self.y_ - l/2
			self.y1 = self.y_ + l/2

	def collide(self, p, E):
		if self.axis == 1:
			intersect = abs(p.y - self.y) - p.r
			if self.x0 < p.x < self.x1 and intersect < 0:
				p.y += intersect
				dv = (self.v - p.yv) *2 
				self.v -= dv / (1 + self.mass)
				p.yv += (dv * self.mass) / (1 + self.mass)

		else:
			intersect = abs(p.x - self.x) - p.r
			if self.y0 < p.y < self.y1 and intersect < 0:
				p.x += intersect * sign(p.xv)
				p.xv = - p.xv * E * self.elasticity

class pool:
	def __init__(self, elasticity = 1, gravity = 0, *particles):
		self.particles = []
		self.obstacles = []
		self.updatables = []
		self.cont = container(((-10000,10000), (10000,-10000)))
		self.elasticity, self.gravity = elasticity, gravity
		for p in particles:
			self.add(p)

	def add(self, body):
		if type(body) == cmp.heatplate or type(body) == piston:
			self.obstacles.append(body)
			if body.updatable == True:
				self.updatables.append(body)
		elif issubclass(type(body), particle):
			self.particles.append(body)
			self.updatables.append(body)

	def merge(self, pool2):
		self.particles += pool2.particles
		self.obstacles += pool2.obstacles
		self.updatables += pool2.updatables

	def update(self):
		elasticity = self.elasticity *.5 + .5
		for body in self.updatables:
			body.update(self.gravity)
		for i, p in enumerate(self.particles):
			for p2 in self.particles[i+1:]:
				p.collide(p2, elasticity)

			for b in self.obstacles:
				b.collide(p, elasticity)
			self.cont.collide(p, elasticity)

	def setdomain(self, rect):
		self.cont = container(rect)
	

	# Uses PV = nRT
	# P --> pressure of the gas,
	# V --> volume of the gas chamber,
	# n 0--> number of moles of gas particles,
	# R --> ideal gas constant (Boltzmann)
	# T --> temperature in Kelvin
	# Number is not ideal, cannot represent pressure well as it is too small
	def pressure_accurate(self, temperature, volume):
		Boltzmann_constant = 1.38e-23  # Boltzmann constant in J/K

		total_speed_squared = 0
		for particle in self.particles:
			total_speed_squared += particle.speed**2

		average_speed_squared = total_speed_squared / len(self.particles)
		kinetic_energy = (1 / 2) * average_speed_squared * particle.mass

		number_of_particles = len(self.particles)
		pressure = (number_of_particles * kinetic_energy) / (volume * Boltzmann_constant * temperature)

		return pressure

	# Focuses on average speed of the gas particles
	# Calculates the square of that speed --> approximation of pressure
	# Not as accurate as it doesn't take in volume and temperature
	def pressure(self):
		total_speed = 0
		for p in self.particles:
			total_speed += p.speed
		try:
			average_speed = total_speed / len(self.particles)
			return round(average_speed ** 2, 1)
		except ZeroDivisionError:
			print("Pool is empty, pressure cannot be calculated.")
			return 0


	# More accurate temperature recording
	# Uses Boltzmann constant
	def temperature_accurate(self):
		Boltzmann_constant = 1.38e-23  # Boltzmann constant in J/K

		total_speed_squared = 0
		for particle in self.particles:
			total_speed_squared += particle.speed**2

		average_speed_squared = total_speed_squared / len(self.particles)
		average_kinetic_energy = (1 / 2) * average_speed_squared * particle.mass

		temperature = (2 * average_kinetic_energy) / (3 * Boltzmann_constant)

		return temperature
	
	# Get temperature in chamber
	# Not as accurate but easier to digest
	def temperature(self):
		t = 0
		for p in self.particles:
			t += p.speed
		try:
			t /= len(self.particles)
			return round(t, 1)
		except ZeroDivisionError:
			print("Pool is empty, cannot get temperature.")

	# Generate random particles in the pool
	def random(self, n, v, r, rect = None):
		if rect is None:
			rect = self.cont.rect
			print(rect)
		for _ in range(n):
			p = particle((randint(rect[0][0], rect[1][0]), randint(rect[1][1], rect[0][1])), (uniform(-v, v), uniform(-v, v)), r)
			self.add(p)

# Merge the pools into one
def mergepools(*pools, elasticity = False, gravity = False):
	if not elasticity:
		elasticity = pools[0].elasticity
	if not gravity:
		gravity = pools[0].gravity
	newpool = pool(elasticity = elasticity, gravity = gravity)
	for p in pools:
		newpool.particles += p.particles
		newpool.obstacles += p.obstacles
		newpool.updatables += p.updatables
	return newpool