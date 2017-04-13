from yacc import *

init_rules()
	
for item in sorted(productions.items()):
	print(item)
print("\n")
print([(tok.val, tok.type) for tok in token_list])
print("\n")
print("\n")


tree, quadruples, stack = start(token_list)
print("TREE")
print_tree(tree)
print("")

print("TSTRING", stringify(tree))

ast_tree = abstract_syntax_tree(tree)
print ("AST")
print_tree(ast_tree)

code = get_code([tree], [])

print("stack", [(s[2], getattr(s[0], s[1])) for s in stack])

if ('dummy1') in quadruples:
	quadruples[quadruples.index('dummy1')+1:quadruples.index('dummy2')], quadruples[quadruples.index('dummy2')+1:quadruples.index('dummy3')] = quadruples[quadruples.index('dummy2')+1:quadruples.index('dummy3')],quadruples[quadruples.index('dummy1')+1:quadruples.index('dummy2')]
	quadruples.remove(('dummy1'))
	quadruples.remove(('dummy2'))
	quadruples.remove(('dummy3'))

print("\n\nQuad")
for q in quadruples:
	print(q)

print("\n SYMTAB")
print(symtab)
for key,val in symtab.items():
	print(key,val)

#with open("symtab.txt", "w") as fp:
#	fp.write('\n'.join('%s\t%s' % x for x in symtab.items()))
#fp.close()

#with open("icg.txt", "w") as fp:
#	 fp.write('\n'.join('%s\t%s\t%s\t%s' % x for x in quadruples))
#fp.close()

#with open("parse_tree.txt", "w") as fp:
#	fp.write(stringify(tree))
#fp.close()

#with open("astree.txt", "w") as fp:
#	fp.write(stringify(ast_tree))
#fp.close()

