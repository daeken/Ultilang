import re

class BuildTokenizer(type):
	def __new__(cls, name, bases, body):
		if '__dont_touch__' in body:
			del body['__dont_touch__']
			return type.__new__(cls, name, bases, body)
		body = {
				'__module__' : body['__module__'], 
				'tokens' : dict((name, BuildTokenizer.compile(value)) for name, value in body.items() if name != '__module__')
			}
		return type.__new__(cls, name, bases, body)
	
	@staticmethod
	def compile(value):
		if isinstance(value, str):
			return re.compile(value, re.M)
		else:
			return value

class Tokenizer(object):
	__metaclass__ = BuildTokenizer
	__dont_touch__ = True
	ws = re.compile('[ \t]+')
	def tokenize(self, code):
		while len(code):
			match = self.ws.match(code)
			if match != None:
				code = code[len(match.group(0)):]
				continue
			found = False
			for name, re in self.tokens.items():
				match = re.match(code)
				if match != None:
					groups = match.groups()
					if len(groups) == 0:
						yield name, (match.group(0), )
					else:
						yield name, groups
					code = code[len(match.group(0)):]
					found = True
					break
			if not found:
				print 'Could not tokenize'
				break

class UltiTokenizer(Tokenizer):
	comment = r'#(.*)$'
	name = r'([a-zA-Z_][a-zA-Z0-9_]*)'
	newline = r'[\r\n]+'
	suppressedNewline = r'\\\n'
	semicolon = r';'
	comma = r','
	op = r'([~!$%\^&*-+=./?:<>]+)'
	number = r'(0x[0-9a-fA-F]+|0o[0-7]+|[0-9]+\.[0-9]+|[0-9]+)([fFdDlL]*)'
	openParen = r'\('
	closeParen = r'\)'
	openBrace = r'\{'
	closeBrace = r'\}'
	openBracket = r'\['
	closeBracket = r'\]'

class Parser(object):
	def parse(self, code):
		self.cur = ['block']
		self.stack = []
		self.push('stmt')
		self.semi = None
		for name, args in UltiTokenizer().tokenize(code):
			handler = getattr(self, name)
			handler(*args)
			if self.semi == True:
				self.semi = False
			elif self.semi == False:
				self.semi = None
		return self.toTuple(self.stack[0])
	
	def toTuple(self, data):
		if isinstance(data, list):
			return tuple(map(self.toTuple, data))
		else:
			return data
	
	def push(self, type):
		new = [type]
		self.cur.append(new)
		self.stack.append(self.cur)
		self.cur = new
	
	def pop(self, type):
		if self.cur[0] == type:
			self.cur = self.stack.pop()
			if type in ('expr', 'stmt') and len(self.cur[-1]) == 1:
				del self.cur[-1]
			return True
		else:
			return False
	
	def comment(self, comment):
		pass
	
	def name(self, name):
		self.cur.append(('name', name))
	
	def newline(self, _):
		if self.semi == None:
			self.pop('stmt')
			self.push('stmt')
	
	def suppressedNewline(self, _):
		pass
	
	def semicolon(self, _):
		self.pop('stmt')
		self.push('stmt')
		self.semi = True
	
	def comma(self, _):
		self.pop('expr')
		self.push('expr')
	
	def op(self, op):
		self.cur.append(('op', op))
	
	def number(self, num, flags):
		if flags != None and 'f' in flags.lower():
			num = float(num)
		elif num.startswith('0o'): # Octal
			num = int(num[2:], 8)
		elif num.startswith('0x'): # Hex
			num = int(num[2:], 16)
		else:
			num = int(num)
		self.cur.append(num)
	
	def openParen(self, _):
		self.push('group')
		self.push('expr')
	
	def closeParen(self, _):
		self.pop('expr')
		self.pop('group')
	
	def openBrace(self, _):
		self.push('block')
		self.push('stmt')
	
	def closeBrace(self, _):
		self.pop('stmt')
		self.pop('block')
		if self.pop('stmt'):
			self.push('stmt')
	
	def openBracket(self, _):
		self.push('expr')
	
	def closeBracket(self, _):
		self.pop('expr')

if __name__=='__main__':
	import pprint, sys
	pprint.pprint(Parser().parse(file(sys.argv[1]).read()))
