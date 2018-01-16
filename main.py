from socket import *
import threading
import sys

server_name = 'http24'
port = 8080

def setup_server(application):
    print 'Launched {} server.'.format(server_name)
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)
    print('Bound @ {} and listening'.format(str(port)))

    run_server = True

    while run_server:
        cs, user_addr = server_socket.accept()

        environ = {}

        request = cs.recv(1024)
        requestlns = request.splitlines()
        primary = requestlns[0]

        primons = primary.split()
        method = primons[0]
        page = primons[1][1:]

        if page == '': page = '/'
        print 'method,', method, '::', 'requested,',page

        environ['wsgi.errors'] = sys.stderr
        environ['wsgi.input'] = None
        environ['wsgi.multiprocess'] = False
        environ['wsgi.multithread'] = False
        environ['wsgi.url_scheme'] = 'http'
        environ['wsgi.version'] = (1,0)
        environ['wsgi.run_once'] = False

        environ['REQUEST_METHOD'] = method
        environ['PATH_INFO'] = page
        environ['SERVER_NAME'] = 'localhost'
        environ['SERVER_PORT'] = str(port)
        environ['CONTENT_LENGTH'] = len(request)

        def start_response(status, response_headers):
            global out_status
            global out_response

            out_status = status
            out_response = response_headers

        rbody = ''
        content = application(environ, start_response)
        for i in content:
            rbody += i + '\n'

        response = 'HTTP/1.0 200 OK \n'
        for header in out_response:
            response += header[0] +': ' + header[1] + '\n'
        response += 'Connection: close\n'
        response += '\n\n'
        response += rbody
        cs.send(response)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Requires a WSGI application to be provided.')

    app = sys.argv[1]
    module_name, app_field = app.split(':')

    module = __import__(module_name)
    application = getattr(module, app_field)

    print 'Module: ' + module_name + ' | App: ' + app_field + ' | Loaded'
    setup_server(application)

