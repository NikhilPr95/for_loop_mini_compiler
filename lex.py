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
		#print("IN incrmult self.index, index = ", self.index, inc)
		self.index += inc
		self.set_val(self.index)
	
	def decrement(self):
		self.decrement_mult(1)
		
	def decrement_mult(self, dec):
		self.index -= dec
		self.set_val(self.index)
		
def is_space(char):
	return (char == ' ' or char == '\n' or char == '\r' or char == '\t')

def tokenize_and_forward(lexemeBegin, index, tok_type):
	#print("in tokenize and forward for ", lexemeBegin.index, index)
	token = string[lexemeBegin.index : index + 1]
	print((tok_type, token))
	#print("indices - ", lexemeBegin.index, index)
	lexemeBegin.increment_mult(index - lexemeBegin.index)
	#print("incremented indices - ", lexemeBegin.index, index)
	
def is_valid(lexemeBegin, index):
	#print("in valid for  ", lexemeBegin.index, index)
	#, " string = ", string[lexemeBegin.index:index])
	
	#if (not index is None):
	#	print("index > lexeme ", index > lexemeBegin.index)
	#else:
	#	print("index = none")
	
	#print("ISVALID ? ", (not (index is None) and index > lexemeBegin.index))
	return (not (index is None) and index > lexemeBegin.index)
		
def start():	
	lexemeBegin = Character(0)
	print("here ", lexemeBegin.val)
	index = -1
	store = Character(0)
	while lexemeBegin.index < len(string):
		#print("lexemeBegin.index ", lexemeBegin.index)
		if is_valid(lexemeBegin, keyword(lexemeBegin.index, store)):
			tokenize_and_forward(lexemeBegin, store.index, "KEYWORD")
		elif is_valid(lexemeBegin, identifier(lexemeBegin.index, store)):
			tokenize_and_forward(lexemeBegin, store.index,"IDENTIFIER")
		else:
			if lexemeBegin.index + 1 == len(string):
				break;
			lexemeBegin.increment()

#prabhat code		
def digit(c):
	return c.isdigit()
	
def isLetter(c):
	return c.isalpha()
	
def identifier(index, store):
	ch = Character(index)
	if(isLetter(ch.val)):
		ch.increment()
		while(digit(ch.val) or isLetter(ch.val) or ch.val == '_'):
			ch.increment()
		ch.decrement()
		store.index = ch.index
		return store.index
		
	else:
		return -1 
		

keywords = ['break', 'case', 'char', 'continue', 'do', 'double', 'else', 'for', 'float', 'if', 'int', 'include', 'long', 'return', 'sizeof', 'static', 'switch', 'void', 'while']
			
def keyword(index, store):
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
							store.index = ch.index
							return store.index
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
						store.index = ch.index
						return store.index
		elif (ch.val == 'h'):
			ch.increment()
			if (ch.val == 'a'):
				ch.increment()
				if (ch.val == 'r'):
					ch.increment()
					if (is_space(ch.val)):
						ch.decrement()
						store.index = ch.index
						return store.index
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
										store.index = ch.index
										return store.index
	elif (ch.val == 'd'):
		ch.increment()
		if (ch.val == 'o'):
			ch.increment()
			if (is_space(ch.val) or ch.val == '{'):
				ch.decrement()
				store.index = ch.index
				return store.index
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
								store.index = ch.index
								return store.index
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
						store.index = ch.index
						return store.index
	elif (ch.val == 'f'):
		ch.increment()
		if (ch.val == 'o'):
			ch.increment()
			if (ch.val == 'r'):
				ch.increment()
				if (is_space(ch.val) or ch.val == '('):
					ch.decrement()
					store.index = ch.index
					return store.index
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
							store.index = ch.index
							return store.index
	elif (ch.val == 'i'):
		ch.increment()
		if (ch.val == 'f'):
			ch.increment()
			if (is_space(ch) or ch.val == '('):
				ch.decrement()
				store.index = ch.index
				return store.index
		elif (ch.val == 'n'):
			ch.increment()
			if (ch.val == 't'):
				ch.increment()
				if (is_space(ch.val)):
					ch.decrement()
					store.index = ch.index
					return store.index
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
									store.index = ch.index
									return store.index
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
						store.index = ch.index
						return store.index
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
								store.index = ch.index
								return store.index
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
								store.index = ch.index
								return store.index
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
								store.index = ch.index
								return store.index
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
								store.index = ch.index
								return store.index
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
						store.index = ch.index
						return store.index
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
							store.index = ch.index
							return store.index	
	else:
		return -1
						
print ("STRING INDEX !!!!! = ", len(string))
start()
