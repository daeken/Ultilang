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
	
	def __transform__(self, node):
		return self.transform(node)

class SyntaxMacro(Macro):
	__dont_touch__ = True
	
	def matches(self, node):
		if len(self.syntax) != len(node):
			return False
		
		for i in xrange(len(self.syntax)):
			elem = self.syntax[i]
			if elem != None and node[i] != elem:
				return False
		return True
	
	def __transform__(self, node):
		args = []
		for i in xrange(len(self.syntax)):
			elem = self.syntax[i]
			if elem == None:
				args.append(node[i])
		return self.transform(*args)

class StmtMacro(SyntaxMacro):
	__dont_touch__ = True
	
	def matches(self, node):
		if node[0] != 'stmt':
			return False
		return SyntaxMacro.matches(self, node[1:])
	
	def __transform__(self, node):
		return SyntaxMacro.__transform__(self, node[1:])

class ExprMacro(Macro):
	__dont_touch__ = True
	
	def matches(self, node):
		if len(self.syntax) > len(node)-1:
			return False
		
		for i in xrange(len(node)-len(self.syntax)):
			match = True
			for j in xrange(len(self.syntax)):
				elem = self.syntax[j]
				if elem != None and node[1+i+j] != elem:
					match = False
					break
			if match:
				self.pos = i
				return True
		return False
	
	def __transform__(self, node):
		args = []
		for i in xrange(len(self.syntax)):
			elem = self.syntax[i]
			if elem == None:
				args.append(node[self.pos+i+1])
		return tuple(node[:self.pos+1] + (self.transform(*args), ) + node[self.pos+len(self.syntax)+1:])
