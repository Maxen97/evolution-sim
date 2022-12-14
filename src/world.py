"""Module containig World and MapObject classes."""

import math
import random
import util
import brain as b
import numpy as np


class World:
	"""World object contains all creatures and food."""

	def __init__(self, drawer, MAP_LIMIT, MAX_NUMBER_OF_FOOD, 
				 MAX_NUMBER_OF_CREATURES):
		"""Initializes world and spawns starting creatures and food."""
		self.drawer = drawer
		self.MAP_LIMIT = MAP_LIMIT
		self.MAX_NUMBER_OF_FOOD = MAX_NUMBER_OF_FOOD
		self.MAX_NUMBER_OF_CREATURES = MAX_NUMBER_OF_CREATURES
		self.foods = []
		self.creatures = []

		# Spawn initial set of creatures and food
		for _ in range(MAX_NUMBER_OF_FOOD): self.spawn_food()
		for _ in range(MAX_NUMBER_OF_CREATURES): self.spawn_creature()


	def spawn_creature(self):
		"""Spawns a creature."""
		self.creatures.append(Creature(self.drawer, self))


	def spawn_food(self):
		"""Spawns a food."""
		self.foods.append(Food(self.drawer, self))


	def update(self, dt):
		"""Calls for update for all creatures and food in the world."""
		for food in self.foods: food.update()
		for creature in self.creatures: creature.update()


	def draw(self):
		"""Calls a draw call for all creatures and food in the world."""
		for food in self.foods: food.draw()
		for creature in self.creatures: creature.draw()


class MapObject:
	"""Wrapper of all objects visible in the world."""
	def __init__(self, drawer, world):
		self.drawer = drawer
		self.world = world
		self.x, self.y = util.randomPointOnCircle(self.world.MAP_LIMIT)
		

class Creature(MapObject):
	"""Creature object extending MapObject.
	Contains update, init, and draw methods.
	"""
	def __init__(self, drawer, world):
		self.size = 10 #also used as mass, i.e. size equivilant to mass
		self.xVel = 0
		self.yVel = 0
		self.reach = 10 #length that extends from size (actual reach = size + reach)
		self.sight = 80 #same direction as self.direction
		self.direction = random.uniform(0, 2 * math.pi)
		self.ddirection = 0 #d(direction)/dt
		self.thrust = 0
		self.friction = 0.95 #friction against floor, 0 to 1, NO FRICITION = 1
		self.energy = 100 #creature dies when energy reaches 0
		self.color = (random.randint(50,255),
			random.randint(50,255),
			random.randint(50,255),
			255)
		self.eat = 0
		self.divide = False
		self.object_in_sight = None
		inputs = ('color0', 'color1', 'color2', 'color3', 'sight distance')
		outputs = ('ddirection', 'thrust', 'eat')
		self.brain = b.Brain((len(inputs), 8, len(outputs)))
		super().__init__(drawer, world)
		

	def update(self):
		""" Updates collision and movement.
		"""

		objects_in_sight = []	# List of objects within sight

		# Placed outsite of loop for efficiency
		px = self.x + self.sight * math.cos(self.direction)
		py = self.y + self.sight * math.sin(self.direction)

		# Check collision between sight and food objects
		for food in self.world.foods:
			d = util.distanceLinePoint(self.x, self.y,
									   px, py,
									   food.x, food.y)
			
			if d < food.size: 
				objects_in_sight.append(food)
		
		closest_distance = np.inf
		self.object_in_sight = None
		#THIS CAN BE OPTIMIZED BY EVALUATING THIS IN LOOP ABOVE
		for object in objects_in_sight: 
			distance = util.distance(object.x, object.y, self.x, self.y) 
			if distance < closest_distance:
				closest_distance = distance
				self.object_in_sight = object

		if self.object_in_sight != None:
			self.object_in_sight.hit()
				
		#TODO update brain
		color = [0,0,0,0]
		distance = self.sight
		if self.object_in_sight == None:
			if util.distance(0,0,self.x+self.sight*math.cos(self.direction), self.y+self.sight*math.sin(self.direction)) < 200:
				color = [255, 255, 255, 255]
		else:
			color = self.object_in_sight.color
			distance = util.distance(self.x, self.y, self.object_in_sight.x, self.object_in_sight.y)
		#print(color)
		#print(distance)
		
		u = (self.brain.forward(np.array([[color[0]], [color[1]], [color[2]], [color[3]], [distance*6]])))
		self.ddirection, self.thrust, self.eat = u[0]/10, u[1], u[2]
		#print('ddir: ', u[0])
		#print('eat: ', self.eat)
		
		self.direction += self.ddirection
		self.xVel += math.cos(self.direction) * self.thrust / self.size
		self.yVel += math.sin(self.direction) * self.thrust / self.size
		self.xVel *= self.friction
		self.yVel *= self.friction
		self.x += self.xVel
		self.y += self.yVel
		
		self.energy -= abs(self.thrust)
		self.energy -= abs(self.ddirection)
		
		if self.eat >= 0.4:
			for food in self.world.foods:
				if util.distance(self.x, self.y, food.x, food.y) <= self.size + self.reach: #THIS CAN BE OPTIMIZED BY CALCULATING ONCE
					self.energy += food.size * 2
					self.world.foods.remove(food)
					self.world.spawn_food()
			self.energy -= 5
			#print("has eaten")
			#print("new energy: ", self.energy)
		
		if self.divide:
			#TODO divide code here
			pass
			
		self.eat = 0
		self.divide = False
		self.ddirection = 0
		self.thrust = 0
		
		if util.distance(self.x, self.y, 0, 0) > 200 or self.energy <= 0: #i.e. outside of map or no energy
			self.world.creatures.remove(self)
			self.world.spawn_creature()
		

	def draw(self):
		self.drawer.circ(self.x, self.y, self.size, self.color, 16)
		self.drawer.circ(self.x, self.y, self.size + self.reach, (self.color[0],self.color[1],self.color[2],60), 16)
		self.drawer.line(self.x, self.y,
			self.x + (self.sight) * math.cos(self.direction),
			self.y + (self.sight) * math.sin(self.direction),
			(255 - self.color[0], 255 - self.color[1], 255 - self.color[2], 255))


class Food(MapObject):
	"""Food object extending MapObject."""

	def __init__(self, drawer, world):
		"""Initializes food object."""
		self.size = random.uniform(3, 8)
		self.base_color = [55, 255, 120, 255]
		self.hit_color = [255, 0, 0, 255]
		self.color = self.base_color
		super().__init__(drawer, world)
		

	def update(self):
		self.color = self.base_color
	

	def hit(self):
		"""If food is seen by a create, the color will be changed."""
		self.color = self.hit_color
	

	def draw(self):
		self.drawer.circ(self.x, self.y, self.size, self.color, 16)
		