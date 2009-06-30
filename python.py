from macro import Macro, SyntaxMacro, Var
import compiler.ast

class Def(SyntaxMacro):
	stage = 1000
	syntax = 'def', Var, Var, Var
	
	def transform(self, name, args, block):
		argnames = []
		defaults = []
		for arg in args[1:]:
			if arg[0] == '=':
				argnames.append(arg[1][1])
				defaults.append(arg[2])
			else:
				argnames.append(arg[1])
		
		return ('Function', 
				None, 
				('str', name[1]), 
				('tuple', ) + tuple(('str', arg) for arg in argnames), 
				('tuple', ) + tuple(defaults), 
				('const', 0), None, 
				block
			)

class Print(SyntaxMacro):
	stage = 1000
	syntax = 'print', Var
	
	def transform(self, value):
		return ('Printnl', ('tuple', value), None)

class Add(SyntaxMacro):
	stage = 1000
	syntax = '+', Var, Var
	
	def transform(self, left, right):
		return ('Add', ('tuple', left, right))

class Not(SyntaxMacro):
	stage = 1200
	syntax = 'not', Var
	
	def transform(self, value):
		return ('Not', value)

class Name(SyntaxMacro):
	stage = 1100
	syntax = 'name', Var
	
	def transform(self, name):
		return ('Name', ('str', name))

class Call(Macro):
	stage = 1200
	
	def matches(self, node):
		return node[0] == 'call'
	
	def transform(self, node):
		return ('CallFunc', 
				node[1], 
				('tuple', ) + node[2:], 
				None, None
			)

class Return(SyntaxMacro):
	stage = 1250
	syntax = 'return', Var
	
	def transform(self, value):
		if value == None:
			return ('Return', ('Const', None))
		else:
			return ('Return', value)

class When(SyntaxMacro):
	stage = 1250
	syntax = 'when', Var, Var
	
	def transform(self, cond, block):
		return ('If', 
				('tuple', 
					('tuple', cond, block)), 
				None
			)

class Equals(SyntaxMacro):
	stage = 1300
	syntax = '==', Var, Var
	
	def transform(self, left, right):
		return ('Compare', left, ('tuple', ('tuple', ('str', '=='), right)))

class Block(Macro):
	stage = 1300
	
	def matches(self, node):
		return node[0] == 'block'
	
	def transform(self, node):
		return ('Stmt', ('tuple', ) + node[1:])

class BuildAST(Macro):
	stage = 1999
	
	def matches(self, node):
		self.first = True
		return True
	
	def transform(self, node):
		first = self.first
		self.first = False
		
		if node == None:
			return None
		elif isinstance(node, int):
			return compiler.ast.Const(node)
		elif node[0] == 'str':
			return node[1]
		elif node[0] == 'const':
			return node[1]
		elif node[0] == 'tuple':
			return map(self.transform, node[1:])
		
		func = getattr(compiler.ast, node[0])
		code = func(*map(self.transform, node[1:]))
		
		if first:
			return compiler.ast.Module(None, code)
		else:
			return code
