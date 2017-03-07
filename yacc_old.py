import pickle
import itertools
from classes import *
with open('tokens.pkl', 'rb') as fp:
		token_list = pickle.load(fp)

#print(token_list)

"""
PROG -> STATEMENT

STATEMENT -> FOR_LOOP_ST | IF_COND_ST | ASSIGN_ST | DECL_ST

FOR_LOOP_ST -> FOR_LOOP ST
IF_COND_ST -> IF_COND ST
ASSIGN_ST -> ASSIGN ST
DECL_ST -> DECL ST

ST -> STATEMENT_ST | epsilon

STATEMENT_ST -> STATEMENT ST


FOR_LOOP -> for ( ASSIGN ; COND ; S) { S }

IF_COND -> KEY[if] ( COND ) { S } OP_ELSE
OP_ELSE -> KEY{else} { S } | epsilon

ASSIGN -> IDENTIFIER = ( IDENTIFIER | NUM | EXPRESSION) ;

DECL -> TYPE IDENTIFIER ;

EXPRESSION ->

"""

def get_index(token):
	return token_list.index(token)
	
def get_first(token_list):
	return token_list[0]

def get_next(token_list, token):
	return token_list[get_index(token) + 1]
	
def get_prev(token_list, token):
	return token_list[get_index(token) - 1]

def is_valid(token, store):
	return (not ((store is None) or (store is False)) and get_index(store) > get_index(token))

def update(token1, token2):
	token1.val = token2.val
	token1.index = token2.index

def program(token_list):
	token = get_first(token_list)
	store = Token(token.val, token.type)
	statement(token, store)
	if is_valid(token, store):
		print("SUCCESS")

# 'for', '(', assign, cond, statement, ')', '{', statement, '}'
def match_rule(token, store, rules):
	try:
		for rule in rules:
			if type(rule) == str:
				token = match_string_and_proceed(token, rule)
			else:
				token = rule(token, store)
		return store
	except:
		return False
		
def statement(token, store):
	for function in [for_loop_st, if_cond_st, assign_st, decl_st]:
		if is_valid(token, function(token, store)):
			return store

def st(token, store):
	statement_st(token, store)
	if is_valid(token, store):
		return store
	else:
		return token
		
def for_loop_st(token, store):
	for_loop(token, store)
	update(token, store)
	st(token, store)
	return store

def if_cond_st(token, store):
	if_cond(token, store)
	update(token, store)
	st(token, store)
	return store
	
def assign_st(token, store):
	assign(token, store)
	update(token, store)
	st(token, store)
	return store
	
def decl_st(token, store):
	decl(token, store)
	update(token, store)
	st(token, store)
	return store



def match_string_and_proceed(token, string):
	if token.val == string:
		return get_next(token_list, token)
	return False
		
def for_loop(token, store):
	try:
		token = match_string_and_proceed(token, 'for')
		token = match_string_and_proceed(token, '(')
		token = assign(token, store)
		token = cond(token, store)
		token = statement(token, store)		
		token = for_body(token, store)
	except:
		return False
		
def for_loop(token, store):
	if token.val == "for":
		token = get_next(token_list,token)
		if token.val == "(":
			token = get_next(token_list,token)
			token = assign(token, store)
			token = get_next(token_list,token)
			token = cond(token, store)
			token = get_next(token_list,token)
			token = statement(token, store)
			token = get_next(token_list,token)
			if token.val == ")":
				token = get_next(token_list,token)	
				token = for_body(token, store)
				return store
	return False

def for_body(token, store):
	try:
		token = match_string_and_proceed(token, '{')
		token = 
	except:
		return False
		
def for_body(token, store):
		if token.val == "{":
			token = get_next(token_list,token)
			token = statement(token, store)
			token = get_next(token_list, token)
			if token.val == '}':
				update(store, token)
				return store
		else:
			statement(token, store)
			return store
	
	
def if_cond(token):
	token = get_next(token_list,token)
	if token.val == "(":
		token = get_next(token_list,token)
		token = cond(token, store)		
		token = get_next(token_list,token)
		if token.val == ")":
			token = get_next(token_list,token)
			if token.val == "{":
				token = get_next(token_list,token)
				token = statement(token, store)
				token = get_next(token_list,token)
				if token.val == '}':
					op_else(token, store)
					return store
			else:
				token = statement(token, store)
				op_else(token, store)
				return store
	return False
	
def else_cond(token, store):
	token = get_next(token_list, token)
	if token.val == "else":
		token = get_next(token_list,token)
		if token.val == "{":
			token = get_next(token_list,token)
			token = statement(token, store)
			token = get_next(token_list,token)
			if token.val == '}':
				update(store, token)
				return store
		else:
			statement(token, store)			
			return store
	return False
	
def op_else(token):
	else_cond(token, store)
	if is_valid(token, store):
		return store
	else:
		return token

								
#print([(token.val, token.type) for token in token_list])
program(token_list[3:])