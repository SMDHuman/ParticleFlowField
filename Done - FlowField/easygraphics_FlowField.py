from opensimplex import OpenSimplex
from numpy import interp
from easygraphics import *
from random import randint
import time
import math

os = OpenSimplex(randint(0, 1000))

class Particles():
	def __init__(self):
		self.pos = [randint(0, xwin * scl) / scl, randint(0, ywin * scl) / scl]
		self.vel = [0, 0]
		self.acc = [0, 0]

	def update(self):
		self.pos[0] += self.vel[0] * dtime
		self.pos[1] += self.vel[1] * dtime
		self.vel[0] += self.acc[0] * dtime
		self.vel[1] += self.acc[1] * dtime

		speedLimit = 2

		if(self.vel[0] > speedLimit): self.vel[0] = speedLimit
		if(self.vel[1] > speedLimit): self.vel[1] = speedLimit

		if(self.vel[0] < -speedLimit): self.vel[0] = -speedLimit
		if(self.vel[1] < -speedLimit): self.vel[1] = -speedLimit

		if(self.pos[0] >= xwin): self.pos[0] = 0
		if(self.pos[0] < 0): self.pos[0] = xwin - 0.1
		if(self.pos[1] >= ywin): self.pos[1] = 0
		if(self.pos[1] < 0): self.pos[1] = ywin - 0.1

	def addForce(self, force):
		self.acc[0] = force[0]
		self.acc[1] = force[1]

	def draw(self):
		r = 0.1
		set_fill_color("black")
		fill_ellipse(self.pos[0], self.pos[1], r, r)

	def drawdot(self):
		colord = 1
		color = get_pixel(self.pos[0] * scl, self.pos[1] * scl).red() - colord
		if(color >= 255): color = 255
		put_pixel(self.pos[0] * scl, self.pos[1] * scl, color_rgb(color, color, color))

def sin(deg):
    deg %= 360
    if(deg < 0):
        deg += 360
    if(deg > 90):
        deg = 180 - deg
    elif(deg > 180):
        deg += 180
    return(math.sin(math.radians(deg)))

def cos(deg):
    deg %= 360
    if(deg < 0):
        deg += 360
    if(deg == 90 or deg == 270):
        return(0)
    elif(deg > 180):
        deg = 180 - (deg - 180)
    return(math.cos(math.radians(deg)))

def drawVector(coords, n):
	deg = int(interp(n, [-1, 1], [-360, 360]))
	line(coords[0] + 0.5, coords[1] + 0.5, coords[0] + 0.5 + cos(deg) /2, coords[1] + 0.5 + sin(deg)/2)

def getVector(n):
	mg = 2
	deg = int(interp(n, [-1, 1], [-360, 360]))
	return((cos(deg) * mg, sin(deg) * mg))

def main():
	global xwin, ywin, scl, dtime
	scl = 10

	init_graph(600, 600)
	set_render_mode(1)
	set_background_color("white")
	scale(scl, scl)

	xwin = int(get_width() / scl)
	ywin = int(get_height() / scl)

	parts = []
	for i in range(500):
		parts.append(Particles())

	osMap = []
	for y in range(ywin):
		osMap.append([0] * xwin)

	increase = 0.1
	zoff = 0
	dtime = 0

	while is_run():
		if(delay_fps(120)):
			ctime = time.time()
			clear_device()
			yoff = 0
			for y in range(ywin):
				xoff = 0
				for x in range(xwin):
					#rgb = int(interp(os.noise3d(xoff, yoff, zoff), [-1, 1], [0, 255]))
					#color = color_rgb(rgb, rgb, rgb)
					#r = Rectangle(Point(x, y), Point(x + 1, y + 1))
					#r.setFill(color)
					#r.draw(win)

					osMap[y][x] = os.noise3d(xoff, yoff, zoff)
					set_color("grey")
					
					drawVector((x, y), osMap[y][x])

					xoff += increase
				yoff += increase
			zoff += 0.003

			for part in parts:
				part.update()
				force = getVector(osMap[int(part.pos[1])][int(part.pos[0])])
				part.addForce(force)
				part.draw()
			dtime = time.time() - ctime
	close_graph()


easy_run(main)