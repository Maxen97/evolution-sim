import numpy as np

class Brain:
	def __init__(self, layer_sizes):
		weight_shapes = [(a,b) for a,b in zip(layer_sizes[1:], layer_sizes[:-1])]
		self.weights = [np.random.normal(0, 14, s)/s[1]**0.5 for s in weight_shapes] #TESTA ATT TA BORT /s[1]**0.5
		self.biases = [np.ones((s,1)) for s in layer_sizes[1:]]
		#for w in self.weights:
		#	print(w, '\n')
		
	def run(self, a):
		for w,b in zip(self.weights, self.biases):
			a = self.activation(np.matmul(w,a) + b)
		return a
		
	@staticmethod
	def activation(x):
		return 1/(1+np.exp(-x)) - 0.5