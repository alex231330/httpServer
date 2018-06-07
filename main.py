from socket import error as SocketError
import errno
import socket 
import signal 
import time 
import ssl   

class Server:

 def __init__(self, port = 80):
     """ Constructor """
     self.host = ''  
     self.port = port
     self.www_dir = 'www'

 def activate_server(self):
     """ Attempts to aquire the socket and launch the server """
     
     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     #self.socket = ssl.wrap_socket (self.socket, keyfile="key.pem", certfile='cert.pem', server_side=True)
     try: 
         print("Launching HTTP server on ", self.host, ":",self.port)
         self.socket.bind((self.host, self.port))

     except Exception as e:
         print ("Warning: Could not aquite port:",self.port,"\n")
        
         user_port = self.port
         self.port = 8080

         try:
             print("Launching HTTP server on ", str(self.host), ":",self.port)
             self.socket.bind((self.host, self.port))

         except Exception as e:
             print("ERROR: Failed to acquire sockets for ports ", user_port, " and 8080. ")
             print("Try running the Server in a privileged user mode.")
             self.shutdown()
             import sys
             sys.exit(1)

     print ("Port acquired:", self.port)
     self._wait_for_connections()

 def shutdown(self):
     try:
         print("Shutting down the server")
         s.socket.shutdown(socket.SHUT_RDWR)

     except Exception as e:
         print("Warning: could not shut down the socket. Maybe it was already closed?",e)

 def _wait_for_connections(self):
     while True:
        print ("Awaiting New connection")
        self.socket.listen(3)

        conn, addr = self.socket.accept()

        print("Got connection from:", addr)

        data = conn.recv(1024)
        if data != None:
            string = bytes.decode(data) 

            request_method = string.split(' ')[0]
            data = string.split(' ')[2]
            print ("Method: ", request_method)
            print ("Request body: ", string)

            if (request_method == 'GET') | (request_method == 'HEAD'):

                print (request_method)
                current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
                req = 'HTTP/1.1 200 OK\n Date: ' + current_date + '\n Server: Simple-Python-HTTP-Server\n Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT\n Content-Length: 88\n Content-Type: text/html \n Connection: close\n\n <html><body><h1>Hello, World!</h1></body></html>'
                print(req + '\n')
                print(str(req.encode()))
                try:
                    conn.send(req.encode())
                except SocketError as e:
                        if e.errno != errno.ECONNRESET:
                            raise Exception('Error').with_traceback(e.__traceback__)
                print ("Closing connection with client")
                conn.close()
            if request_method == 'POST':

                print (request_method)
                print(data)
                req = 'HTTP/1.1 200 OK\n Date: ' + current_date + '\n Server: Simple-Python-HTTP-Server\n Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT\n Content-Length: 88\n Content-Type: text/html \n Connection: close\n\n <html><body><h1>Hello, World!</h1></body></html>'
                conn.close()
            else:
                 print("Unknown HTTP request method:", request_method)

def graceful_shutdown(sig, dummy):
    """ This function shuts down the server. It's triggered
    by SIGINT signal """
    s.shutdown() 
    import sys
    sys.exit(1)

signal.signal(signal.SIGINT, graceful_shutdown)

print ("Starting web server")
s = Server(80)  
s.activate_server() 