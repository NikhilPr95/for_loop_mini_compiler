import sys
import copy

### Getting input program ###
inFile = sys.argv[1]
string = ""

with open(inFile,'r') as i:
    lines = i.readlines()
	
for line in lines:
	string += line

#print(string)

####

class Character:
	def set_val(self, index):
		self.val = string[self.index]

	def __init__(self, index):
		self.index = index
		self.set_val(self.index)
		
	def increment(self):
		self.increment_mult(1)
		
	def increment_mult(self, inc):
		if (self.index + inc) >= len(string):
			return -1
		self.index += inc
		self.set_val(self.index)
	
	def decrement(self):
		self.decrement_mult(1)
		
	def decrement_mult(self, dec):
		self.index -= dec
		self.set_val(self.index)
		
def is_space(char):
	return (char == ' ' or char == '\n' or char == '\r' or char == '\t')

def start():	
	lexemeBegin = Character(0)
	print("here ", lexemeBegin.val)
	
	while lexemeBegin.index < len(string):
		index = keyword(lexemeBegin.index)
		if not index is None and index > lexemeBegin.index:
				token = string[lexemeBegin.index : index + 1]
				print(("KEYWORD", token))
				lexemeBegin.increment_mult(index - lexemeBegin.index)
				
		else:
			if lexemeBegin.index + 1 == len(string):
				break;
			lexemeBegin.increment()

keywords = ['break', 'case', 'char', 'continue', 'do', 'double', 'else', 'for', 'float', 'if', 'int', 'include', 'long', 'return', 'sizeof', 'static', 'switch', 'void', 'while']
			
def keyword(index):
	#print("in keyword - ", index, string[index])
	ch = Character(index)
	if (ch.val == 'b'):
		ch.increment()
		if (ch.val == 'r'):
			ch.increment()
			if (ch.val == 'e'):
				ch.increment()
				if (ch.val == 'a'):
					ch.increment()
					if (ch.val == 'k'):
						ch.increment()
						if (is_space(ch.val) or ch.val == ';'):
							ch.decrement()
							return ch.index
	elif (ch.val == 'c'):		
		ch.increment()
		if (ch.val == 'a'):
			ch.increment()
			if (ch.val == 's'):
				ch.increment()
				if (ch.val == 'e'):
					ch.increment()
					if (is_space(ch.val)):
						ch.decrement()
						return ch.index
		elif (ch.val == 'h'):
			ch.increment()
			if (ch.val == 'a'):
				ch.increment()
				if (ch.val == 'r'):
					ch.increment()
					if (is_space(ch.val)):
						ch.decrement()
						return ch.index
		elif (ch.val == 'o'):
			ch.increment()
			if (ch.val == 'n'):
				ch.increment()
				if (ch.val == 't'):
					ch.increment()
					if (ch.val == 'i'):
						ch.increment()
						if (ch.val == 'n'):
							ch.increment()
							if (ch.val == 'u'):
								ch.increment()
								if (ch.val == 'e'):
									ch.increment()
									if (is_space(ch.val) or ch.val == ';'):
										ch.decrement()
										return ch.index
	elif (ch.val == 'd'):
		ch.increment()
		if (ch.val == 'o'):
			ch.increment()
			if (is_space(ch.val) or ch.val == '{'):
				ch.decrement()
				return ch.index
			elif (ch.val == 'u'):
				ch.increment()
				if (ch.val == 'b'):
					ch.increment()
					if (ch.val == 'l'):
						ch.increment()
						if (ch.val == 'e'):
							ch.increment()
							if (is_space(ch.val)):
								ch.decrement()
								return ch.index							
	elif (ch.val == 'e'):
		ch.increment()
		if (ch.val == 'l'):
			ch.increment()
			if (ch.val == 's'):
				ch.increment()
				if (ch.val == 'e'):
					ch.increment()
					if (is_space(ch.val) or ch.val == '{'):
						ch.decrement()
						return ch.index
	elif (ch.val == 'f'):
		ch.increment()
		if (ch.val == 'o'):
			ch.increment()
			if (ch.val == 'r'):
				ch.increment()
				if (is_space(ch.val) or ch.val == '('):
					ch.decrement()
					return ch.index
		elif (ch.val == 'l'):
			ch.increment()
			if (ch.val == 'o'):
				ch.increment()
				if (ch.val == 'a'):
					ch.increment()
					if (ch.val == 't'):
						ch.increment()
						if (is_space(ch.val)):
							ch.decrement()
							return ch.index			
	elif (ch.val == 'i'):
		ch.increment()
		if (ch.val == 'f'):
			ch.increment()
			if (is_space(ch) or ch.val == '('):
				ch.decrement()
				return ch.index
		elif (ch.val == 'n'):
			ch.increment()
			if (ch.val == 't'):
				ch.increment()
				if (is_space(ch.val)):
					ch.decrement()
					return ch.index
			elif (ch.val == 'c'):
				ch.increment()
				if (ch.val == 'l'):
					ch.increment()
					if (ch.val == 'u'):
						ch.increment()
						if (ch.val == 'd'):
							ch.increment()
							if (ch.val == 'e'):
								ch.increment()
								if (is_space(ch.val) or ch.val == '>'):
									ch.decrement()
									return ch.index
	elif (ch.val == 'l'):
		ch.increment()
		if (ch.val == 'o'):
			ch.increment()
			if (ch.val == 'n'):
				ch.increment()
				if (ch.val == 'g'):
					ch.increment()
					if (is_space(ch.val)):
						ch.decrement()
						return ch.index
	elif (ch.val == 'r'):
		ch.increment()
		if (ch.val == 'e'):
			ch.increment()
			if (ch.val == 't'):
				ch.increment()
				if (ch.val == 'u'):
					ch.increment()
					if (ch.val == 'r'):
						ch.increment()
						if (ch.val == 'n'):
							ch.increment()
							if (is_space(ch.val)):
								ch.decrement()
								return ch.index
	elif (ch.val == 's'):
		ch.increment()
		if (ch.val == 'i'):
			ch.increment()
			if (ch.val == 'z'):
				ch.increment()
				if (ch.val == 'e'):
					ch.increment()
					if (ch.val == 'o'):
						ch.increment()
						if (ch.val == 'f'):
							ch.increment()
							if (is_space(ch.val) or ch.val == '('):
								ch.decrement()
								return ch.index
		elif (ch.val == 't'):
			ch.increment()
			if (ch.val == 'a'):
				ch.increment()
				if (ch.val == 't'):
					ch.increment()
					if (ch.val == 'i'):
						ch.increment()
						if (ch.val == 'c'):
							ch.increment()
							if (is_space(ch.val)):
								ch.decrement()
								return ch.index
		elif (ch.val == 'w'):
			ch.increment()
			if (ch.val == 'i'):
				ch.increment()
				if (ch.val == 't'):
					ch.increment()
					if (ch.val == 'c'):
						ch.increment()
						if (ch.val == 'h'):
							ch.increment()
							if (is_space(ch.val)):
								ch.decrement()
								return ch.index
	elif (ch.val == 'v'):
		ch.increment()
		if (ch.val == 'o'):
			ch.increment()
			if (ch.val =='i'):
				ch.increment()
				if (ch.val == 'd'):
					ch.increment()
					if (is_space(ch.val)):
						ch.decrement()
						return ch.index
	elif (ch.val == 'w'):
		ch.increment()
		if (ch.val == 'h'):
			ch.increment()
			if (ch.val == 'i'):
				ch.increment()
				if (ch.val == 'l'):
					ch.increment()
					if (ch.val == 'e'):
						ch.increment()
						if (is_space(ch.val) or ch.val == '('):
							ch.decrement()
							return ch.index
	else:
		return -1
						
print ("STRING INDEX !!!!! = ", len(string))
start()