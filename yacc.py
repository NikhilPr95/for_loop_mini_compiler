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
			"DECL: type identifier ;",
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
#'''

#Problem - Currently computes only when it is going down - Need it to do so when going back up (synvals)
#Currently top-down parser is only top-down -- There is no going up... Once it comes back up we can apply
# the rules but I think there will be conflict. Applying the top down rules again in bottom-up
# thus screwing up the values
#in bottom up only certain rules need to be applied
# example in E -> TE' the rule for E' has to be applied not for T
# also in the same rule, E' should not be applied when going top down
# so does that mean the last rule is always bottom up?
# How apt ! Because the if condition symbol != rule[-1] is just above! i just need to do a tab indent
# next what is required is assign prod to be called after it comes out of isvalid and apply the rule for the last symbol

# But i am still not sure if it is correct
# need to verify

assign = {
	'ASSIGN' : {
		'identifier' : [['=',(0,'type'),('root','inhval')]], # is this correct?
		'EXPRESSION' : [['=',(0,'val'),(2,'val')]]
	},
	'DECL': {
		'type' : [['=',(1, 'inhval'), (0, 'type')]]
	},
	'ID': {
		'identifier' : [['=', (0, 'type'), ('root', 'type')]]
	},
	'ID\'' : {
		'identifier' : [['=', (1,'type'),('root','type')], ['=',(2,'type'),('root','type')]]
	},
	'DEFN' : {
		'type' : [['=',(1, 'inhval'), (0, 'type')]]
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
		'T' : [['=',(1,'inhval'),(0,'val')]],
		'E\'' : [['=', ('root','val'),(1,'synval')]]
	},
	'E\'': {
		'M': [['=',(0,'inhval'),('root','inhval')]],  # Changed all 0 to root here and  1 to 0
		'E1\'': [['=',('root','synval'),(0,'synval')]],
		'E2\'': [['=',('root','synval'),(0,'synval')]]
	},
	'E1\'' : {
		'T' : [['+=',(2,'inhval'),('root','inhval'),(1,'inhval')]],
		'E\'' : [['=',('root','synval'),(1,'synval')]],	
	},
	'E2\'' : {
		'T' : [['-=',(2,'inhval'),('root','inhval'),(1,'inhval')]],
		'E\'' : [['=',('root','synval'),(1,'synval')]],
	},
	'T' : {
		'F' : [['=',(1,'inhval'),(0,'val')]],
		'T\'' : [['=', ('root','val'),(1,'synval')]]
	},
	'T\'': {
		'M': [['=',(0,'inhval'),('root','inhval')]], # Changed all 0 to root here and 1 to 0
		'T1\'': [['=',('root','synval'),(0,'synval')]],
		'T2\'': [['=',('root','synval'),(0,'synval')]]
	},
	'T1\'' : {
		'F' : [['*=',(2,'inhval'),('root','inhval'),(1,'inhval')]],
		'T\'' : [['=',('root','synval'),(1,'synval')]],	
	},
	'T2\'' : {
		'F' : [['/=',(2,'inhval'),('root','inhval'),(1,'inhval')]],
		'T\'' : [['=',('root','synval'),(1,'synval')]],
	},
	'F' : {
		'(' : [['=',(0,'inhval'),('root','inhval')]],
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
	node.lexval = token.val
	print("TOKENSET ", node.name, node.lexval)
	
def get_params(vals, root, children):
	tuples = vals[0][1:]
	num = len(tuples)
	params = []
	print("TP ", vals)
	print("tuples", tuples)
	print("children ", [c.name for c in children])
	for val in tuples:
		x = val[0]
		x_attr = val[1]
		print("x, x_attr", x, x_attr)
		if x == 'root':
			node_x = root
		else:
			node_x = children[x]
		params += [node_x, x_attr]
	return params	

def assign_producer_vals(symbol, rule, root):
	if root.name in assign:
		if symbol in assign[root.name]:
			vals = assign[root.name][symbol]
			children = root.get_children()
			print("here2 in assign_producer_vals with ", symbol, root.name, rule)
			print("here3 in assign_producer_vals", vals[0])
			op = vals[0][0]
			if op == '=':
				node_x, x_attr, node_y, y_attr = get_params(vals, root, children)			
				print("PARAMS ", node_x.name, x_attr, node_y.name, y_attr, rule)
				setattr(node_x, x_attr, getattr(node_y, y_attr))
				print("setting =", node_x.name, x_attr, getattr(node_y, y_attr), "under root ", root.name, "with rule ", rule)
			elif op == '+=':
				node_x, x_attr, node_y, y_attr, node_z, z_attr = get_params(vals, root, children)
				print("PARAMS ", get_params(vals, root, children))
				setattr(node_x, x_attr, (getattr(node_y, y_attr) + getattr(node_z, z_attr)))
				print("setting +=", node_x.name, x_attr, (getattr(node_y, y_attr) + getattr(node_z, z_attr)), "under root ", root.name, "with rule ", rule)
			elif op == '-=':
				node_x, x_attr, node_y, y_attr, node_z, z_attr = get_params(vals, root, children)
				setattr(node_x, x_attr, (getattr(node_y, y_attr) - getattr(node_z, z_attr)))
				print("setting -=", node_x.name, x_attr, (getattr(node_y, y_attr) - getattr(node_z, z_attr)), "under root ", root.name, "with rule ", rule)
			elif op == '*=':
				node_x, x_attr, node_y, y_attr, node_z, z_attr = get_params(vals, root, children)
				setattr(node_x, x_attr, (getattr(node_y, y_attr) * getattr(node_z, z_attr)))
				print("setting *=", node_x.name, x_attr, (getattr(node_y, y_attr) * getattr(node_z, z_attr)), "under root ", root.name, "with rule ", rule)
			elif op == '/=':
				node_x, x_attr, node_y, y_attr, node_z, z_attr = get_params(vals, root, children)
				setattr(node_x, x_attr, (getattr(node_y, y_attr) / getattr(node_z, z_attr)))
				print("setting /=", node_x.name, x_attr, (getattr(node_y, y_attr) / getattr(node_z, z_attr)), "under root ", root.name, "with rule ", rule)
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
					if True:#has_proceeded(temp, store):
						print("1.SYMBOL in RULE", symbol, rule)
						if not symbol == rule[-1]: #don't progress token if the symbol is the last in the list -> Error
							update(temp, store)
						assign_producer_vals(symbol, rule, root)
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
						print("2.SYMBOL in RULE", symbol, rule, root.name)
						assign_producer_vals(symbol, rule, root)
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
				elif (symbol == 'epsilon'):
					return True
				else:
					print("5. unmatched", symbol, temp.val)
					return False
		else:
			print ("unmatched exiting")
			return False
			
	return matched
			
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