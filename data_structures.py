import operator

ops = {
	'+' : operator.add,
	'-' : operator.sub,
	'*' : operator.mul,
	'/' : operator.truediv,
	'<' : operator.lt,
	'>' : operator.gt,
	'<=' : operator.le,
	'>=' : operator.ge,
	'==' : operator.eq,
	'!=' : operator.ne
}


symtab = dict()

rules = [
			"PROG: STATEMENT eof",
			"STATEMENT: FOR_LOOP_ST | COND_ST | IF_COND_ST | DEFN_ST | ASSIGN_ST | DECL_ST",
			"FOR_LOOP_ST: FOR_LOOP ST' ",
			"IF_COND_ST: IF_COND ST' ",
			"COND_ST: COND ST'",
			"ASSIGN_ST: ASSIGN ST' ",
			"ST': ST | epsilon",
			"DECL_ST: DECL ST' ",
			"DEFN_ST: DEFN ST' ",
			"ST: STATEMENT_ST ",
			"STATEMENT_ST: STATEMENT STMT' ",
			"STMT': ; ST | epsilon",
			"FOR_LOOP: for ( ASSIGN COND INCREMENT ) { STATEMENT }",
			"INCREMENT: I_ASSIGN | I_COND | EXPRESSION",
			"IF_COND: if ( COND ) { STATEMENT ; } OP_ELSE | if ( COND ) { STATEMENT }",
			"OP_ELSE: else { STATEMENT } ",
			"ASSIGN: identifier = EXPRESSION ;",
			"DECL: type ID ;",
			"ID: identifier ID'",
			"ID': , identifier ID' | epsilon ", 			
			"DEFN: type ASSIGN",
			"COND: COND1 | COND2 | COND3 | COND4",
			"COND1: EXPRESSION1 < EXPRESSION2 ;",
			"COND2: EXPRESSION1 > EXPRESSION2 ;",
			"COND3: EXPRESSION1 <= EXPRESSION2 ;",
			"COND4: EXPRESSION1 >= EXPRESSION2 ;",
			"I_ASSIGN: identifier = EXPRESSION",
			"I_COND: EXPRESSION1 < EXPRESSION2 ; | EXPRESSION1 > EXPRESSION2 ; | EXPRESSION1 <= EXPRESSION2 ; | EXPRESSION1 >= EXPRESSION2 ;",
			"EXPRESSION1: EXPRESSION",
			"EXPRESSION2: EXPRESSION",
			"EXPRESSION: E",			
 			"E: T E'",
			"E': M E1' | M E2' | epsilon",
			"M: epsilon",
			"E1': + T E' | epsilon",
			"E2': - T E' | epsilon",
			"T: F T'",
			"T': M T1' | M T2' | epsilon",
			"T1': * F T' | epsilon",
			"T2': / F T' | epsilon",
			"F: ( E ) | identifier | number ",
		]

assign = {
	'DECL' : {
		'type' : [['=',(1, 'type'), (0, 'type')]],
		'identifier' : [[['enter', (1, 'type')]]]
	},
	'ASSIGN' : {
		'identifier' : [['=',(0,'type'),('root','inhval')]],
		'EXPRESSION' : [['=',(0,'val'),(2,'val')], ['addToST',(0, 'entry'), (0, 'val')]]
	},
	'D*ECL': {
		'type' : [['=',(1, 'inhval'),(0, 'type')]]
	},
	'ID': {
		'identifier' : [['=', (0, 'type'),('root', 'type')]]
	},
	'ID\'' : {
		'identifier' : [['=', (1,'type'),('root','type')], ['=',(2,'type'),('root','type')]]
	},
	'DEFN' : {
		'type' : [['=',(1, 'inhval'), (0, 'type')]]
	},
	'EXPRESSION1' : {
		'EXPRESSION' : [['=',('root','val'),(0,'val')], ['=', ('root', 'entry'),(0, 'entry')]]
	},
	'EXPRESSION2' : {
		'EXPRESSION' : [['=',('root','val'),(0,'val')], ['=', ('root', 'entry'),(0, 'entry')]]
	},
	'EXPRESSION' : {
		'E' : [['=',('root','val'),(0,'synval')], ['=', ('root', 'entry'),(0, 'entry')]]
	},
	'COND1' : {
		'EXPRESSION2' : [['<',('root','val'),(0, 'val'),(2, 'val')]]
	},
	'COND2' : {
		'EXPRESSION2' : [['>',('root','val'),(0, 'val'),(2, 'val')]]
	},
	'COND3' : {
		'EXPRESSION2' : [['<=',('root','val'),(0, 'val'),(2, 'val')]]
	},
	'COND4' : {
		'EXPRESSION2' : [['>=',('root','val'),(0, 'val'),(2, 'val')]]
	},
	'E' : {
		'T' : [['=',(1,'inhval'),(0,'synval')], ['=', ('root', 'entry'),(0, 'entry')]],
		'E\'' : [['=', ('root','synval'),(1,'synval')], ['=', ('root', 'entry'),(0, 'entry')]]
	},
	'E\'': {
		'M': [['=',(1,'inhval'),('root','inhval')]],  # Changed all 0 to root here and  1 to 0
		'E1\'': [['=',('root','synval'),(1,'synval')], ['=', ('root', 'entry'),(0, 'entry')]],
		'E2\'': [['=',('root','synval'),(1,'synval')], ['=', ('root', 'entry'),(0, 'entry')]],
		'epsilon': [['=', ('root', 'synval'), ('root','inhval')]] 
	},
	'E1\'' : {
		'T' : [['+',(2,'inhval'),('root','inhval'),(1,'synval')]],
		'E\'' : [['=',('root','synval'),(2,'synval')], ['=', ('root', 'entry'),(0, 'entry')]],	
		'epsilon' : [['=', ('root', 'synval'), ('root', 'inhval')]]
	},
	'E2\'' : {
		'T' : [['-',(2,'inhval'),('root','inhval'),(1,'synval')], ['=', ('root', 'entry'),(0, 'entry')]],
		'E\'' : [['=',('root','synval'),(2,'synval')], ['=', ('root', 'entry'),(0, 'entry')]],
		'epsilon' : [['=', ('root', 'synval'), ('root', 'inhval')]]
	},
	'T' : {
		'F' : [['=',(1,'inhval'),(0,'synval')], ['=', ('root', 'entry'),(0, 'entry')]],
		'T\'' : [['=', ('root','synval'),(1,'synval')], ['=', ('root', 'entry'),(0, 'entry')]]
	},
	'T\'': {
		'M': [['=',(1,'inhval'),('root','inhval')]], # Changed all 0 to root here and 1 to 0
		'T1\'': [['=',('root','synval'),(1,'synval')], ['=', ('root', 'entry'),(0, 'entry')]],
		'T2\'': [['=',('root','synval'),(1,'synval')], ['=', ('root', 'entry'),(0, 'entry')]],
		'epsilon': [['=', ('root', 'synval'), ('root','inhval')]] 
	},
	'T1\'' : {
		'F' : [['*',(2,'inhval'),('root','inhval'),(1,'synval')], ['=', ('root', 'entry'),(0, 'entry')]],
		'T\'' : [['=',('root','synval'),(2,'synval')], ['=', ('root', 'entry'),(0, 'entry')]],	
		'epsilon' : [['=', ('root', 'synval'), ('root', 'inhval')]]
	},
	'T2\'' : {
		'F' : [['/',(2,'inhval'),('root','inhval'),(1,'synval')], ['=', ('root', 'entry'),(0, 'entry')]],
		'T\'' : [['=',('root','synval'),(1,'synval')], ['=', ('root', 'entry'),(0, 'entry')]],
		'epsilon' : [['=', ('root', 'synval'), ('root', 'inhval')]]
	},
	'F' : {
		'(' : [['=',(0,'inhval'),('root','inhval')]],
		')' : [['=',('root','synval'),(0,'synval')]],
		'identifier' : [['=',('root','synval'),(0,'val')], ['=', ('root', 'entry'),(0, 'entry')]],
		'number' : [['=',('root','synval'),(0,'lexval')]]
	},
	'FOR_LOOP' : {
		#'for' : [[]],
		'ASSIGN' : [['code', (2, 'code'), [('Label','_','_','L0')]]],
		'COND' : [['code', (3, 'code'), [('ifFalse','COND','_','L1'),('dummy1')]]],
		'INCREMENT' : [['code',(4,'code'),[('dummy2')]]],
		'STATEMENT' : [['code', (6, 'code'), [('dummy3')]]],
		'}' : [['code', (8, 'code'), [('goto','_','_','L0'),('Label','_','_','L1')]]]
	}
	
}

productions = dict()
