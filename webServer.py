# Yusuf Nadir Cavus
# February 26, 2023

import socket
import threading

PORT = 8080 # assumed port number 
HOST = 'localhost' # assumed host
HTML_FILE = "index.html" # assumed http file/webpage
IMAGE_FILE = "image.jpg" # assumed image file
BUF_SIZE = 1024 # max size for the request

# func: requestHandler
# parameters: c_socket : Any. this is a socket object, more specificcally the client socket
# This function recieves the request from the passed socket
# Then splits the request message to get the request method and what is requested
# if the method is 'GET', composes a response depending on the requested file (http file or image or neither)

def requestHandler(c_socket):
    req_sentence = c_socket.recv(BUF_SIZE).decode() # receive therequest message
    print(req_sentence)
    req_method = req_sentence.split(' ')[0] # method
    req_file = req_sentence.split(' ')[1] # file
    
    if req_method == "GET":
        
        if req_file == "/" + HTML_FILE:   
            # if the client's request is GET /index.html(HTML_FILE) 
            with open(HTML_FILE, "r") as f: 
                data = f.read()
            # HTTP response header
            response =  "HTTP/1.0 200 OK\r\n" # status code 
            response += "Content-Type: text/html\r\n" # content type
            response += "Content-Length: " + str(len(data)) + "\r\n" # content length
            response += "\r\n" # indicating the end of the response header
            response += data # this is the html, added to response after the header
            c_socket.sendall(response.encode()) # send the response back
            
        elif req_file == "/" + IMAGE_FILE:
            # if the client's request is GET /image.jpg(IMAGE_FILE) 
            with open(IMAGE_FILE, "rb") as f: # the mode specifier is 'rb' instead of 'r', becasue the file should be treated as binary
                data = f.read()               # otherwise, we get the error "UnicodeDecodeError: 'utf-8' codec can't decode"
            # HTTP response header
            response =  "HTTP/1.0 200 OK\r\n" # status code 
            response += "Content-Type: image/jpeg\r\n" # content type
            response += "Content-Length: " + str(len(data)) + "\r\n" # content length
            response += "\r\n" # indicating the end of the response header
            c_socket.sendall(response.encode() + data) # send the response back
            
        elif req_file == "/page1.html":
            # if the client's request is GET /page1.jpg
            response =  "HTTP/1.0 301 Moved Permanently\r\n" # status code
            response += "Content-Type: text/plain\r\n" # content type
            response += "Location: /page2.html\r\n" # Location, speciifes where the site should be redirected to
            response += "\r\n" # indicating the end of the response header
            c_socket.sendall(response.encode() + data) # send the response back
            
        else:
            data = "404 Not Found" 
            response = "HTTP/1.0 404 Not Found\r\n" # status code
            response += "Content-Type: text/plain\r\n" # content type
            response += "Content-Length: {}\r\n".format(len(data)) # content length
            response += "\r\n" # indicating the end of the response header
            response += data 
            c_socket.sendall(response.encode()) # send the response back
    
    else: 
        c_socket.close()    

# main function
# creates a socket object and binds it to localhost:8080
# main thread listens to the port 1
# for each request, a new thread is created and started 

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket object
    soc.bind((HOST, PORT)) # bind it to localhost:8080
    soc.listen(1) 
    
    print('The server is ready to receive\n') 
    
    while True:
        connectionSocket = soc.accept()[0] # accept() returns a tuple[socket, address]. we only need the socket
        thread = threading.Thread(target = requestHandler, args = (connectionSocket,)) # the requestHandler function is called on a new thread
                                                                                       # "(connectionSocket,)" the reason there is a comma after connecctionSocket here is to make it
                                                                                       # interpreted as a tuple with a single element instead of a variable, which is what the args = acceepts
        thread.start()

if __name__ == '__main__':
    main()
