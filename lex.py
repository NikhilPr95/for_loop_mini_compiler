import sys
import copy
import pickle
from classes import *

### Getting input program ###
def get_program():
	string = ""
	inFile = sys.argv[1]

	with open(inFile,'r') as i:
		lines = i.readlines()
		
	for line in lines:
		string += line

	return string
###

#keywords = ['break', 'case', 'char', 'continue', 'do', 'double', 'else', 'for', 'float', 'if', 'int', 'include', 'long', 'return', 'sizeof', 'static', 'switch', 'void', 'while']

symtab = dict()
comment_list = []
token_list = []
spaces = ['\n','\r','\t',' ']

def digit(c):
	return c.isdigit()
	
def isLetter(c):
	return c.isalpha()

def is_valid(lexemeBegin, index):
	return (not (index is None) and index >= lexemeBegin.index)

def is_space(char):
	return (char == ' ' or char == '\n' or char == '\r' or char == '\t')

def add_to_symtab(token):
	if not token in symtab:
		symtab[token] = None

def match(ch, string):
	i = 0
	while (i < len(string) and ch.val == string[i]):
		ch.increment()
		i += 1
	return ch, i
		
def match_string(ch, store, string):
	ch, i = match(ch, string)
	if (i == len(string)):
		ch.decrement()
		store.update(ch)
		return True
	else:
		return False

def match_string_with_lookahead(ch, store, string, lookaheads):
	ch, i = match(ch, string)
	if (i == len(string)):
		if ch.val in lookaheads:
		#if is_space(ch.val):
			ch.decrement()
			store.update(ch)
			return True
		else:
			return False
	else:
		return False
					
def number(index, store):
	ch = Character(string, index)
	if (digit(ch.val)):
		ch.increment()
		while (digit(ch.val)):
			ch.increment()
		ch.decrement()
		store.update(ch)
		return store.index
	else:
		return -1
			
def identifier(index, store):
	ch = Character(string, index)
	if(isLetter(ch.val)):
		ch.increment()
		while(digit(ch.val) or isLetter(ch.val) or ch.val == '_'):
			ch.increment()
		ch.decrement()
		store.update(ch)
		return store.index		
	else:
		return -1 
		
def string_literal(index, store):
	ch = Character(string, index)
	if (ch.val == '"'):
		ch.increment()
		while not(ch.val == '"'):
			if (ch.val == '/'):
				temp = Character(index + 1)
				if (temp.val == '"'):
					ch.increment()
			ch.increment()
		store.update(ch)
		return store.index
	else:
		return -1

def type(index, store):
	ch = Character(string, index)
	for t in ['int', 'float', 'double', 'char']:
		if match_string_with_lookahead(ch, store, t, spaces):
			return store.index
		
def keyword(index, store):
	ch = Character(string, index)
	if match_string_with_lookahead(ch, store, 'break', spaces + [';']):
		return store.index
	elif (ch.val == 'c'):		
		ch.increment()
		for symbol in ['ase', 'har']:
			if match_string_with_lookahead(ch, store, symbol, spaces):
				return store.index
		if match_string_with_lookahead(ch, store, 'ontinue', spaces + [';']):
			return store.index
	elif (ch.val == 'd'):
		ch.increment()
		if (ch.val == 'o'):
			ch.increment()
			if (is_space(ch.val) or ch.val == '{'):
				ch.decrement()
				store.update(ch)
				return store.index
			elif match_string_with_lookahead(ch, store, 'uble', spaces):
				return store.index
	elif match_string_with_lookahead(ch, store, 'else', spaces + ['{']):
		return store.index
	elif (ch.val == 'f'):
		ch.increment()
		if match_string_with_lookahead(ch, store, 'or', spaces + ['{']):
			return store.index
		elif match_string_with_lookahead(ch, store, 'loat', spaces):
			return store.index
	elif (ch.val == 'i'):
		ch.increment()
		if match_string_with_lookahead(ch, store, 'f', spaces + ['(']):
			return store.index
		elif (ch.val == 'n'):
			ch.increment()
			if match_string_with_lookahead(ch, store, 't', spaces):
				return store.index
			elif match_string_with_lookahead(ch, store, 'clude', spaces + ['>']):
				return store.index			
	elif match_string_with_lookahead(ch, store, 'long', spaces):
		return store.index
	elif match_string_with_lookahead(ch, store, 'return', spaces):
		return store.index
	elif (ch.val == 's'):
		ch.increment()
		if match_string_with_lookahead(ch, store, 'izeof', spaces + ['(']):
			return store.index
		else:
			for symbol in ['tatic', 'witch']:
				if match_string_with_lookahead(ch, store, symbol, spaces):
					return store.index
	elif match_string_with_lookahead(ch, store, 'void', spaces):
		return store.index
	elif match_string_with_lookahead(ch, store, 'while', spaces + ['(']):
		return store.index
	else:
		return -1

def check_extra(ch, store, symbol):
	ch.increment()
	if (ch.val == symbol):
		store.update(ch)
		return store.index
	else:
		ch.decrement()
		store.update(ch)
		return store.index		

def relational_operator(index, store):
	ch = Character(string, index)
	if (ch.val == '<'):
		ch.increment()
		if (ch.val == '='):
			store.update(ch)
			return store.index
		elif (is_space(ch.val)):
			ch.decrement()
			store.update(ch)
			return store.index				
	elif (ch.val == '>'):
		ch.increment()
		if (ch.val == '='):
			store.update(ch)
			return store.index
		elif (is_space(ch.val)):
			ch.decrement()
			store.update(ch)
			return store.index			
	else:
		for symbol in ['==', '!=']:
			if match_string(ch, store, symbol):
				return store.index
	

def logical_operator(index, store):
	ch = Character(string, index)
	for symbol in ['&&', '||', '!']:
		if match_string(ch, store, symbol):
			return store.index
	
def bitwise_operator(index, store):
	ch = Character(string, index)
	for symbol in ['&', '|', '^', '~', '<<', '>>']:
		if match_string(ch, store, symbol):
			return store.index
	
def arithmetic_operator(index, store):
	ch = Character(string, index)
	if (ch.val == '+'):
		return check_extra(ch, store, '+')
	elif (ch.val == '-'):
		return check_extra(ch, store, '-')
	else:
		for symbol in ['*', '/', '%']:
			if match_string(ch, store, symbol):
				return store.index
		
def assignment_operator(index, store):
	ch = Character(string, index)
	for symbol in ['=', '+=', '-=', '*=', '/=', '%=', '&=', '^=', '|=', '<<=', '>>=']:
		if match_string(ch, store, symbol):
			return store.index

def punctuation(index, store):
	ch =Character(string, index)
	for symbol in [',', ';', ':', ')', '(', '[', ']', '{', '}']:
		if match_string(ch, store, symbol):
			return store.index
		
# [/][*][^*]*[*]+([^/*][^*]*[*]+)*/ | //[.]*(\n)
def comment(index, store):
	ch = Character(string, index)
	if (ch.val == '/'):
		ch.increment()
		if (ch.val == '*'):
			ch.increment()
			while (ch.val != '*'):
				ch.increment()
			if (ch.val == '*'):
				ch.increment()
				while (ch.val == '*'):
					ch.increment()
				temp = Character(string, ch.index)
				valid = True
				while (valid):
					ch= Character(string, temp.index)
					if (temp.val not in ['/','*']):
						temp.increment()
						while (temp.val != '*'):
							temp.increment()
						if (temp.val == '*'):
							temp.increment()
						else:
							valid = False							
						while (temp.val == '*'):
							temp.increment()
					else:
						valid = False
				if (ch.val == '/'):
					store.update(ch)
					return store.index
		elif (ch.val == '/'):
			ch.increment()
			while (ch.val != '\n') and ch.index < len(string):
				ch.increment()
			store.update(ch)
			return store.index
			
def remove_comments(string):
	if len(comment_list) > 0:
		str = ""
		str += string[:comment_list[0]]
		for index in range(1, len(comment_list)-1, 2):
				str += string[comment_list[index]:comment_list[index+1]]
		str += string[comment_list[-1]:]
		
		return str
	else:
		return string
token_types = [comment, type, keyword, punctuation, string_literal, number, relational_operator, assignment_operator, arithmetic_operator, logical_operator, bitwise_operator, identifier]

def start():
	comment_list = []
	lexemeBegin = Character(string, 0)
	index = -1
	store = Character(string, 0)
	while lexemeBegin.index < len(string):
		valid = False
		i = 0
		while lexemeBegin.index < len(string) and i < len(token_types):
			function = token_types[i]
			if is_valid(lexemeBegin, function(lexemeBegin.index, store)):
				tokenize_and_forward(lexemeBegin, store.index, function.__name__)
				valid = True
				i = 0
			i += 1	
			
		if not valid:
			if lexemeBegin.index + 1 == len(string):
				break
			else:
				lexemeBegin.increment()
		
def tokenize_and_forward(lexemeBegin, index, tok_type):
	global comment_list
	token = string[lexemeBegin.index : index + 1]
	print((tok_type, token))
	if (tok_type == 'IDENTIFIER'):
		add_to_symtab(token)
	if (tok_type == 'COMMENT'):
		comment_list += [lexemeBegin.index, index+1]
	else:
		token_list.append(Token(tok_type, token))
	lexemeBegin.increment_mult(index + 1 - lexemeBegin.index)
	return Token(tok_type, token)


string = get_program()	
start()
string = remove_comments(string)


print("SYMTAB -")
#print(sorted(symtab.items()))
print([(tok.type,tok.val) for tok in token_list])
print(len(string))

			
with open('tokens.pkl', 'wb') as fp:
	pickle.dump(token_list, fp, pickle.HIGHEST_PROTOCOL)
	
with open('token_types.pkl', 'wb') as fp:
	pickle.dump([t.__name__ for t in token_types], fp, pickle.HIGHEST_PROTOCOL)
	
