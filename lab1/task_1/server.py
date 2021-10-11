#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
from datetime import datetime
import time

host = '127.0.0.1'
port = 55556

server_socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket_connection.bind((host, port))

number_connections = int(input('Enter number of connections: '))
current = 0

while current < number_connections:
    server_socket_connection.listen(2)
    print('Active server! waiting for connections:')

    client_socket_connection, addr = server_socket_connection.accept()
    print('Got a connection from {}'.format(addr))

    _ = 'Hello, client. Input your message. Input *** to close connection'

    while True:
        client_socket_connection.send(_.encode('utf-8'))

        message = client_socket_connection.recv(1024)

        now = datetime.now()
        now = now.strftime("%d/%m/%y %H:%M:%S")

        print('(' + now + ') :' + message.decode('utf-8'))

        if message.decode('utf-8') == '***':
            client_socket_connection.close()
            break

        time.sleep(5)

        now = datetime.now()
        now = now.strftime("%d/%m/%y %H:%M:%S")
        print('(' + now + ') : RESPONSED TO CLIENT')

        client_socket_connection.send(message)

    print('\n')
    current += 1
    
server_socket_connection.close()    
print('All connections are used, goodbye!')
