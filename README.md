for_loop_mini_compiler
Read ME
--------
STEP 1:
	run:
		
		$python3 lex.py test/forteststruct.c
	
	for generating the tokens in the file
	2nd argument is the input c program
STEP 2:
	run:
		
		$python3 run_yacc.py	
	
	to generate the outputs
	
the outputs are in files:
	1.Parse Tree:
		parse_tree.txt
	2.AST
		astree.txt
		to see indented ast for forteststruct.c check pretty_astree.txt
	3.Symbol table
		symtab.txt
	4.Intermediate Code Generation(Quadriple):
		icg.txt
	