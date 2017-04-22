import pickle
import itertools
import copy
from classes import *
from data_structures import *

with open('tokens.pkl', 'rb') as fp:
		token_list = pickle.load(fp)

with open('token_types.pkl', 'rb') as fp:
		token_types = pickle.load(fp)

temps = ['t1','t2','t3','t4','t5','t6','t7','t8','t9']
t = 0

def tempGen():
	global t
	t += 1
	return ("t"+str(t))

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

def assign_token_vals(token, node, quadruples):
	if node.name == 'type':
		node.type = token.val
		print("TOKENSET ", node.name, node.type)
	elif node.name == 'identifier':
		node.entry = token.val
	else:
		node.lexval = token.val
		print("TOKENSET ", node.name, node.lexval)

def get_params(vals, root, children):
	tuples = vals[1:]
	num = len(tuples)
	params = []
	print("TP ", vals)
	for val in tuples:
		x = val[0]
		x_attr = val[1]
		if x == 'root':
			node_x = root
		else:
			node_x = children[x]
		params += [node_x, x_attr]
	return params

def get_val(node, attr):
	val = getattr(node, attr)
	print("val", val)
	if type(val) == str and attr not in ['entry','tempname']:
		return eval(val)
	return val

def is_empty(li):
	return len(li) == 0

#"""
def assign_producer_vals(symbol, rule, root, quadruples, stack):
	if root.name in assign:
		if symbol in assign[root.name]:
			values = assign[root.name][symbol]
			children = root.get_children()
			print("here2 in assign_producer_vals with ", symbol, root.name, rule)
			for vals in values:
				print("here3 in assign_producer_vals", vals)
				op = vals[0]
				if op == '=':		
					node_x, x_attr, node_y, y_attr = get_params(vals, root, children)			
					print("ENTRYYY", node_x.name, getattr(node_x, 'entry'))					
					print("ENTRYYY", node_y.name, getattr(node_y, 'entry'))
					print(symtab)
					y_val = get_val(node_y, y_attr)
					if getattr(node_y, 'entry'):
						y = getattr(node_y, 'entry')
						print("y=", y)						
						if x_attr == 'entry':
							y_val = y
						else:
							if y in symtab:
								y_val = symtab[y]

					setattr(node_x, x_attr, y_val)
					if x_attr in ['val']:
						if node_x.entry in symtab:
							print("nodex entry", node_x.entry, x_attr, y_val)
							symtab[node_x.entry] = y_val						

					#if True:#
					if x_attr in ['val']:
						#if True:#
						if root.name not in ['EXPRESSION2', 'EXPRESSION1','EXPRESSION']:
							if True:#if node_x.name == 'identifier':
								if (is_empty(stack)):
									y = getattr(node_y, y_attr)
								else:
									y = node_y.name

								if getattr(node_y, 'tempname') == None:					
									if getattr(node_y, 'entry'):
										y = getattr(node_y, 'entry')
										y_val = symtab[y]
								else:
									y = getattr(node_y, 'tempname')
								
								#y = node_y.name		
								print("y_val", y_val)
								tup = ('=', y,'_', node_x.entry)
							else:
								tup = ('=', y, '_', node_x.name)#, rule, root.name)
							print("QUAD ", tup)
							quadruples.append(tup)
							root.code.append(tup)
					print("PARAMS ", node_x.name, x_attr, node_y.name, y_attr, rule)
					print("setting =", node_x.name, x_attr, y_val, "under root ", root.name, "with rule ", rule, "with symbol", symbol)
					print_tree(node_x.parent)
				
				elif op in ['+', '-', '*', '/', '<', '>', '<=', '>=', '==', '!=']:

					node_x, x_attr, node_y, y_attr, node_z, z_attr = get_params(vals, root, children)
					y_val, z_val = get_val(node_y, y_attr), get_val(node_z, z_attr)

					print("PARAMS ", node_x.name, x_attr, node_y.name, y_attr, node_z.name, z_attr)
					
					global t
					
					if is_empty(stack):
						y, z = getattr(node_y, y_attr), getattr(node_z, z_attr)					
						print("stak1.")
					else:
						y, z = getattr(node_y, y_attr), node_z.name
						print("stak2.")
					
					#y, z = node_y.name, node_z.name

					print("y_attr", y_attr)
					if(getattr(node_y, 'entry')):
						print('true', getattr(node_y, 'entry'))
					
					if getattr(node_y, 'tempname') == None:					
						if getattr(node_y, 'entry'):
							y = getattr(node_y, 'entry')
							y_val = symtab[y]
					else:
						y = getattr(node_y, 'tempname')

					if getattr(node_z, 'tempname') == None:
						if getattr(node_z, 'entry'):
							z =getattr(node_z, 'entry')
							z_val = symtab[z]
					else:
						z = getattr(node_z, 'tempname')

					print("vals ", y_val, z_val)
						
					
					node_x.tempname = tempGen()
					x = node_x.tempname
					root.tempname = x
					print("TEMPSET", node_x.name, x)
					print("TEMPSET", root.name, x)
					tup = (op, y, z, x)
					print("QUAD", tup)
					print("ENTRYYY", node_x.name, getattr(node_x, 'entry'))					
					print("ENTRYYY", node_y.name, getattr(node_y, 'entry'))
					print("ENTRYYY", node_z.name, getattr(node_z, 'entry'))


					setattr(node_x, x_attr, ops[op](y_val, z_val))
					if node_x.entry in symtab:
						print("nodex entry", node_x.entry, x_attr, ops[op](y_val, z_val))
						symtab[node_x.entry] = ops[op](y_val, z_val)
					print("setting", op, node_x.name, x_attr, ops[op](y_val, z_val), "under root ", root.name, "with rule ", rule, "with symbol", symbol)		

					quadruples.append(tup)
					root.code.append(tup)
					print_tree(node_x.parent)

				elif op == 'code':
					print("in CODE", vals)
					for code in vals[2]:
						#if code[0] == 'ifFalse':
							#code = (code[0], root.tempname, code[2], code[3])
							#code[1] = root.tempname
						quadruples.append(code)	

				elif op == 'addToST':
					print("in add Symbol", vals)
					node_y, y_attr, node_z, z_attr = get_params(vals, root, children)
					print("PARAMS ", node_y.name, y_attr, node_z.name, z_attr)
					y_val, z_val = get_val(node_y, y_attr), get_val(node_z, z_attr)
					print("vals ", y_val, z_val)
					symtab[y_val] = z_val

		else:
			print("2. prod", symbol, "not in ", assign[root.name])
	else:
		print("1. prod ", root.name, "not in assign")

"""
def assign_producer_vals(a,b,c):
	x=1
#"""

def match_token(token, store, symbol, node, quadruples):
	print("in match token", token.val, token.type, symbol)
	if token.type == symbol:
		assign_token_vals(token, node, quadruples)
		store.set_index(token.index + 1)	
		return True
	return False
	
def is_tuple(symbol):
	return symbol[0] == '(' and symbol[-1] == ')'


def print_tabs(n):
	print(n*' ', end = " ")


def stringify(root):
	return string_the_tree(root, "")

def string_the_tree(root, string):
	string += root.name +" "
	if root.children:
		string += " ["
	for child in root.children:
		string = string_the_tree(child, string)
	if root.children:
		string += "] "
	
	return string

def print_tree(root):
	print_the_tree(root)
	#print("")

def print_the_tree(root):
	print(root.name, end= " ")
	if root.children:
		print("[", end = "")
	for child in root.children:
		print_the_tree(child)
	if root.children:
		print("]", end = " ")

def is_epsiloned():
	x=1

def is_valid(rule, productions, token, token_list, store, root, quadruples, stack):
	temp = TokenList(token_list,0)
	update(temp, token)
	matched = True
	check = TokenList(token_list, temp.index)
	children = root.get_children()
	for i in range(len(rule)):
		symbol = rule[i]
		child = children[i]
		print("SYMBOL ", symbol)
		print("in symbol", symbol, "\t\t(in rule ", rule, ")")			
		if matched:
			if is_producer(symbol):
				print("in producer")
				print("check is now ", check.val)
				if match_rule(temp, token_list, store, productions, symbol, child, quadruples, stack): # add back rule - if not epsilon has to have proceeded or invalid
					if has_proceeded(check, store) or symbol == 'M':
						print("1.SYMBOL in RULE", symbol, rule)
						if not symbol == rule[-1]: #don't progress token if the symbol is the last in the list -> Error
							update(temp, store)
							print("1. updated ", temp.val, store.val)
							print("1. NOT LAST")
							assign_producer_vals(symbol, rule, root, quadruples, stack)
						print("1. temp store", temp.val, store.val)					
					else:
						print("has not proceeded ", check.val, store.val)
						print("1. unmatched", symbol, temp.val, store.val, rule)
						return False
				else:
					print("2. unmatched", symbol, temp.val, store.val, rule)
					return False
			elif is_token(symbol):
				print("is token")
				if match_token(temp, store, symbol, child, quadruples):
					if has_proceeded(temp, store) :#or symbol == 'epsilon':
						print("2.SYMBOL in RULE", symbol, rule, root.name)
						if not symbol == rule[-1]:
							update(temp, store)
							print("2. updated ", temp.val, store.val)
							print("3. NOT LAST")
							assign_producer_vals(symbol, rule, root, quadruples, stack)
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
						print("3. updated ", temp.val, store.val)
						print("matched")
				elif (symbol == 'epsilon'):
					print ("epsilon matched")
					return True
				else:
					print("5. unmatched", symbol, temp.val)
					return False
		else:
			print ("unmatched exiting")
			return False
			
	return matched
			
def match_rule(token, token_list, store, productions, producer, root, quadruples, stack):
	print("in match rule with ", producer, ":", productions[producer])
	for rule in productions[producer]:
		print("in rule ", rule, " with ", token.val)
		root.set_children(rule)
		print("TREE")
		print_tree(root)
		print("")

		if (is_valid(rule, productions, token, token_list, store, root, quadruples, stack)):
			print("here we are", rule, productions[producer], productions[producer].index(rule), rule)
			symbol = rule[-1]
			print("2. LAST", rule)
			assign_producer_vals(symbol, rule, root, quadruples, stack)
			print("done")
			return True
		else:
			x = None
			root.delete_children()
			print("TREE")
			print_tree(root)
			print("")
			print("returned false ", rule, productions[producer])
	
	return False

def has_redundant_child(node):
	return len(node.children) == 1 and (len(node.children[0].children) != 0)

def has_redundant_nonop_child(node):
	if has_redundant_child(node):
		child = node.children[0]
		return has_redundant_child(child) and child.children[0].name not in ['+','-','*','/']
	
	return False

def has_no_real_descendant(node):	
	while(len(node.children) > 0 and has_redundant_child(node)):		
		node = node.children[0]

	if len(node.children) > 0 and node.children[0].name == 'epsilon':
		return True		
	return False

def set_children(child, ast_node):
	ast_child = child.node_copy()
	ast_child.parent = ast_node
	ast_node.children.append(ast_child)
	return ast_child

def remove_dead_paths(node, ast_node):
	for child in node.children:
		if not has_no_real_descendant(child) :#and child.name not in ['eof', ';']:
			ast_child = set_children(child, ast_node)
			remove_dead_paths(child, ast_child)

def remove_redundant_intermediates(node, ast_node):
	if has_redundant_child(node):
		#print("has has_redundant_child", node.name)
		remove_redundant_intermediates(node.children[0], ast_node)
		#remove_redundant_intermediates(node.parent, ast_node.parent)
	else:
		for child in node.children:
			ast_child = set_children(child, ast_node)
			remove_redundant_intermediates(child, ast_child)

def is_operator(node):
	return node.name in ['+', '-', '*', '/']

def is_equal(node):
	return node.name in ['=']

def is_relop(node):
	return node.name in ['<','>','<=','>=']

def get_niece(node):
	try:
		index = node.parent.children.index(node)
		return node.parent.children[index-1].children[0]
	except:
		print("FAIL NIECE", node.name, [c.name for c in node.children])
		print("NIECE PARENT", node.parent.name, [c.name for c in node.parent.children])

def elevate_operators(node):
	for child in node.children:
		if is_operator(child):
			niece = get_niece(node)
			node.name = child.name
			node.delete_child(child)
			node.children = [niece] + node.children
			niece.parent = node
			node.parent.delete_child(node.parent.children[0])
		elevate_operators(child)
        
def remove_single_node_tree(node):
	if len(node.children) == 1:
		print("hello")
		print("Parent",node.name)
		for i in node.children:
			print("Children",i.name)
	
		if is_producer(node.name):
			print("im here")
			x = node.name
			node.name = node.children[0].name
			print("changing name to ", x, node.name)
			for i in node.children[0].children:
				node.set_child(i)
				remove_single_node_tree(i)
			node.delete_child(node.children[0])
			for i in node.children:
				print("Children",i.name)
		else:
			remove_single_node_tree(node.children[0])
	else:
		for i in node.children:
			remove_single_node_tree(i)


def apply_equal(node):
	for child in node.children:
		if is_equal(child) or is_relop(child):
			node.name = child.name
			node.delete_child(child)
		apply_equal(child)

def remove_redundant_number_producers(node):
	if is_operator(node):
		for child in node.children:
			if len(child.children) == 1:
				if child.children[0].name == 'number' and len(child.children[0].children) == 0:
					child.name = child.children[0].name
					child.delete_children()					
	for child in node.children:
		remove_redundant_number_producers(child)

def abstract_syntax_tree(root):
	ast_root = root.node_copy()
	remove_dead_paths(root, ast_root)
	print("step 1")
	print_tree(ast_root)
	print("")
	ast_root2 = ast_root.node_copy()
	remove_redundant_intermediates(ast_root, ast_root2)
	print("step 2")
	print_tree(ast_root2)
	print("")
	elevate_operators(ast_root2)
	apply_equal(ast_root2)
	print("step 3")
	print_tree(ast_root2)
	print("")	
	remove_single_node_tree(ast_root2)
	print("step4")
	print_tree(ast_root2)	
	return ast_root2

def get_code(node_queue, code):
	if node_queue:
		children = []
		for node in node_queue:
			#print("getcode", node.name)
			if len(node.code):
				for c in node.code:
					code.insert(0,c)
					print("inserting c", c)
			children += node.children
		get_code(children, code)
	return code

def remove_comments(li):
	
	for t in li:
		print(t.type)
	print ([(t.type, t.val) for t in li])
	print ([(t.type, t.val) for t in li if t.type != 'comment'])

	print("remove ocmment")

	return [t for t in li if t.type != 'comment']

def start(token_list):
	eof = Token('eof', 'eof')
	token_list.append(eof)
	token_list = remove_comments(token_list)
	print("tokenlist", [t.type for t in token_list])
	token = TokenList(token_list, 0)
	store = TokenList(token_list,0)
	root = Tree("PROG")

	quadruples = []
	stack = []

	print("TREE")
	print_tree(root)
	print("")
	
	if match_rule(token, token_list, store, productions, "PROG", root, quadruples, stack):
		print("VALID", token.val, store.val)
	else:
		print("ERROR", token.val, store.val)
	
	print("stack", stack)
	return root, quadruples, stack
		
def init_rules():	
	for rule in rules:
		symbol, prod = rule.split(":")
		for p in prod.split("|"):
			add(productions, symbol, p.strip())			