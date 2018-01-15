from socket import *
import threading
import sys

'''
    Implemented:
        - GET
        - HEAD
'''

server_name = 'http24'

print 'Launched {} server.'.format(server_name)
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(10)

print('Bound and listening')

run_server = True
while run_server:
    cs, user_addr = server_socket.accept()

    request = cs.recv(1024)
    req_lines = request.split('\n')

    method = req_lines[0].split()[0]

    page = req_lines[0].split()[1][1:]
    if page == '/' or page == '': page = 'index.html'
    print 'method,', method, ' ', 'requested,',page

    if method == 'GET' or method == 'HEAD':
        f = open('templates/' + page, 'r')
        html = f.read().encode('utf-8')
        length = len(html)
        response = 'HTTP/1.0 200 OK\n'
        response += 'Server: {}\n'.format(server_name)
        response += 'Content-Type: text/html; charset=utf-8\n'
        response += 'Content-Length: ' + str(length) + '\n'
        response += 'Connection: close\n\n' 
        if method == 'GET':
            response += html + '\n'
        cs.send(response)
    elif method == 'POST':
        print request

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Requires a WSGI application to be provided.')
