import sys
import copy
import pickle
from classes import *

### Getting input program ###
inFile = sys.argv[1]
string = ""

with open(inFile,'r') as i:
    lines = i.readlines()
	
for line in lines:
	string += line

####
#keywords = ['break', 'case', 'char', 'continue', 'do', 'double', 'else', 'for', 'float', 'if', 'int', 'include', 'long', 'return', 'sizeof', 'static', 'switch', 'void', 'while']

symtab = dict()
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
		store.index = ch.index
		return True
	else:
		return False

def match_string_with_lookahead(ch, store, string, lookaheads):
	ch, i = match(ch, string)
	if (i == len(string)):
		if ch.val in lookaheads:
		#if is_space(ch.val):
			ch.decrement()
			store.index = ch.index
			return True
		else:
			return False
	else:
		return False
					
def number(index, store):
	ch = Character(string, index)
	while (digit(ch.val)):
		ch.increment()
	ch.decrement()
	if ch.index >= index:
		store.index = ch.index
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
		store.index = ch.index
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
		store.index = ch.index
		return store.index
	else:
		return -1
			
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
				store.index = ch.index
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
		store.index = ch.index
		return store.index
	else:
		ch.decrement()
		store.index = ch.index
		return store.index		

def relational_operator(index, store):
	ch = Character(string, index)
	if (ch.val == '<'):
		ch.increment()
		if (ch.val == '='):
			store.index = ch.index
			return store.index
		elif (is_space(ch.val)):
			ch.decrement()
			store.index = ch.index
			return store.index				
	elif (ch.val == '>'):
		ch.increment()
		if (ch.val == '='):
			store.index = ch.index
			return store.index
		elif (is_space(ch.val)):
			ch.decrement()
			store.index = ch.index
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
	#print("in punct")
	ch =Character(string, index)
	for symbol in [',', ';', ':', ')', '(', '[', ']', '{', '}']:
		if match_string(ch, store, symbol):
			return store.index
		
		
def start():
	lexemeBegin = Character(string, 0)
	print("here ", lexemeBegin.val)
	index = -1
	store = Character(string, 0)
	while lexemeBegin.index < len(string):
		yes = False
		for function in [keyword, punctuation, string_literal, number, relational_operator, assignment_operator, arithmetic_operator, logical_operator, bitwise_operator, identifier]:
			if is_valid(lexemeBegin, function(lexemeBegin.index, store)):
				tokenize_and_forward(lexemeBegin, store.index, function.__name__.upper())
				yes = True
		if not yes:		
			if lexemeBegin.index + 1 == len(string):
				break
			lexemeBegin.increment()
		
def tokenize_and_forward(lexemeBegin, index, tok_type):
	token = string[lexemeBegin.index : index + 1]
	lexemeBegin.increment_mult(index + 1 - lexemeBegin.index)
	print((tok_type, token))
	if (tok_type == 'IDENTIFIER'):
		add_to_symtab(token)
	token_list.append(Token(tok_type, token))
	return Token(tok_type, token)
			
start()

print("SYMTAB -")
print(sorted(symtab.items()))
print([(tok.type,tok.val) for tok in token_list])

with open('tokens.pkl', 'wb') as fp:
	pickle.dump(token_list, fp, pickle.HIGHEST_PROTOCOL)