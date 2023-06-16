import math
from random import randint, uniform
from numpy import sign
import particles as prt

class obstacle:
	color = (0,0,0)
	updatable = False
	e = 1
	tag = None
	def collide(self, p, E):
		pass

class slider:
	def __init__(self, x, y, range, lenght, size):
		self.x0 = x - lenght / 2
		self.x1 = x + lenght / 2
		self.y = y
		self.x = self.x0
		self.value = 0
		self.start = range[0]
		self.end = range[1]
		self.range = range[1] - range[0]
		self.size = size
		self.color = (150,150,150)

	def update(self, mouse_pos, clicking):
		mx, my = mouse_pos
		# if colliding with mouse
		if self.x - self.size <= mx <= self.x + self.size and self.y - self.size <= my <= self.y + self.size:
			self.color = (200,200,200)
			if clicking:
				self.x = mx
				if self.x > self.x1:
					self.x = self.x1
				elif self.x < self.start + self.x0:
					self.x = self.start + self.x0
			self.value = (self.x - self.x0) / self.range
		else:
			self.color = (100,100,100)

class barrier(obstacle):
	def __init__(self, axis, x, y, l, tag = None):
		self.tag = tag
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
			print("invalid axis")

	def changelen(self, l):
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
				p.y += intersect * sign(p.yv)
				p.yv = - p.yv * E * self.e
		else:
			intersect = abs(p.x - self.x) - p.r
			if self.y0 < p.y < self.y1 and intersect < 0:
				p.x += intersect * sign(p.xv)
				p.xv = - p.xv * E * self.e

class heatplate(barrier):
	updatable = True
	def __init__(self, widget, axis, x, y, l, tag = None):
		super(heatplate, self).__init__(axis, x, y, l, tag)
		self.widget = widget
		self.e = 1
		self.color = (0,0,0)

	def update(self, _):
		self.e = self.widget.value * 2
		self.color = prt.getcolor(self.e * 3.75)

class _container(obstacle):
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