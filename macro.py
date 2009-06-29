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

Var = None
class Macro(object):
	__metaclass__ = MetaMacro
	__dont_touch__ = True

class StmtMacro(Macro):
	__dont_touch__ = True
	
	def matches(self, node):
		if node[0] != 'stmt' or len(self.syntax) > len(node)-1:
			return False
		
		for i in xrange(len(self.syntax)):
			elem = self.syntax[i]
			if elem != None and node[i+1] != elem:
				return False
		return True
	
	def transform(self, node):
		args = []
		for i in xrange(len(self.syntax)):
			elem = self.syntax[i]
			if elem == None:
				args.append(node[i+1])
		return self.stmt(*args)
