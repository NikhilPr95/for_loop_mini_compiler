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

def digit(c):
	return c.isdigit()
	
def isLetter(c):
	return c.isalpha()

def is_space(char):
	return (char == ' ' or char == '\n' or char == '\r' or char == '\t')

def add_to_symtab(token):
	if not token in symtab:
		symtab[token] = None
		
def tokenize_and_forward(lexemeBegin, index, tok_type):
	token = string[lexemeBegin.index : index + 1]
	lexemeBegin.increment_mult(index + 1 - lexemeBegin.index)
	print((tok_type, token))
	if (tok_type == 'IDENTIFIER'):
		add_to_symtab(token)
	token_list.append(Token(tok_type, token))
	return Token(tok_type, token)
	
def is_valid(lexemeBegin, index):
	return (not (index is None) and index >= lexemeBegin.index)
		
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
		#ch.decrement()
		store.index = ch.index
		return store.index
	else:
		return -1
			
def keyword(index, store):
	ch = Character(string, index)
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
	elif (ch.val == '='):
		ch.increment()
		if (ch.val == '='):
			store.index = ch.index
			return store.index		
	elif (ch.val == '!'):
		ch.increment()
		if (ch.val == '='):
			store.index = ch.index
			return store.index

def logical_operator(index, store):
	ch = Character(string, index)
	if (ch.val == '&'):
		ch.increment()
		if (ch.val == '&'):
			store.index = ch.index
			return store.index
	elif (ch.val == '|'):
		ch.increment()
		if (ch.val == '|'):
			store.index = ch.index
			return store.index
	elif (ch.val == '!'):
		store.index = ch.index
		return store.index

def bitwise_operator(index, store):
	ch = Character(string, index)
	if (ch.val == '&'):
		store.index = ch.index
		return store.index
	elif (ch.val == '|'):
		store.index = ch.index
		return store.index
	elif (ch.val == '^'):
		store.index = ch.index
		return store.index
	elif (ch.val == '~'):
		store.index = ch.index
		return store.index
	elif (ch.val == '<'):
		ch.increment()
		if (ch.val == '<'):
			store.index = ch.index
			return store.index
	elif (ch.val == '>'):
		ch.increment()
		if (ch.val == '>'):
			store.index = ch.index
			return store.index
	
def arithmetic_operator(index, store):
	ch = Character(string, index)
	if (ch.val == '+'):
		return check_extra(ch, store, '+')
	elif (ch.val == '-'):
		return check_extra(ch, store, '-')
	elif (ch.val == '*'):
		store.index = ch.index
		return store.index
	elif (ch.val == '\\'):
		store.index = ch.index
		return store.index
	elif (ch.val == '%'):
		store.index = ch.index
		return store.index

def assignment_operator(index, store):
	ch = Character(string, index)
	if (ch.val == '='):
		store.index = ch.index
		return store.index
	elif (ch.val == '+'):
		ch.increment()
		if (ch.val == '='):
			store.index = ch.index
			return store.index
	elif (ch.val == '-'):
		ch.increment()
		if (ch.val == '='):
			store.index = ch.index
			return store.index
	elif (ch.val == '*'):
		ch.increment()
		if (ch.val == '='):
			store.index = ch.index
			return store.index
	elif (ch.val == '/'):
		ch.increment()
		if (ch.val == '='):
			store.index = ch.index
			return store.index
	elif (ch.val == '%'):
		ch.increment()
		if (ch.val == '='):
			store.index = ch.index
			return store.index
	elif (ch.val == '&'):
		ch.increment()
		if (ch.val == '='):
			store.index = ch.index
			return store.index
	elif (ch.val == '^'):
		ch.increment()
		if (ch.val == '='):
			store.index = ch.index
			return store.index
	elif (ch.val == '|'):
		ch.increment()
		if (ch.val == '='):
			store.index = ch.index
			return store.index
	elif (ch.val == '<'):
		ch.increment()
		if ch.val == '<':
			ch.increment()
			if (ch.val == '='):
				store.index = ch.index
				return store.index
	#elif not match_string(ch, store, '<<='):
	#	match_string(ch, store, '>>=')
	#"""
	elif (ch.val == '>'):
		ch.increment()
		if ch.val == '>':
			ch.increment()
			if (ch.val == '='):
				store.index = ch.index
				return store.index
	#"""
	
def match_string(ch, store, string):
	i = 0
	while (i < len(string) and ch.val == string[i]):
		ch.increment()
		i += 1
	print("I EQEQWEL", i)
	if (i == len(string)):
		store.index = ch.index
		return store.index
	else:
		return -1
def start():
	lexemeBegin = Character(string, 0)
	print("here ", lexemeBegin.val)
	index = -1
	store = Character(string, 0)
	while lexemeBegin.index < len(string):
		if is_valid(lexemeBegin, keyword(lexemeBegin.index, store)):
			tokenize_and_forward(lexemeBegin, store.index, "KEYWORD")
		elif is_valid(lexemeBegin, string_literal(lexemeBegin.index, store)):
			tokenize_and_forward(lexemeBegin, store.index, "STRING LITERAL")
		elif is_valid(lexemeBegin, number(lexemeBegin.index, store)):
			tokenize_and_forward(lexemeBegin, store.index, "NUMBER")
		elif is_valid(lexemeBegin, relational_operator(lexemeBegin.index, store)):
			tokenize_and_forward(lexemeBegin, store.index, "RELATIONAL OPERATOR")
		elif is_valid(lexemeBegin, assignment_operator(lexemeBegin.index, store)):
			tokenize_and_forward(lexemeBegin, store.index, "ASSIGNMENT OPERATOR")
		elif is_valid(lexemeBegin, arithmetic_operator(lexemeBegin.index, store)):
			tokenize_and_forward(lexemeBegin, store.index, "ARITHMETIC OPERATOR")
		elif is_valid(lexemeBegin, logical_operator(lexemeBegin.index, store)):
			tokenize_and_forward(lexemeBegin, store.index, "LOGICAL OPERATOR")
		elif is_valid(lexemeBegin, bitwise_operator(lexemeBegin.index, store)):
			tokenize_and_forward(lexemeBegin, store.index, "BITWISE OPERATOR")
		elif is_valid(lexemeBegin, identifier(lexemeBegin.index, store)):
			tokenize_and_forward(lexemeBegin, store.index,"IDENTIFIER")
		else:
			if lexemeBegin.index + 1 == len(string):
				break;
			lexemeBegin.increment()
		
start()

print("SYMTAB -")
print(symtab)
print([(tok.type,tok.val) for tok in token_list])

with open('tokens.pkl', 'wb') as fp:
	pickle.dump(token_list, fp, pickle.HIGHEST_PROTOCOL)