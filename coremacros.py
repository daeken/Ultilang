from macro import Macro, ExprMacro, StmtMacro, Var

class Assign(ExprMacro):
	stage = 200
	syntax = Var, ('op', '='), Var
	
	def transform(self, left, right):
		return ('=', left, right)

class Equals(ExprMacro):
	stage = 150
	syntax = Var, ('op', '=='), Var
	
	def transform(self, left, right):
		return ('==', left, right)

class Add(ExprMacro):
	stage = 103
	syntax = Var, ('op', '+'), Var
	
	def transform(self, left, right):
		return ('+', left, right)

class Def(StmtMacro):
	stage = 300
	syntax = ('name', 'def'), Var, Var, Var
	
	def transform(self, name, args, block):
		return ('def', name, args, block)

class When(StmtMacro):
	stage = 300
	syntax = ('name', 'when'), Var, Var
	
	def transform(self, cond, block):
		return ('when', cond, block)

class Yield(StmtMacro):
	stage = 300
	syntax = ('name', 'yield'), Var
	
	def transform(self, value):
		return ('yield', value)

class Return(StmtMacro):
	stage = 300
	syntax = ('name', 'return'), Var
	
	def transform(self, value):
		return ('return', value)

class Print(StmtMacro):
	stage = 300
	syntax = ('name', 'print'), Var
	
	def transform(self, value):
		return ('print', value)

class Call(Macro):
	stage = 300
	
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
		return node[:self.pos] + tuple(((node[self.pos][1], ) + node[self.pos+1][1:], )) + node[self.pos+2:]

class Cull(Macro):
	stage = 1000
	
	def matches(self, node):
		if node[0] in ('expr', 'group', 'stmt') and len(node) == 2:
			return True
		return False
	
	def transform(Self, node):
		return node[1]
