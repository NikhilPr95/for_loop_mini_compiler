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
			"DEFN: type identifier = EXPRESSION ;",
			"COND: EXPRESSION1 relational_operator EXPRESSION2 ;",
			"I_ASSIGN: identifier = EXPRESSION",
			"EXPRESSION1: EXPRESSION",
			"EXPRESSION2: EXPRESSION",
			"EXPRESSION: E",
			"E: T E' | T",
			"E': + T E' | - T E'", # | epsilon",
			"T: F T' | F",
			"T': * F T' | / F T'", # | epsilon",
			"F: G ^ F | G",
			"G: ( E ) | identifier | number "
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
	return store.index > start.index
	
def is_producer(symbol):
	return symbol.isupper()

def is_token(symbol):
	return symbol in token_types

def match_token(token, store, symbol):
	print("in match token", token.val, token.type, symbol)
	if token.type == symbol:
		store.set_index(token.index + 1)		
		return True
	return False
	
def is_tuple(symbol):
	return symbol[0] == '(' and symbol[-1] == ')'
	
def is_valid(rule, productions, token, store, stack, root):
	temp = TokenList(token_list,0)
	update(temp, token)
	matched = True
	children = root.get_children()
	for i in range(len(rule)):
		symbol = rule[i]
		child = children[i]
		print("in symbol", symbol, "\t\t(in rule ", rule, ")")			
		if matched:
			if is_producer(symbol):
				print("in producer")
				if match_rule(temp, store, productions, symbol, stack, child):
					if has_proceeded(temp, store):
						print("1.SYMBOL in RULE", symbol, rule)
						if not symbol == rule[-1]:# and rule[rule.index(symbol) + 1] != 'eof':
							update(temp, store)
						print("1. temp store", temp.val, store.val)					
					else:
						print("1. unmatched", symbol, temp.val, store.val, rule)
						return False
				else:
					print("2. unmatched", symbol, temp.val, store.val, rule)
					#stack.pop()
					return False
			elif is_token(symbol):
				print("is token")
				if match_token(temp, store, symbol):
					if has_proceeded(temp, store):
						#print("2.SYMBOL in RULE", symbol, rule)
						if not symbol == rule[-1]:# and rule[rule.index(symbol) + 1] != 'eof':
							update(temp, store)
						print("matched")
						print("2. temp store", temp.val, store.val)
					else:
						print("3. unmatched not proceeded", symbol, temp.val)
						#stack.pop()
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
	
def print_stack(stack):
	x=1
	n = stack.count('(((')
	i = 0	
	while i < (len(stack)):
		print_tabs(n)
		if not stack[i] == '(((':
			while (stack[i] != ')))'):
				print(stack[i], end = "")
				i += 1
			n -= 1
		else:
			i += 1

def print_tree(root):
	print(root.val, end= " ")
	if is_producer(root.val) and root.children:
		print("(", end = "")
	for child in root.children:
		print_tree(child)
	if is_producer(root.val) and root.children:
		print(")", end = " ")

def list_indent_stack(stack):
	li = []
	for element in stack:
		if element == '(((':
			li.append(list_indent_stack)
			
def match_rule(token, store, productions, producer, stack, root):
	print("in match rule with ", producer, ":", productions[producer])
	for rule in productions[producer]:
		print("in rule ", rule, " with ", token.val)
		#stack.append('(((')
		stack.append(rule)
		root.set_children(rule)	
		print("TREE")
		print_tree(root)
		print("")
		print("STACK ", stack)
		if (is_valid(rule, productions, token, store, stack, root)):
			print("here we are", rule, productions[producer], productions[producer].index(rule))#, productions[producer][productions[producer].index(rule)])
			#stack.append(rule)
		#	stack.append(')))')
			return True
		else:
			x = None
			#while(x != '((('):#
			while(rule != x):
				x = stack.pop()
	#			print("Popped ", x," with rule ", rule)
			#x = stack.pop()
			#print("Popped ", x," with rule ", rule)
			print("STACK ", stack)
			print("returned false ", rule, productions[producer])
	
	return False
			
def start(token_list):
	eof = Token('eof', 'eof')
	token_list.append(eof)
	token = TokenList(token_list, 0)
	store = TokenList(token_list,0)
	stack = []

	root = Tree("PROG")
	#stack.append('(((')
	stack.append("PROG")
	print("TREE")
	print_tree(root)
	print("")
	print("STACK ", stack)
	if match_rule(token, store, productions, "PROG", stack, root):
		print("VALID", token.val, store.val)
	else:
		print("ERROR", token.val, store.val)

	print("TREE")
	print_tree(root)
	print("")
	
	return stack
	#stack.append(')))')
		
def init_rules():	
	for rule in rules:
		#print(rule.split(":"))
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


stack = start(token_list)

print("STACK ----")
print(stack)
#print_stack(stack)
#print("ttt",token_types)
