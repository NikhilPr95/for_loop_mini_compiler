import pickle
import itertools
import copy
from classes import *

with open('tokens.pkl', 'rb') as fp:
		token_list = pickle.load(fp)

with open('token_types.pkl', 'rb') as fp:
		token_types = pickle.load(fp)
		
"""
PROG : STATEMENT

STATEMENT : FOR_LOOP_ST | IF_COND_ST | ASSIGN_ST | DECL_ST

FOR_LOOP_ST : FOR_LOOP ST
IF_COND_ST : IF_COND ST
ASSIGN_ST : ASSIGN ST
DECL_ST : DECL ST

ST : STATEMENT_ST | epsilon

STATEMENT_ST : STATEMENT ST

FOR_LOOP : for ( ASSIGN ; COND ; S) { S }

IF_COND : KEY[if] ( COND ) { S } OP_ELSE
OP_ELSE : KEY{else} { S } | epsilon

ASSIGN : IDENTIFIER = ( IDENTIFIER | NUM | EXPRESSION) ;

DECL : TYPE IDENTIFIER ;

EXPRESSION : E

E : TE' | T
E' : +TE' | -TE' | EPSILON
T : FT' | F
T' : *FT' | /FT' | EPSILON
F : G^F | G
G : (E) | id | num 

"""
rules = [
			"PROG: STATEMENT",
			"STATEMENT: FOR_LOOP_ST | IF_COND_ST | ASSIGN_ST | DECL_ST",
			"FOR_LOOP_ST: FOR_LOOP ST",
			"IF_COND_ST: IF_COND ST",
			"ASSIGN_ST: ASSIGN ST",
			"DECL_ST: DECL ST",
			"ST: STATEMENT_ST | epsilon",
			"STATEMENT_ST: STATEMENT ST",
			"FOR_LOOP: for ( ASSIGN ; COND ; S) { S }",
			"IF_COND: if ( COND ) { S } OP_ELSE",
			"OP_ELSE: else { S } | epsilon",
			"ASSIGN: identifier = ( VAL ) ;",
			"VAL: identifier | number | EXPRESSION",
			"DECL: TYPE identifier ;",
			"EXPRESSION: E",
			"E: T E' | T",
			"E': + T E' | - T E' | epsilon",
			"T: F T' | F",
			"T': * F T' | / F T' | epsilon",
			"F: G ^ F | G",
			"G: ( E ) | id | num" 
		 ]

productions = dict()

def add(dict, key, val):
	sym_list = []
	if key not in dict:
		dict[key] = []
	for symbol in val.strip().split(' '):
		sym_list.append(symbol)
	dict[key].append(sym_list)
	
def update(token1, token2):
	token1.set_index(token2.index)
	
def has_proceeded(start, store):
	print("proceed", start.val, store.val)
	return store.index > start.index
	
def is_producer(symbol):
	return symbol.isupper()

def is_token(symbol):
	return symbol in token_types

def match_token(token, store, symbol):
	if token.type == symbol:
		print("token matched")
		token.increment()
		update(store, token)

def is_tuple(symbol):
	return symbol[0] == '(' and symbol[-1] == ')'
	
def is_valid(rule, productions, token, store):
	start = token
	y = store.index
	matched = True
	for symbol in rule:
		if matched:
			print("in symbol", symbol)
			if is_producer(symbol):
				print("in if")
				match_rule(token, store, productions, symbol)			
				if has_proceeded(token, store):
					update(token, store)
				else:
					matched = False
			elif is_token(symbol):
				print("is token", symbol)
				match_token(token, store, symbol)
				if has_proceeded(token, store):
					update(token, store)
				else:
					matched = False
			else:
				print("in else ")
				if (token.val == symbol):
					print("matched")
					token.increment()
					update(store, token)		
				else:
					matched =  False
	
	return matched
	
def match_rule(token, store, productions, producer):
	print("in match rule with ", producer)
	for rule in productions[producer]:
		print("in rule ", rule)
		if (is_valid(rule, productions, token, store)):
			x = store.index
			return store

def start(token_list):
	token = TokenList(token_list, 0)
	store = TokenList(token_list,0)
	
	match_rule(token, store, productions, "PROG")

def init_rules():	
	for rule in rules:
		symbol, prod = rule.split(":")
		for p in prod.split("|"):
			add(productions, symbol, p.strip())

init_rules()
			
for item in productions.items():
	print(item)
print("\n")
print([(tok.val, tok.type) for tok in token_list])
print("\n")
print("\n")

start(token_list)
#print("ttt",token_types)