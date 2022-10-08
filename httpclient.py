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
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=500, body=''):
        self.code = code
        self.body = body

class HTTPClient(object):

    def get_host_port(self,url):
        # We initialize an empty list called "host_port" and then we parse the url to get the hostname and port number and store them in the list
        # (host name first and then port number). We then return them both in the list 

        host_port = ['127.0.0.1', 80]
        url_host = urllib.parse.urlparse(url).hostname
        url_port = urllib.parse.urlparse(url).port

        if url_host != None:
            host_port[0] = url_host
            remote_ip = socket.gethostbyname(host_port[0])
            host_port[0] = remote_ip

        if url_port != None:
            host_port[1] = url_port

        return host_port

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        response_list = data.split(" ")
        code = int(response_list[1])
        return code

    def get_headers(self,data):
        response_list = data.split("\r\n\r\n")
        header = response_list[0]
        return header

    def get_body(self, data):
        response_list = data.split("\r\n\r\n")
        body = response_list[1]
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

        try:
            host_port = self.get_host_port(url)
            host = host_port[0]
            port = host_port[1]
            self.connect(host, port) 

            full_url = url
            content_type = ""
            content_len = 0

            if args != None:
                params = urllib.parse.urlencode(args)
                content_type = "application/x-www-form-urlencoded"
                content_len = len(params)
                full_url += "?" + params

            payload = f'GET /{full_url} HTTP/1.1\r\nHost: {host}\r\nContent-type: {content_type}\r\nContent-length: {content_len}\r\n\r\n'
            self.sendall(payload)
            response = self.recvall(self.socket)

            code = self.get_code(response)
            body = self.get_body(response)

        except Exception as e:
            print(e)

        finally:
            #always close at the end!
            self.close()

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""

        try:
            host_port = self.get_host_port(url)
            host = host_port[0]
            port = host_port[1]
            self.connect(host, port)

            full_url = url
            content_type = ""
            content_len = 0
            params = ""

            if args != None:
                params = urllib.parse.urlencode(args)
                content_type = "application/x-www-form-urlencoded"
                content_len = len(params)
                full_url += "?" + params
                body = str(args) + '\r\n\r\n'

            payload = f'POST /{full_url} HTTP/1.1\r\nHost: {host}\r\nContent-type: {content_type}\r\nContent-length: {content_len}\r\n\r\n{params}'
            print(payload)
            self.sendall(payload)

            response = self.recvall(self.socket)

            code = self.get_code(response)
            body = self.get_body(response)

        except Exception as e:
            print(e)

        finally:
            #always close at the end!
            self.close()

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            result = self.POST(url, args)
            return result
        else:
            result = self.GET(url, args)
            return result
    
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
