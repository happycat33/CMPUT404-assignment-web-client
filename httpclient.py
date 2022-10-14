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
        # We initialize an empty list called "host_port" and then we parse the url to get the hostname and port number and 
        # store them in the list (host name first and then port number). We then return them both in the list 

        host_port = ['127.0.0.1', 80]
        url_host = urllib.parse.urlparse(url).hostname
        url_port = urllib.parse.urlparse(url).port

        if url_host != None:
            host_port[0] = url_host

        if url_port != None:
            host_port[1] = url_port

        return host_port

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        # To get the code, the function takes in a HTTP response and splits the data by a space. This gives a list of all 
        # the seperate items of the response. We then take the int of the second item in the list (which is the status code)

        response_list = data.split(" ")
        code = int(response_list[1])
        return code

    def get_headers(self,data):
        # To get the code, the function takes in a HTTP response and splits the data by \r\n\r\n. This seperates the header 
        # and the body, we then take the first item in the split list (which is the header) and return it. 

        response_list = data.split("\r\n\r\n")
        header = response_list[0]
        return header

    def get_body(self, data):
        # To get the code, the function takes in a HTTP response and splits the data by \r\n\r\n. This seperates the header
        # and the body, we then take the second item in the split list (which is the body) and return it.

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
        # When given the GET command, we first try and set a basic code and body, then we get the host and port number 
        # (using get_host_port function) and then connect to a socket. Once we are connect, we find the path given
        # in the url (by parsing) and if we are given any queries or parameters, we add those to the path. We then set 
        # up the GET payload and put in the request and the headers and send it to the socket. Once we send it, we receive 
        # the response and close the socket. If anything fails then the try catch will print an exception. If it succeeds, then
        # we then call the corresponding functions to get the code and body and return in the form of a HTTP response. 

        try: 
            code = 500
            body = ""

            host_port = self.get_host_port(url)
            host = host_port[0]
            port = host_port[1]
            self.connect(host, port) 

            parsed_url = urllib.parse.urlparse(url)
            path = parsed_url.path

            # suggested by landberg (rather than adding an extra /, just check if path is empty, is so then add it to empty path)
            if not path:
                path = '/'

            payload = f'GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n'
            self.sendall(payload)
            response = self.recvall(self.socket)
            
        except Exception as e:
            print(e)

        finally:
            #always close at the end!
            self.close()
            code = self.get_code(response)
            body = self.get_body(response)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        # When given the POST command, we first set a basic code and body, then we get the host and port number
        # (using get_host_port function) and then connect to a socket. Once we are connect, we set an empty params,
        # content_type and content_len header. Then we find the path given in the url (by parsing) and if we are given
        # any params we then encode them, set the content_type and the content length and add it to the body variable. 
        # We then set up the POST payload and put in the request, headers, body and send it to the socket. Once we send 
        # it, we receive the response and close the socket.If anything fails then the try catch will print an exception. 
        # If it succeeds, then we then call the corresponding functions to get the code and body and return in the form 
        # of a HTTP response. 

        code = 500
        body = ""

        try:
            host_port = self.get_host_port(url)
            host = host_port[0]
            port = host_port[1]
            self.connect(host, port)

            params = ''
            content_type = ""
            content_len = 0

            parsed_url = urllib.parse.urlparse(url)
            path = parsed_url.path

            if not path:
                path = '/'

            if args:
                params = urllib.parse.urlencode(args)
                content_type = "application/x-www-form-urlencoded"
                content_len = len(params)

            payload = f'POST {path} HTTP/1.1\r\nHost: {host}\r\nContent-type: {content_type}\r\nContent-length: {content_len}\r\n\r\n{params}'
            self.sendall(payload)

            response = self.recvall(self.socket)

        except Exception as e:
            print(e)

        finally:
            #always close at the end!
            self.close()
            code = self.get_code(response)
            body = self.get_body(response)

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
