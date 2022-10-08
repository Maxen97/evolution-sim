import pyglet
from pyglet.window import key
import math
import random
import time
import Drawer
import mapobjects
import util

class MainWindow(pyglet.window.Window):
	def __init__(self):
		super().__init__(width=window_dimension[0], height=window_dimension[1], caption="Main", vsync=0, resizable = True)
		
	def on_key_press(self, symbol, modifiers):
		if symbol == key.Q:
			pyglet.app.exit()
			self.close()
			print("Window closed.")
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
			
	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		if button == pyglet.window.mouse.LEFT:
			pyglet.gl.glTranslatef(dx, dy , 0)
			
	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		print(x, y)
		if scroll_y == 1:
			print("zoom in")
			pyglet.gl.glScalef(1 + zoom_factor, 1 + zoom_factor, 1)
		elif scroll_y == -1:
			print("zoom out")
			pyglet.gl.glScalef(1 - zoom_factor, 1 -  zoom_factor, 1)
			
	def on_draw(self):
		self.clear()
		drawer.circ(0, 0, 200, (255,255,255,255), 32)
		for food in foods:
			food.draw()
			
		for creature in creatures:
			creature.draw()
		#print("on_draw was called")

def init():
	number_of_foods = 50
	number_of_creatures = 1
	for i in range(0, number_of_foods):
		foods.append(mapobjects.Food(drawer))
		
	for i in range(0, number_of_creatures):
		creatures.append(mapobjects.Creature(drawer))
		
def update(dt):
	global last_time
	last_time += dt
	
	for i in foods:
		i.update()
		
	for i in creatures:
		i.update(foods, creatures)
		

if __name__ == '__main__':
	last_time = 0
	UPDATE_CAP = 100 #Updates per second
	window_dimension = (400, 400)
	map_radius = 200
	window = MainWindow()
	drawer = Drawer.Drawer()
	zoom_factor = 0.05
	foods = []
	creatures = []
	universe_color = (0, 48 / 255, 14 / 255, 1)
	universe_color = (0,0,0,0)
	
	init()
	
	bg = universe_color
	pyglet.gl.glClearColor(*bg)
	pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
	pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
	pyglet.clock.set_fps_limit(None)
	pyglet.clock.schedule_interval(update, 1 / UPDATE_CAP)
	pyglet.gl.glTranslatef(200, 200 , 0)
	pyglet.app.run()