# Reference Code: https://github.com/jihoonog/CMPUT404-assignment-web-client/blob/master/httpclient.py

#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse, urlencode

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def parse_url(self,url):
        parsed_url = urlparse(url)

        host = parsed_url.hostname

        if parsed_url.port:
            port = parsed_url.port
        else:
            port = 80

        if parsed_url.path:
            path = parsed_url.path
        else:
            path = '/'
        
        return host, port, path

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code = int(data.split()[1])
        return code

    def get_headers(self,data):
        header = data.split('\r\n\r\n')[0]
        return header

    def get_body(self, data):
        body = data.split('\r\n\r\n')[1]
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""

        host, port, path = self.parse_url(url)
        self.connect(host, port)

        if args:
            body = urlencode(args)

        request_data = f'GET {path} HTTP/1.1\r\n'
        request_data += f'Host: {host}:{port}\r\n'
        request_data += "User-Agent: Sandip's Web Client\r\n"
        if len(body) == 0:
            request_data += 'Content-Length: 0\r\n'
        else:
            request_data += f'Content-Length: {len(body)}\r\n'
            request_data += 'Content-Type: application/x-www-form-urlencoded\r\n'
        request_data += 'Connection:close\r\n\r\n'
        request_data += body

        self.sendall(request_data)

        response_data = self.recvall(self.socket)
        self.close()

        print('**********[GET] request data**********')
        print('*****************START****************')
        print(request_data)
        print('******************END*****************')
        print()
        print('**********[GET] response data*********')
        print('*****************START****************')
        print(response_data)
        print('******************END*****************')
        print()

        header = self.get_headers(response_data)
        code = self.get_code(header)
        body = self.get_body(response_data)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""

        host, port, path = self.parse_url(url)
        self.connect(host, port)

        if args:
            body = urlencode(args)

        request_data = f'POST {path} HTTP/1.1\r\n'
        request_data += f'Host: {host}:{port}\r\n'
        request_data += "User-Agent: Sandip's Web Client\r\n"
        if len(body) == 0:
            request_data += 'Content-Length: 0\r\n'
        else:
            request_data += f'Content-Length: {len(body)}\r\n'
            request_data += 'Content-Type: application/x-www-form-urlencoded\r\n'
        request_data += 'Connection:close\r\n\r\n'
        request_data += body

        self.sendall(request_data)

        response_data = self.recvall(self.socket)
        self.close()
        
        print('**********[POST] request data**********')
        print('*****************START*****************')
        print(request_data)
        print('******************END******************')
        print()
        print('**********[POST] response data*********')
        print('*****************START*****************')
        print(response_data)
        print('******************END******************')
        print()

        header = self.get_headers(response_data)
        code = self.get_code(header)
        body = self.get_body(response_data)

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
