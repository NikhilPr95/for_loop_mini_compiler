import pickle
import itertools
from classes import *
with open('tokens.pkl', 'rb') as fp:
		token_list = pickle.load(fp)

#print(token_list)

"""
PROG -> STATEMENT

STATEMENT -> FOR_LOOP | IF_COND | ASSIGN | DECL | STATEMENT STATEMENT

FOR_LOOP -> KEY[for] ( ASSIGN ; COND ; S) { S }

IF_COND -> KEY[if] ( COND ) { S } OP_ELSE
OP_ELSE -> KEY{else} { S } | epsilon

ASSIGN -> IDENTIFIER = ( IDENTIFIER | NUM) ;

DECL -> TYPE IDENTIFIER ;

"""

def program(token_list):
	t = get_first(token_list)
	statement(t)
	
def statement(token):
	if token.value == "for":
		for_loop(token)
	elif token.value == "if":
		if_cond(token)
	elif get_next(token_list,token).value == "=" and not get_next(token_list,token).value == "=":
		assign(token)
	elif token.value == "int" or token.value == "float":
		decl(token)
	else:
		statement(token)
		statement(token)
		
def for_loop(token):
	if token.value == "for":
		token = get_next(token_list,token)
		if token.value == "(":
			token = get_next(token_list,token)
				assign(token)
				token = get_next(token_list,token)
				if token.value == ";"
					token = get_next(token_list,token)
					cond(token)
					token = get_next(token_list,token)
					if token.value == ";"
						token = get_next(token_list,token)
						statement(token)
						token = get_next(token_list,token)
						if token.value == ")"
							token = get_next(token_list,token)
							if token.value == "{":
								token = get_next(token_list,token)
								statement(token)
								token = get_next(token_list,token)
							else:
								statement(token)
							
def if_cond(token):
	token = get_next(token_list,token)
	if token.value == ";"
		token = get_next(token_list,token)
		cond(token)
		token = get_next(token_list,token)
		if token.value == ")":
			token = get_next(token_list,token)
			if token.value == "{":
				token = get_next(token_list,token)
				statement(token)
				token = get_next(token_list,token)
			else:
				statement(token)
			token = get_next(token_list,token)
			if token.value == "else":
				token = get_next(token_list,token)
				if token.value == "{":
					token = get_next(token_list,token)
					statement(token)
					token = get_next(token_list,token)
				else:
					statement(token)
				

							
				

	
#def statement():

def get_first(token_list):
	return token_list[0]

def get_next(token_list, token):
	return token_list[token_list.index(token) + 1]
	
def get_prev(token_list, token):
	return token_list[token_list.index(token) - 1]
