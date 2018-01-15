from socket import *
import threading
import sys

print 'Launched http server'
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(10)

print('Bound and listening.')

while True:
    cs, user_addr = server_socket.accept()
    #print 'New connection from', user_addr[0]

    request = cs.recv(1024)
    req_lines = request.split('\n')

    method = req_lines[0].split()[0]

    page = req_lines[0].split()[1][1:]
    if page == '/' or page == '': page = 'index.html'
    print 'method,', method, ' ', 'requested,',page

    f = open(page, 'r')
    html = f.read().encode('utf-8')
    length = len(html)

    response = 'HTTP/1.0 200 OK\n'
    response += 'Server: Custom\n'
    response += 'Content-Type: text/html; charset=utf-8\n'
    response += 'Content-Length: ' + str(length) + '\n'
    response += 'Connection: close\n\n' 
    if method == 'GET':
        response += html + '\n'

    cs.send(response)