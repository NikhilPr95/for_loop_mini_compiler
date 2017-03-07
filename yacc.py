import pickle
import itertools
from classes import *
with open('tokens.pkl', 'rb') as fp:
		token_list = pickle.load(fp)

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
rules = ["PROG : STATEMENT","STATEMENT : FOR_LOOP_ST | IF_COND_ST | ASSIGN_ST | DECL_ST","FOR_LOOP_ST : FOR_LOOP ST","IF_COND_ST : IF_COND ST","ASSIGN_ST : ASSIGN ST","DECL_ST : DECL ST","ST : STATEMENT_ST | epsilon","STATEMENT_ST : STATEMENT ST","FOR_LOOP : for ( ASSIGN ; COND ; S) { S }","IF_COND : KEY[if] ( COND ) { S } OP_ELSE","OP_ELSE : KEY{else} { S } | epsilon","ASSIGN : IDENTIFIER = ( IDENTIFIER | NUM | EXPRESSION) ;","DECL : TYPE IDENTIFIER ;","EXPRESSION : E","E : TE' | T","E' : +TE' | -TE' | EPSILON","T : FT' | F","T' : *FT' | /FT' | EPSILON","F : G^F | G","G : (E) | id | num" ]

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
# for A | B C
def match_rule(token, store, unsplit_rules):
	try:
		for rules in unsplit_rules.split('|'):
			for rule in rules:
				if type(rule) == str:
					token = match_string_and_proceed(token, rule)
				else:
					token = rule(token, store)
			return store
	except:
		return False

