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

#def program(token_list):
	
#def statement():


def get_next(token_list, token):
	return token_list[token_list.index(token) + 1]
	
def get_prev(token_list, token):
	return token_list[token_list.index(token) - 1]