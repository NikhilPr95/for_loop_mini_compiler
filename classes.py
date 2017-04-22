class Character:
	def set_val(self, string, index):
		if self.index >= self.stringlen:
			self.val = None
		else:
			self.val = string[self.index]

	def __init__(self, string, index):
		self.string = string
		self.stringlen = len(string)
		self.index = index
		self.set_val(self.string, self.index)
		
	def increment(self):
		self.increment_mult(1)
		
	def increment_mult(self, inc):
		self.index += inc
		self.set_val(self.string, self.index)
	
	def decrement(self):
		self.decrement_mult(1)
		
	def decrement_mult(self, dec):
		self.index -= dec
		self.set_val(self.string, self.index)
		
	def update(self, obj):
		self.index = obj.index
		self.set_val(self.string, obj.index)
			
class Token:
	def __init__(self, type, val):
		self.type = type
		self.val = val

class TokenList:
	def set_vals(self, index):
		self.type = self.token_list[index].type
		self.val = self.token_list[index].val
		
	def __init__(self, token_list, index):
		self.index = index
		self.token_list = token_list
		self.set_vals(index)
		
	def increment(self):
		self.index += 1
		self.set_vals(self.index)
		
	def decrement(self):
		self.index -= 1
		self.set_vals(self.index)
		
	def set_index(self, index):
		self.index = index
		self.set_vals(self.index)

class Tree:
	def __init__(self, name):
		self.name = name
		self.children = []
		self.parent = []
		self.entry = []
		self.val = None
		self.lexval = None
		self.synval = None
		self.inhval = None
		self.type = None
		self.inhtype = None
		self.entry = None
		self.tempname = None
		self.code = []
		
	def set_synthval(self, synthval):
		self.synthval = synthval
	
	def set_entry(self, entry):
		self.entry = entry
		
	def set_children(self, children_names):
		for child_name in children_names:
			child_node = Tree(child_name)
			child_node.set_parent(self)
			self.children.append(child_node)

	def  set_child(self,c):
		c.set_parent(self)
		self.children.append(c)
		
	
	def set_parent(self, parent):
		self.parent = parent

	def get_children(self):
		return self.children

	def get_parent(self):
		return self.parent
		
	def delete_children(self):
		for child in self.children:
			child.delete_children()
		self.children = []

	def delete_child(self, child):
		if child in self.children:
			self.children.remove(child)
			
	def node_copy(self):
		new_node = Tree(self.name)
		new_node.entry = self.entry
		new_node.val = self.val
		new_node.lexval = self.lexval
		new_node.synval = self.synval
		new_node.inhval = self.inhval
		new_node.type = self.type
		new_node.inhtype = self.inhtype
		new_node.entry = self.entry
		new_node.code = self.code

		return new_node
