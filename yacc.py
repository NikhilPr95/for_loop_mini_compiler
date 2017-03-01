import pickle
from classes import *
with open('tokens.pkl', 'rb') as fp:
		token_list = pickle.load(fp)

print(token_list)
"""
PROG -> S

STATEMENT -> FOR_LOOP | IF_COND | ASSIGN | DECL | STATEMENT STATEMENT

FOR_LOOP -> KEY[for] ( ASSIGN ; COND ; S) { S }

IF_COND -> KEY[if] ( COND ) { S } OP_ELSE
OP_ELSE -> KEY{else} { S } | epsilon

ASSIGN -> IDENTIFIER = ( IDENTIFIER | NUM) ;

DECL -> TYPE IDENTIFIER ;

"""

#def program(token_list):
	
#def statement():
	
#print next(token_list)