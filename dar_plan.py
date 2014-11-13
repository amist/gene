from random import randint

class DarPlan:
	def __init__(self):
		self.gene = []
		
	def get_random_gene(self):
		id = randint(0, 1000)
		taxi = randint(0, 5)
		pickup_time = randint(1, 1000)
		stay_time = randint(1, 100)
		in_taxi = True if randint(0, 1) == 0 else False
		gene = [id, taxi, pickup_time, stay_time, in_taxi]
		return gene
		
	def get_child(self):
		raise NotImplementedError
		
	def get_fitness_value(self):
		raise NotImplementedError