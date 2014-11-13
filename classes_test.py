class user_class:
	def __init__(self):
		self.val = 42
		
	def do_something(self):
		print 'In user_class. The value is %d' % self.val
	
class exec_class:
	def __init__(self, user_class):
		self.user_class = user_class
		
	def get_solution(self):
		ni = eval(self.user_class.__name__)()
		ni.do_something()
		ni.val = 44
		return ni

if __name__ == '__main__':
	print 'starting...'
	uc1 = user_class()
	ec = exec_class(user_class)
	uc2 = ec.get_solution()
	print uc1.val
	print uc2.val
	print 'finish'