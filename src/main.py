'''
    http24

    A single-threaded WSGI HTTP server created, with the exception of some tweaks, in 24 hours.
'''

from socket import *
import sys

server_name = 'http24'
port = 80

def setup_server(application):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)
    print('Server bound on port {} and listening'.format(str(port)))
    print('-------------------------------------------------')

    run_server = True
    while run_server:
        conn, user_addr = server_socket.accept()

        request = conn.recv(1024)
        (method, page, status) = request.splitlines()[0].split()
        if page == '': page = '/'
        print 'Method,', method, '|', 'Page requested:',page

        environ = {}
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
            
        html_content = ''
        content = application(environ, start_response)
        for i in content:
            html_content += i + '\n'
        response = 'HTTP/1.0 '+ out_status + '\n'
        for header in out_response:
            response += header[0] +': ' + header[1] + '\n'
        response += 'Connection: close\n'
        response += '\n\n'
        response += html_content
        conn.send(response)
        conn.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('http24 requires a WSGI application to be provided as an argument.')

    app = sys.argv[1]
    module_name, app_field = app.split(':')

    module = __import__(module_name)
    application = getattr(module, app_field)

    print 'Module: ' + module_name + ' | App: ' + app_field + ' | Loaded'
    setup_server(application)

