
# Ex 4.4 - HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules
import socket
import os
import sys
# TO DO: set constants
IP = '0.0.0.0'
PORT = 80
DEFAULT_BUFFERSIZE = 1024
SOCKET_TIMEOUT = 1000
root=os.getcwd()
DEFAULT_URL ="./index.html"
ROOTwebroot = "./webroot"
print(DEFAULT_URL)
REDIRECTION_DICTIONARY = {} 
HTTP_VERSION="HTTP/1.1"

def get_file_data(filename):
    """ Get data from file """
    data=None
    print(root)
    print(ROOTwebroot)
    print (filename)
    print(os.path.isfile(root+ROOTwebroot+filename))
    if (os.path.isfile(root+filename)):
        file=open(filename,'rb')
        data=file.read()
        file.close()
    else : 
        print(" the access is forbidden ")
    if data == None : 
        print(" the file didnt open " )  
    return data 







def handle_client_request(resource, client_socket):
    print("resource: ", resource)
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    #return


    if resource == '' or resource== '/':
        url = DEFAULT_URL
    else:
        url = resource
    print(filename)
    filename = ROOTwebroot+ url 
        

    # TO DO: check if URL had been redirected, not available or other error code. For example:
    if url in REDIRECTION_DICTIONARY:
        client_socket.send(HTTP_VERSION+" 302 Found\r\n")
        # TO DO: send 302 redirection response

    # TO DO: extract requested file tupe from URL (html, jpg etc)

    filetype =  resource[-resource[::-1].find('.'):]
    print("the file type is : " , filetype) 
    if filetype == 'html':
        http_header = HTTP_VERSION+" 200 OK\r\nContent-Length: %s\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"%(os.path.getsize(resource)) # TO DO: generate proper HTTP header
    elif filetype == 'jpg':
        http_header = HTTP_VERSION+" 200 OK\r\nContent-Length:%s\r\nContent-Type: image/jpeg \r\n\r\n "%(os.path.getsize(resource)) # TO DO: generate proper HTTP header
# TO DO: generate proper jpg header
    # TO DO: handle all other headers
    # TO DO: read the data from the file
    data = get_file_data(filename)
    if(data == None):
        print("file is not valid ")
    else:
        if (type(data) != bytes):
             data= data.encode()
             client_socket.send(http_header)
             client_socket.send(data)
    
    
   
   


    
def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    print("request: "+ request)
    arr =request.split("\r\n")
    print("arr: "+str(arr) )
    print("res: " ,  arr[0].split(" ")[1] )
    print("arr2: ", arr[0].split(" "))
    if len(arr[0].split(" ")) == 3 and chek_for_valid_get(request) : 
        return True , arr[0].split(" ")[1] 
    # TO DO: write function
    return False, "Error"






def chek_for_valid_get(msg:str): 
    print( "1 : ", msg.split(" ")[0] == "GET"  , " 2: " , "/" in msg.split(" ")[1] , " 3: " ,  "HTTP" in msg.split(" ")[2]  )
    return msg.split(" ")[0] == "GET"  and "/" in msg.split(" ")[1] and "HTTP" in msg.split(" ")[2]  






def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    http_req=client_socket.recv(DEFAULT_BUFFERSIZE).decode()
    
    
    #client_socket.send(FIXED_RESPONSE.encode())
        # TO DO: insert code that receives client request
        # ...
    client_request  = http_req 
    print(client_request)
    valid_http, resource = validate_http_request(client_request)
    if valid_http:
        print("resource: " + resource)
        print('Got a valid HTTP request')
        handle_client_request(resource, client_socket ) 
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
