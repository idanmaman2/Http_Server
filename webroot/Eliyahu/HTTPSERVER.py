"""
    Ex 4.4 - HTTP Server
    Author: Eliyahu Gamliel 325884054
    Date: 12.11.2021
"""

import socket
import os

IP = "0.0.0.0"
PORT = 80
SOCKET_TIMEOUT = 1000
DEFAULT_BUFLEN = 1024
DEFAULT_URL = '/index.html'
root_path = './webroot'
REDIRECTION_DICTIONARY = {'/page1.html': '/page2.html'}
FORBIDDEN = ["/secret1.html", "/secret2.html"]
error403 = '/error403.html'
error404 = '/error404.html'
error500 = '/error500.html'


def get_file_data(path):
    print(path)
    """ get: path
            return: the data from the file
        Read file and return the data
    """
    # if the file is exist
    if os.path.isfile(path):
        file = open(path, 'rb')
        size = os.path.getsize(path)
        data = file.read(size)
        return data
    # if the file isn't exist
    else:
        print("ERROR, the file doesn't exist")
        return ""


def handle_client_request(resource, client_socket):
    # Check the required resource, generate proper HTTP response and send to client
    if resource == '' or resource == '/':
        url = DEFAULT_URL
    else:
        url = resource
    path = root_path + url
    # Type Content default
    TContent = "text/html"
    # check if URL had been redirected, not available or other error code. For example:
    # Error 302
    if url in REDIRECTION_DICTIONARY:
        status = '302 Temporarily Moved'
        data = b''
        RESPONSE = 'HTTP/1.1 {}\r\nLocation:{}\r\n\r\n'.format(status, REDIRECTION_DICTIONARY[url])
    # Error 404
    elif not os.path.isfile(path):
        status = '404 Not Found'
        path = root_path + error404
        # To show the page "Error 404"
        data = get_file_data(path)
        RESPONSE = "HTTP/1.1 {}\r\nContent-Length: {}\r\nContent-Type: {}\r\n\r\n".format(status, len(data), TContent)
    # Error 403
    elif url in FORBIDDEN:
        status = '403 Forbidden'
        path = root_path + error403
        # To show the page "Error 403"
        data = get_file_data(path)
        RESPONSE = "HTTP/1.1 {}\r\nContent-Length: {}\r\nContent-Type: {}\r\n\r\n".format(status, len(data), TContent)
    # Valid
    else:
        status = "200 OK"
        filetype = url.split('.')[-1]
        if filetype == 'html' or filetype == 'text':
            TContent = "text/html; charset=utf-8"
        elif filetype == 'jpg':
            TContent = "image/jpeg"
        elif filetype == 'js':
            TContent = "text/javascript; charset=UTF-8"
        elif filetype == 'css':
            TContent = "text/css"
        elif filetype == 'ico':
            TContent = "image/x-icon"
        data = get_file_data(path)
        RESPONSE = "HTTP/1.1 {}\r\nContent-Length: {}\r\nContent-Type: {}\r\n\r\n".format(status, len(data), TContent)
    client_socket.send(RESPONSE.encode())
    if type(data) != bytes:
        data = data.encode()
    client_socket.send(data)


def validate_http_request(request):
    # Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    request = request.split('\r\n')
    arr_request = request[0].split()
    if len(arr_request) == 3 and arr_request[0] == "GET" and arr_request[2] == "HTTP/1.1":
        return True, arr_request[1]
    else:
        return False, "Error"


def handle_client(client_socket):
    """ get: the socket
            return: (send in the socket)
        Read file and return the data
    """
    print('Client connected')
    # Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests
    client_request = client_socket.recv(DEFAULT_BUFLEN).decode()
    valid_http, resource = validate_http_request(client_request)
    if valid_http:
        print('Got a valid HTTP request')
        handle_client_request(resource, client_socket)
    # Error 500
    else:
        print('Error: Not a valid HTTP request')
        status = '500 Internal Server Error'
        path = root_path + error500
        data = get_file_data(path)
        TContent = "text/html"
        RESPONSE = "HTTP/1.1 {}\r\nContent-Length: {}\r\nContent-Type: {}\r\n\r\n".format(status, len(data), TContent)
        client_socket.send(RESPONSE.encode())
        client_socket.send(data)
    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
