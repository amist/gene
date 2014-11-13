from bottle import route, run, request

@route('/')
def hello():
	return """
Usage: PUT request to /request
"""

@route('/request', method='PUT')
def post():
	id = request.query.getall('id')
	src = request.query.getall('src')
	dest = request.query.getall('dest')
	time = request.query.getall('time')
	add_request(id, src, dest, time)
	return "POST succeeded"

def add_request(id, src, dest, time):
	requests.append((id, src, dest, time))

requests = []
if __name__ == '__main__':
	run(host='localhost', port=8080, debug=True)