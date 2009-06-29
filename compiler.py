from parse import Parser

import macro
#import coreMacros
#import Backend.Python

def isiterable(obj):
	if isinstance(obj, tuple) or isinstance(obj, list):
		return True
	else:
		return False

class Compiler(object):
	def compile(self, code):
		code = Parser().parse(code)
		for macros in macro.stages:
			code = self.run(macros, code)
		return code
	
	def run(self, macros, node):
		if not isiterable(node):
			return node
		
		done = False
		while not done and isiterable(node):
			done = True
			for macro in macros:
				if macro.matches(node):
					node = macro.transform(node)
					done = False
					break
		
		if isiterable(node):
			return map(lambda node: self.run(macros, node), node)
		else:
			return node

if __name__=='__main__':
	import pprint, sys
	pprint.pprint(Compiler().compile(file(sys.argv[1]).read()))
