from re import A
import numpy as np

class Brain:
	def __init__(self, layer_sizes):
		"""Initializes a neural network with dimensions specified in the
		paramater layer_sizes.
		
		layer_sizes is in the form [params_in_layer_1, params_in_layer2, ...]
		"""
		weight_shapes = np.array([(a, b) for a, b in zip(layer_sizes[1:], layer_sizes[:-1])])
		self.weights = np.array([np.random.normal(0, 14, s) / s[1] ** 0.5 for s in weight_shapes])
		self.biases = np.array([np.ones((s, 1)) for s in layer_sizes[1:]])
		
	def forward(self, a):
		"""Forward pass. Parameter a is a n-sized vector with input
		values. 
		"""
		for w, b in zip(self.weights, self.biases):
			a = self.sigmoid(np.matmul(w, a) + b)
		return a
		
	@staticmethod
	def sigmoid(x):
		"""Sigmoid function. Used as activation function."""
		return 1 / (1 + np.exp(-x)) - 0.5