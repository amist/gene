import serv
from population import Population

def test_add_request():
	serv.requests = []
	serv.add_request('idid', 'sss', 'ddd', 'ttt')
	assert serv.requests[0] == ('idid', 'sss', 'ddd', 'ttt')
	
def test_unimplemented():
	population = Population()
	try:
		population.expand_population(1, 1)
		assert False
	except NotImplementedError:
		assert True
	
	try:
		population.sort_population()
		assert False
	except NotImplementedError:
		assert True
	
	try:
		population.distinct_population()
		assert False
	except NotImplementedError:
		assert True
	
	try:
		population.cut_population()
		assert False
	except NotImplementedError:
		assert True
	
if __name__ == '__main__':
	test_add_request()
	test_unimplemented()
	