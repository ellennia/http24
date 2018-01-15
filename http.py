from socket import *
import threading
import sys

'''
    Implemented:
        - GET
        - HEAD
'''

server_name = 'http24'
port = 8080

print 'Launched {} server.'.format(server_name)
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('localhost', port))
server_socket.listen(1)

print('Bound @ {} and listening'.format(str(port)))

def test_application(environ, start_response):
    pass

run_server = True
while run_server:
    cs, user_addr = server_socket.accept()

    environ = {}

    request = cs.recv(1024)
    requestlns = request.splitlines()

    primons = primary.split()
    method = primons[0]
    page = primons[1][1:]

    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.input'] = sys.stdin.buffer
    environ['wsgi.multiprocess'] = False
    environ['wsgi.multithread'] = False
    environ['wsgi.version'] = (1,0)
    environ['wsgi.run_once'] = False

    environ['REQUEST_METHOD'] = method
    environ['PATH_INFO'] = page
    environ['SERVER_NAME'] = 'http24'
    environ['SERVER_PORT'] = str(port)
    environ['CONTENT_LENGTH'] = len(request)

    print 'method,', method, ' :: ', 'requested,',page

    out_status = None
    out_response = None

    def start_response(status, response_headers):
        out_status = status
        out_response = response_headers

    content = application(environ, start_response)

    response = 'HTTP/1.0' + out_status + '\n'
    response += content
    cs.send(response)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Requires a WSGI application to be provided.')
