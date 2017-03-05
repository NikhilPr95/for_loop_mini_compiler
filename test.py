def outer(string):
	def inner(ch):
		if (ch == '='):
			return 2
		else:
			return -2
			
	if (string[0] == '='):
		inner(string[1])

print(outer('=='))