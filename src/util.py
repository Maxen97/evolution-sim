import math
import random

def distance(x1, y1, x2, y2):
	"""Returns distance between point (x1, y1) and (x2, y2)."""
	return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
	

def distanceLinePoint(x1, y1, x2, y2, x0, y0):
	"""Returns orthogonal distance from a point (x0, y0) and a straight
	line that intersects points (x1, y1) and (x2, y2).
	"""
	px = x2 - x1
	py = y2 - y1
	
	norm = px * px + py * py
	
	u = ((x0 - x1) * px + (y0 - y1) * py) / float(norm)
	
	if u > 1: u = 1
	elif u < 0: u = 0
	
	x = x1 + u * px
	y = y1 + u * py
	
	dx = x - x0
	dy = y - y0
	
	return math.sqrt(dx * dx + dy * dy)
	

def randomPointOnCircle(d):
	"""Returns a random point on a circle from a random angle and 
	distance from origin.

	Paramater d is the radius of the circle.
	"""
	angle = random.uniform(0, 2 * math.pi)
	rad = random.uniform(0, d)
	return (math.cos(angle) * rad, math.sin(angle) * rad)