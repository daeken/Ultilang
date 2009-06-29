class Stages(object):
	def __init__(self):
		self.stages = {}
	
	def __iter__(self):
		for stage in sorted(self.stages.keys()):
			yield self.stages[stage]
	
	def add(self, stage, macro):
		if stage not in self.stages:
			self.stages[stage] = []
		self.stages[stage].append(macro())
stages = Stages()

class MetaMacro(type):
	def __new__(cls, name, bases, body):
		if '__dont_touch__' in body:
			del body['__dont_touch__']
			return type.__new__(cls, name, bases, body)
		
		macro = type.__new__(cls, name, bases, body)
		stages.add(body['stage'], macro)
		return macro

class Macro(object):
	__metaclass__ = MetaMacro
	__dont_touch__ = True
