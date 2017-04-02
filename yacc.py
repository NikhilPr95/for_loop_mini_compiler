import pickle
import itertools
import copy
from classes import *

with open('tokens.pkl', 'rb') as fp:
		token_list = pickle.load(fp)

with open('token_types.pkl', 'rb') as fp:
		token_types = pickle.load(fp)

rules = [
			"PROG: STATEMENT eof",
			"STATEMENT: FOR_LOOP_ST | IF_COND_ST | DEFN_ST | ASSIGN_ST | DECL_ST",
			"FOR_LOOP_ST: FOR_LOOP ST | FOR_LOOP",
			"IF_COND_ST: IF_COND ST | IF_COND",
			"ASSIGN_ST: ASSIGN ST | ASSIGN",
			"DECL_ST: DECL ST | DECL",
			"DEFN_ST: DEFN ST | DEFN",
			"ST: STATEMENT_ST ",
			"STATEMENT_ST: STATEMENT ; ST | STATEMENT ",
			"FOR_LOOP: for ( ASSIGN COND INCREMENT ) { STATEMENT }",
			"INCREMENT: I_ASSIGN | I_COND | EXPRESSION",
			"IF_COND: if ( COND ) { STATEMENT ; } OP_ELSE | if ( COND ) { STATEMENT }",
			"OP_ELSE: else { STATEMENT } ",
			"ASSIGN: identifier = EXPRESSION ;",			
			"DECL: type ID ;",
			"ID: identifier ID'",
			"ID': , identifier ID' | epsilon ", 
			"DEFN: type ASSIGN",
			"COND: EXPRESSION1 relational_operator EXPRESSION2 ;",
			"I_ASSIGN: identifier = EXPRESSION",
			"I_COND: EXPRESSION1 relational_operator EXPRESSION2",
			"EXPRESSION1: EXPRESSION",
			"EXPRESSION2: EXPRESSION",
			"EXPRESSION: E",
			"E: T E'",
			"E': M E1' | M E2'",
			"M: epsilon",
			"E1': + T E' | epsilon",
			"E2': - T E' | epsilon",
			"T: F T'",
			"T': T1' | T2'",
			"T1': * F T' | epsilon",
			"T2': / F T' | epsilon",
			"F: ( E ) | identifier | number ",
		]

assign = {
	'ASSIGN' : {
		'identifier' : [['=',(0,'type'),('root','inh')]],
		'EXPRESSION' : [['=',(0,'val'),(2,'val')]]
	},
	'DECL': {
		'type' : [['=',(1, 'inh'), (0, 'type')]]
	},
	'ID': {
		'identifier' : [['=', (0, 'type'), ('root', 'type')]]
	},
	'ID\'' : {
		'identifier' : [['=', (1,'type'),('root','type')], ['=',(2,'type'),('root','type')]]
	},
	'DEFN' : {
		'type' : [['=',(1, 'inh'), (0, 'type')]]
	},
	'EXPRESSION1' : {
		'EXPRESSION' : [['=',('root','val'),(0,'val')]]
	},
	'EXPRESSION2' : {
		'EXPRESSION' : [['=',('root','val'),(0,'val')]]
	},
	'EXPRESSION' : {
		'E' : [['=',('root','val'),(0,'val')]]
	},
	'E' : {
		'T' : [['=',(1,'inh'),(0,'val')]],
		'E\'' : [['=', ('root','val'),(1,'synval')]]
	},
	'E\'': {
		'M': [['=',(1,'inh'),(0,'inh')]], 
		'E1\'': [['=',(0,'synval'),(1,'synval')]],
		'E2\'': [['=',(0,'synval'),(1,'synval')]]
	},
	'E1\'' : {
		'T' : [['+=',(2,'inh'),('root','inh'),(1,'inh')]],
		'E\'' : [['=',('root','synval'),(1,'synval')]],	
	},
	'E2\'' : {
		'T' : [['-=',(2,'inh'),('root','inh'),(1,'inh')]],
		'E\'' : [['=',('root','synval'),(1,'synval')]],
	},
	'T' : {
		'F' : [['=',(1,'inh'),(0,'val')]],
		'T\'' : [['=', ('root','val'),(1,'synval')]]
	},
	'T\'': {
		'M': [['=',(1,'inh'),(0,'inh')]], 
		'T1\'': [['=',(0,'synval'),(1,'synval')]],
		'T2\'': [['=',(0,'synval'),(1,'synval')]]
	},
	'T1\'' : {
		'F' : [['*=',(2,'inh'),('root','inh'),(1,'inh')]],
		'T\'' : [['=',('root','synval'),(1,'synval')]],	
	},
	'T2\'' : {
		'F' : [['/=',(2,'inh'),('root','inh'),(1,'inh')]],
		'T\'' : [['=',('root','synval'),(1,'synval')]],
	},
	'F' : {
		'(' : [['=',(0,'inh'),('root','inh')]],
		')' : [['=',('root','synval'),(0,'synval')]],
		'identifier' : [['=',('root','synval'),(0,'val')]],
		'number' : [['=',('root','synval'),(0,'lexval')]]
	}
	
}
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
	return store.index > start.index
	
def is_producer(symbol):
	return symbol.isupper()

def is_token(symbol):
	return symbol in token_types

def assign_token_vals(token, node):
	x=1
	
def get_params(vals, children):
	tuples = vals[1:]
	num = len(tuples)
	params = []
	
	for val in tuples:
		x = vals[0]
		x_attr = vals[1]
		
		if x == 'root':
			node_x = root
		else:
			node_x = children(x)		
		params.append(node_x, x_attr)
	
	return params	

def assign_producer_vals(symbol, rule, root):
	if root in assign:
		if symbol in assign[root]:
			vals = assign[root][symbol]
			children = root.get_children()
			if vals[0] == '=':
				node_x, x_attr, node_y, y_attr = get_params(vals, children)			
				setattr(node_x, x_attr, getattr(node_y, y_attr))
			elif vals[0] == '+=':
				node_x, x_attr, node_y, y_attr, node_z, z_attr = get_params(vals, children)
				setattr(node_x, x_attr, (getattr(node_y, y_attr) + getattr(node_z, z_attr)))
			elif vals[0] == '-=':
				node_x, x_attr, node_y, y_attr, node_z, z_attr = get_params(vals, children)
				setattr(node_x, x_attr, (getattr(node_y, y_attr) - getattr(node_z, z_attr)))
			elif vals[0] == '*=':
				node_x, x_attr, node_y, y_attr, node_z, z_attr = get_params(vals, children)
				setattr(node_x, x_attr, (getattr(node_y, y_attr) * getattr(node_z, z_attr)))
			elif vals[0] == '/=':
				node_x, x_attr, node_y, y_attr, node_z, z_attr = get_params(vals, children)
				setattr(node_x, x_attr, (getattr(node_y, y_attr) / getattr(node_z, z_attr)))
		
#def assign_producer_vals(symbol, rule, root):
	
def assign_symbol_vals():
	x=1
			
def match_token(token, store, symbol, node):
	print("in match token", token.val, token.type, symbol)
	if token.type == symbol:
		assign_token_vals(token, node)
		store.set_index(token.index + 1)	
		return True
	return False
	
def is_tuple(symbol):
	return symbol[0] == '(' and symbol[-1] == ')'
	
def is_valid(rule, productions, token, store, root):
	temp = TokenList(token_list,0)
	update(temp, token)
	matched = True
	children = root.get_children()
	for i in range(len(rule)):
		symbol = rule[i]
		child = children[i]
		print("SYMBOL ", symbol)
		print("in symbol", symbol, "\t\t(in rule ", rule, ")")			
		if matched:
			if is_producer(symbol):
				print("in producer")
				if match_rule(temp, store, productions, symbol, child):
					if has_proceeded(temp, store):
						print("1.SYMBOL in RULE", symbol, rule)
						if not symbol == rule[-1]: #don't progress token if the symbol is the last in the list -> Error
							update(temp, store)
						#assign_producer_vals(symbol, rule, root)
						print("1. temp store", temp.val, store.val)					
					else:
						print("1. unmatched", symbol, temp.val, store.val, rule)
						return False
				else:
					print("2. unmatched", symbol, temp.val, store.val, rule)
					return False
			elif is_token(symbol):
				print("is token")
				if match_token(temp, store, symbol, child):
					if has_proceeded(temp, store):
						print("2.SYMBOL in RULE", symbol, rule)
						if not symbol == rule[-1]:
							update(temp, store)
						print("matched")
						print("2. temp store", temp.val, store.val)
					else:
						print("3. unmatched not proceeded", symbol, temp.val)
						return False
				else:
					print("4. unmatched token")
					return False
			else: #string match
				print("else", temp.val, symbol)
				if (temp.val == symbol):
					if (temp.type == 'eof'):
						print("done!")
						return True
					else:
						temp.increment()
						update(store, temp)
						print("matched")
				else:
					print("5. unmatched", symbol, temp.val)
					return False					
		else:
			print ("unmatched exiting")
			return False
			
	return matched

def print_tabs(n):
	print(n*' ', end = " ")

	
def print_tree(root):
	print(root.name, end= " ")
	if is_producer(root.name) and root.children:
		print("[", end = "")
	for child in root.children:
		print_tree(child)
	if is_producer(root.name) and root.children:
		print("]", end = " ")
			
def match_rule(token, store, productions, producer, root):
	print("in match rule with ", producer, ":", productions[producer])
	for rule in productions[producer]:
		print("in rule ", rule, " with ", token.val)
		root.set_children(rule)
		#assign_producer_vals(root)
		print("TREE")
		print_tree(root)
		print("")
		if (is_valid(rule, productions, token, store, root)):
			print("here we are", rule, productions[producer], productions[producer].index(rule))
			#assign_producer_vals(root)
			return True
		else:
			x = None
			root.delete_children()
			print("TREE")
			print_tree(root)
			print("")
			print("returned false ", rule, productions[producer])
	
	return False
			
def start(token_list):
	eof = Token('eof', 'eof')
	token_list.append(eof)
	token = TokenList(token_list, 0)
	store = TokenList(token_list,0)
	root = Tree("PROG")

	print("TREE")
	print_tree(root)
	print("")
	
	if match_rule(token, store, productions, "PROG", root):
		print("VALID", token.val, store.val)
	else:
		print("ERROR", token.val, store.val)
	
	return root
		
def init_rules():	
	for rule in rules:
		symbol, prod = rule.split(":")
		for p in prod.split("|"):
			add(productions, symbol, p.strip())

init_rules()
			
for item in sorted(productions.items()):
	print(item)
print("\n")
print([(tok.val, tok.type) for tok in token_list])
print("\n")
print("\n")


tree = start(token_list)
print("TREE")
print_tree(tree)
print("")
