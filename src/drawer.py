import pyglet
from math import sin, cos, pi

class Drawer:
	def __init__(self):
		pass
	
	#POINT
	def point(self, x, y, color):
		pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ('v2f', (x, y)))
	
	#CIRCLE
	def circ(self, x, y, radius, color, quality):
		n = quality #NUMBER OF TRIANGLES; ~quality of circle
		delta_angle = 2 * pi / n
		angle = 0
		verts = [x,y]

		for i in range(n+1):
			temp_x = x + radius * cos(angle)
			temp_y = y + radius * sin(angle)
			angle += delta_angle
			verts.append(temp_x)
			verts.append(temp_y)
		v_list = pyglet.graphics.vertex_list(int(len(verts)/2), ('v2f',tuple(verts)), ('c4B', color*int(len(verts)/2)))
		v_list.draw(pyglet.gl.GL_TRIANGLE_FAN)
		
	#RECTANGLE
	def rect(self, x1, y1, width, height, color):
		vert_list = pyglet.graphics.vertex_list(4, ('v2f', (x1, y1, x1 + width, y1, x1 + width, y1 + height, x1, y1 + height) ), ('c4B', color * 4 ))
		vert_list.draw(pyglet.gl.GL_QUADS)

	#LINE
	def line(self, x0, y0, x1, y1, color):
		vert_list = pyglet.graphics.vertex_list(2, ('v2f', (x0,y0,x1,y1)),('c4B', color + color))
		vert_list.draw(pyglet.gl.GL_LINES)

	#GRAD_LINE
	def grad_line(self, x0, y0, x1, y1, color1, color2):
		vert_list = pyglet.graphics.vertex_list(2, ('v2f', (x0,y0,x1,y1)),('c4B', color1 + color2))
		vert_list.draw(pyglet.gl.GL_LINES)