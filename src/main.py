""" 
This program simulates evolution through neuroevolution.

Creatures and food objects spawn randomly on a circle and creatures
will try to survive for as long as possible.
"""

import pyglet
from pyglet.window import key
from drawer import Drawer
from world import World


class MainWindow(pyglet.window.Window):
	"""
	MainWindow class contains all methods related to the wrapper window 
	including drawing frames and checking for keyboard and mouse inputs.
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
		"""Translates screen if dragging the mouse."""
		if button == pyglet.window.mouse.LEFT:
			pyglet.gl.glTranslatef(dx, dy, 0)

			
	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		"""Handles Zoom in and out with mouse wheel."""
		zoom_factor = 0.05
		if scroll_y == 1:
			pyglet.gl.glScalef(1 + zoom_factor, 1 + zoom_factor, 1)
		elif scroll_y == -1:
			pyglet.gl.glScalef(1 - zoom_factor, 1 -  zoom_factor, 1)

			
	def on_draw(self):
		"""Clears screen and calls for drawing of all objects in the 
		world.
		"""
		self.clear()
		world.draw()
		

if __name__ == '__main__':
	print("\nGame started\nPress Q to quit\n")

	MAP_LIMIT = 200		# Circular map radius limit
	MAX_NUMBER_OF_FOOD = 100
	MAX_NUMBER_OF_CREATURES = 2
	UPDATE_CAP = 1000	# Updates per second
	BG_COLOR = (0, 48 / 255, 14 / 255, 1)		# Background color

	drawer = Drawer()
	world = World(drawer, MAP_LIMIT, MAX_NUMBER_OF_FOOD, 
				  MAX_NUMBER_OF_CREATURES)
	window = MainWindow()

	# Set pyglet run and graphic settings
	pyglet.gl.glClearColor(*BG_COLOR)
	pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
	pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, 
						  pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
	pyglet.clock.schedule_interval(world.update, 1 / UPDATE_CAP)
	pyglet.gl.glTranslatef(200, 200 , 0)
	
	# Start program
	pyglet.app.run()