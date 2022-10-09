""" 
This program simulates evolution through neuroevolution.

Creatures and food objects spawn randomly on a circle and creatures
will try to survive for as long as possible.

By: Max Edin, 2022
"""

import pyglet
from pyglet.window import key
from drawer import Drawer
from world import World


class MainWindow(pyglet.window.Window):
	"""
	MainWindow class contains all methods related to the wrapper window 
	including drawing frames, updating objects, check for keyboard and 
	mouse innputs etc.
	"""

	def __init__(self):
		super().__init__(
			width=400, 
			height=400, 
			caption="Evolution simulator", 
			vsync=0, 
			resizable = True
			)
		
	def on_key_press(self, symbol, modifiers):
		if symbol == key.Q:
			pyglet.app.exit()
			self.close()
			print("Window closed.")

		""" # ONLY TO BE USED FOR TESTING
		elif symbol == key.A:
			creatures[0].ddirection = 0.1
		elif symbol == key.D:
			creatures[0].ddirection = -0.1
		elif symbol == key.W:
			creatures[0].thrust = 5
		elif symbol == key.S:
			creatures[0].thrust = -5
		elif symbol == key.E:
			creatures[0].eat = 1
		elif symbol == key.F:
			creatures[0].divide = True
		"""
			
	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		if button == pyglet.window.mouse.LEFT:
			pyglet.gl.glTranslatef(dx, dy, 0)
			
	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		zoom_factor = 0.05
		print(x, y)
		if scroll_y == 1:
			print("zoom in")
			pyglet.gl.glScalef(1 + zoom_factor, 1 + zoom_factor, 1)
		elif scroll_y == -1:
			print("zoom out")
			pyglet.gl.glScalef(1 - zoom_factor, 1 -  zoom_factor, 1)
			
	def on_draw(self):
		self.clear()
		world.draw()
		

if __name__ == '__main__':
	print(f"\nGame started\nPress Q to quit\n")

	drawer = Drawer()
	world = World(drawer)
	UPDATE_CAP = 100 #Updates per second
	map_radius = 200
	window = MainWindow()
	universe_color = (0, 48 / 255, 14 / 255, 1)

	bg = universe_color
	pyglet.gl.glClearColor(*bg)
	pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
	pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, 
						  pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
	#pyglet.clock.set_fps_limit(None)
	pyglet.clock.schedule_interval(world.update, 1 / UPDATE_CAP)
	pyglet.gl.glTranslatef(200, 200 , 0)
	pyglet.app.run()