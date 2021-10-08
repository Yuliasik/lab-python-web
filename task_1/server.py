#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
from datetime import date, datetime

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

    _ = 'Hello, client. Input your message'
    client_socket_connection.send(_.encode('utf-8'))

    message = client_socket_connection.recv(1024).decode('utf-8')
    client_socket_connection.close()

    now = datetime.now()
    now = now.strftime("%d/%m/%y %H:%M")

    print('(' + now + ') :' + message)
    print('\n')
    current += 1

server_socket_connection.close()
print('All connections are used, goodbye!')
