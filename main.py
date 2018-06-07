
import socket 
import signal 
import time 
import ssl   

class Server:
 """ Class describing a simple HTTP server objects."""

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
         print ("I will try a higher port")
        
         user_port = self.port
         self.port = 8080

         try:
             print("Launching HTTP server on ", self.host, ":",self.port)
             self.socket.bind((self.host, self.port))

         except Exception as e:
             print("ERROR: Failed to acquire sockets for ports ", user_port, " and 8080. ")
             print("Try running the Server in a privileged user mode.")
             self.shutdown()
             import sys
             sys.exit(1)

     print ("Server successfully acquired the socket with port:", self.port)
     print ("Press Ctrl+C to shut down the server and exit.")
     self._wait_for_connections()

 def shutdown(self):
     """ Shut down the server """
     try:
         print("Shutting down the server")
         s.socket.shutdown(socket.SHUT_RDWR)

     except Exception as e:
         print("Warning: could not shut down the socket. Maybe it was already closed?",e)

 def _gen_headers(self,  code):
     """ Generates HTTP response Headers. Ommits the first line! """

     h = ''
     if (code == 200):
        h = 'HTTP/1.1 200 OK\n'
     elif(code == 404):
        h = 'HTTP/1.1 404 Not Found\n'

     current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
     h += 'Date: ' + current_date +'\n'
     h += 'Server: Simple-Python-HTTP-Server\n'
     h += 'Connection: close\n\n' 

     return h

 def _wait_for_connections(self):
     """ Main loop awaiting connections """
     while True:
         print ("Awaiting New connection")
         self.socket.listen(3)

         conn, addr = self.socket.accept()

         print("Got connection from:", addr)

         data = conn.recv(1024)
         string = bytes.decode(data) 

         request_method = string.split(' ')[0]
         print ("Method: ", request_method)
         print ("Request body: ", string)

         if (request_method == 'GET') | (request_method == 'HEAD'):

             print (request_method)
             conn.send(b'server_response')
             print ("Closing connection with client")
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