from parser import Parser

import macro
import coreMacros
import Backend.Python

class Compiler(object):
	def compile(self, code):
		code = Parser().parse(code)
		for stage in macro.stages:
			code = self.run(stage.macros, code)
	
	def run(self, macros, node):
		if not isinstance(node, tuple) and not isinstance(node, list):
			return node
		
		done = False
		while not done and :
			done = True
			for macro in macros:
				if macro.matches(node):
					node = macro.transform(node)
					done = False
					break
		
		return map(lambda node: self.run(macros, node), node)

if __name__=='__main__':
	import sys
	print Compiler().compile(file(sys.argv[1]).read())
