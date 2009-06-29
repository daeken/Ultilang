from macro import StmtMacro, Var

class Def(StmtMacro):
	stage = 100
	syntax = ('name', 'def'), Var, Var, Var
	
	def stmt(self, name, args, body):
		print 'Function definition:', name, args
		return None
