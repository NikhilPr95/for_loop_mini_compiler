class Character:
	def set_val(self, string, index):
		self.val = string[self.index]

	def __init__(self, string, index):
		self.string = string
		self.stringlen = len(string)
		self.index = index
		self.set_val(self.string, self.index)
		
	def increment(self):
		self.increment_mult(1)
		
	def increment_mult(self, inc):
		if (self.index + inc) >= self.stringlen:
			return -1
		self.index += inc
		self.set_val(self.string, self.index)
	
	def decrement(self):
		self.decrement_mult(1)
		
	def decrement_mult(self, dec):
		self.index -= dec
		self.set_val(self.string, self.index)

class Token:
	def __init__(self, type, val):
		self.type = type
		self.val = val
