#! /usr/bin/env python3
# -*- coding:utf-8 -*-

from http.server import HTTPServer, CGIHTTPRequestHandler


def start_server(port=8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    start_server()
