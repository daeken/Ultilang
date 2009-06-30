from macro import Macro, ExprMacro, StmtMacro, Var

class Def(StmtMacro):
	stage = 100
	syntax = ('name', 'def'), Var, Var, Var
	
	def transform(self, name, args, block):
		return ('def', name, ('args', ) + args[1:], block)

class When(StmtMacro):
	stage = 100
	syntax = ('name', 'when'), Var, Var
	
	def transform(self, cond, block):
		return ('when', cond, block)

class Unless(StmtMacro):
	stage = 100
	syntax = ('name', 'unless'), Var, Var
	
	def transform(self, cond, block):
		return ('when', ('not', cond), block)

class Call(Macro):
	stage = 150
	
	def matches(self, node):
		for i in xrange(1, len(node)-1):
			try:
				if node[i][0] == 'name' and node[i+1][0] == 'group':
					self.pos = i
					return True
			except:
				pass
		return False
	
	def transform(self, node):
		return node[:self.pos] + tuple((('call', node[self.pos], ) + node[self.pos+1][1:], )) + node[self.pos+2:]

class Add(ExprMacro):
	stage = 202
	syntax = Var, ('op', '+'), Var
	
	def transform(self, left, right):
		return ('+', left, right)

class Equals(ExprMacro):
	stage = 250
	syntax = Var, ('op', '=='), Var
	
	def transform(self, left, right):
		return ('==', left, right)

class Assign(ExprMacro):
	stage = 300
	syntax = Var, ('op', '='), Var
	
	def transform(self, left, right):
		return ('=', left, right)

class Yield(StmtMacro):
	stage = 400
	syntax = ('name', 'yield'), Var
	
	def transform(self, value):
		return ('yield', value)

class ReturnNone(StmtMacro):
	stage = 400
	syntax = ('name', 'return'), 
	
	def transform(self):
		return ('return', None)

class Return(StmtMacro):
	stage = 400
	syntax = ('name', 'return'), Var
	
	def transform(self, value):
		return ('return', value)

class Print(StmtMacro):
	stage = 400
	syntax = ('name', 'print'), Var
	
	def transform(self, value):
		return ('print', value)

class Cull(Macro):
	stage = 999
	
	def matches(self, node):
		if node[0] in ('expr', 'group', 'stmt') and len(node) == 2:
			return True
		return False
	
	def transform(Self, node):
		return node[1]
