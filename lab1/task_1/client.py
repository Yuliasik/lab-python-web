#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import socket

host = '127.0.0.1'
port = 55556


def main():
    server_socket_connection = \
        socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket_connection.connect((host, port))

    while True:
        print(server_socket_connection.recv(1024).decode('utf-8'))

        a = input()

        server_socket_connection.send(a.encode('utf-8'))

        if a == '***':
            break

        print(server_socket_connection.recv(1024).decode('utf-8'))

    print('Connection closed!')


if __name__ == '__main__':
    main()
