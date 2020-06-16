## Instructions

#### STEP 1:
For generating the tokens in the file; 2nd argument is the input c program
```	
python3 lex.py test/forteststruct.c
```
##### STEP 2:
To generate the outputs
```		
python3 run_yacc.py	
```		
#### STEP 3:
The outputs are in files:
```
1.Parse Tree: parse_tree.txt
2.AST: astree.txt (to see indented ast for forteststruct.c check pretty_astree.txt)
3.Symbol table: symtab.txt
4.Intermediate Code Generation(Quadriple): icg.txt
```
