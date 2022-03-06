
import socket
import os
import sys

# TO DO: set constants
IP = '0.0.0.0'
PORT = 80
DEFAULT_BUFFER_SIZE = 2048  # default size of http packet
SOCKET_TIMEOUT = 1000
root = os.getcwd()
print(os.path.isfile("./webroot/index.html"))
DEFAULT_URL = "/index.html"
ROOT_w = "/webroot"
print(DEFAULT_URL)
# all the Moved Files and the path that they Moved to(To There)
REDIRECTION_DICTIONARY = {'/imgs/Moved1.jpg': '/jpg/ToThere1.jpg', '/imgs/Moved2.jpg': '/jpg/ToThere2.jpg'}
FORBIDDEN = ("/imgs/forbidden1.jpg", "/imgs/forbidden2.jpg")  # all the forbidden files
HTTP_VERSION = "HTTP/1.1"


def get_file_data(filename):
    """ Get data from file """
    data = None
    print(os.path.isfile(filename))
    if os.path.isfile(filename):
        file = open(filename, 'rb')
        data = file.read()
        file.close()
    else:
        print(" the access failed ")
    if data is None:
        print("the file didn't open ")
    return data


def handle_client_request(resource, client_socket):
    print("resource: ", resource)
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    # return
    filename = ""
    code = "200 OK"
    if resource == '' or resource == '/':
        url = DEFAULT_URL
    else:
        url = resource
    if resource in FORBIDDEN:
        code = "403 Forbidden"
        filename = root + ROOT_w + "/error403.html"
        print("FIle of 403 is :", os.path.isfile(filename), "\n", filename)
    if url in REDIRECTION_DICTIONARY:
        http_header = HTTP_VERSION + " 302 Temporarily Moved\r\nLocation:%s\r\n\r\n" % (REDIRECTION_DICTIONARY[url])
        client_socket.send(http_header.encode())
        return
    if code == "200 OK":
        filename = root + ROOT_w + url
        print(filename)
    data = get_file_data(filename)
    if data is None:
        print("file is not valid ")
        code = "404  Not Found"
        filename = root + ROOT_w + "/error404.html"
        data = get_file_data(filename)
    filetype = filename[-filename[::-1].find('.'):]
    print("the file type is : ", filetype)
    if filetype == "ico":
        http_header = HTTP_VERSION + " %s\r\nContent-Length: %s\r\nContent-Type:image/x-icon\r\n\r\n" % \
                      (code, os.path.getsize(filename))  # TO DO: generate proper HTTP header
    elif filetype == "css":
        http_header = HTTP_VERSION + " %s\r\nContent-Length: %s\r\nContent-Type: text/css; charset=utf-8\r\n\r\n" % \
                      (code, os.path.getsize(filename))  # TO DO: generate proper HTTP header
    elif filetype == "js":
        http_header = HTTP_VERSION + " %s\r\nContent-Length: %s\r\nContent-Type: text/js; charset=utf-8\r\n\r\n" % \
                      (code, os.path.getsize(filename))  # TO DO: generate proper HTTP header
    elif filetype == 'html':
        http_header = HTTP_VERSION + " %s\r\nContent-Length: %s\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" % \
                      (code, os.path.getsize(filename))  # TO DO: generate proper HTTP header
    elif filetype == 'jpg':
        http_header = HTTP_VERSION + " %s\r\nContent-Length: %s\r\nContent-Type: image/jpeg\r\n\r\n" % \
                      (code, os.path.getsize(filename))  # TO DO: generate proper HTTP header
    else:
        print("File Found Type is UnknownConverts as a text - text shower readonly")
        http_header = HTTP_VERSION + "500  Not Found\r\n\r\n"
        # read this file as text instead of send error page - i found this more useful
        print("BAD HTTP REQUEST")
    client_socket.send(http_header.encode())
    client_socket.send(data)


def validate_http_request(request):
    global HTTP_VERSION
    if request == "" or request == " ":
        return False, "Error"

    print("request: " + request)
    arr = request.split("\r\n")
    if len(arr[0].split(" ")) == 3 and chek_for_valid_get(request):
        HTTP_VERSION = arr[0].split(" ")[2]
        return True, arr[0].split(" ")[1]
        # TO DO: write function
    return False, "Error"


def chek_for_valid_get(msg: str):
    print("1 : ", msg.split(" ")[0] == "GET", " 2: ", "/" in msg.split(" ")[1], " 3: ", "HTTP" in msg.split(" ")[2])
    return msg.split(" ")[0] == "GET" and "/" in msg.split(" ")[1] and "HTTP" in msg.split(" ")[2]


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    http_req = client_socket.recv(DEFAULT_BUFFER_SIZE).decode()

    # client_socket.send(FIXED_RESPONSE.encode())
    # TO DO: insert code that receives client request
    # ...
    client_request = http_req
    print(client_request)
    valid_http, resource = validate_http_request(client_request)
    if valid_http:
        print("resource: " + resource)
        print('Got a valid HTTP request')
        handle_client_request(resource, client_socket)
    else:
        print('Error: Not a valid HTTP request')

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
