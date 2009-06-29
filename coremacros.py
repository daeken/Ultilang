from macro import ExprMacro, StmtMacro, Var

class Assign(ExprMacro):
	stage = 500
	syntax = Var, ('op', '='), Var
	
	def transform(self, left, right):
		return ('=', left, right)

class Equals(ExprMacro):
	stage = 200
	syntax = Var, ('op', '=='), Var
	
	def transform(self, left, right):
		return ('==', left, right)

class Add(ExprMacro):
	stage = 200
	syntax = Var, ('op', '+'), Var
	
	def transform(self, left, right):
		return ('+', left, right)

class Def(StmtMacro):
	stage = 500
	syntax = ('name', 'def'), Var, Var, Var
	
	def transform(self, name, args, block):
		return ('def', name, args, block)

class When(StmtMacro):
	stage = 500
	syntax = ('name', 'when'), Var, Var
	
	def transform(self, cond, block):
		return ('when', cond, block)

class Yield(StmtMacro):
	stage = 500
	syntax = ('name', 'yield'), Var
	
	def transform(self, value):
		return ('yield', value)
