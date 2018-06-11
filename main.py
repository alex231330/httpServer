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
         self.port = 2345

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


 def _gen_headers(self,  code, data):
     """ Generates HTTP response Headers. Ommits the first line! """
     h = ''
     if (code == 200):
        h = 'HTTP/1.1 200 OK\n'
     elif(code == 404):
        h = 'HTTP/1.1 404 Not Found\n'

     # write further headers
     current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
     h += 'Date: ' + current_date +'\n'
     h += 'Server: Simple-Python-HTTP-Server\n'
     h += 'Connection: close\n\n'  # signal that the conection wil be closed after complting the request
	 if not(data == None):
		h += data
     return h


 def _wait_for_connections(self):
     minerStats = None
     current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
     cReq = 'HTTP/1.1 303 OK\n Date: ' + current_date + '\n Server: Simple-Python-HTTP-Server\n Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT \n Content-Length: 10 \n Content-Type: text/html \n Connection: close \n\n'
     while True:
        print ("Awaiting New connection")
        self.socket.listen(3)

        conn, addr = self.socket.accept()

        print("Got connection from:", addr)

        data = conn.recv(1024)
        if data != None:
            string = bytes.decode(data) 
            request_method = string.split(' ')[0]
            print ("Method: ", request_method)
            print ("Request body: ", string)

            if (request_method == 'GET') | (request_method == 'HEAD'):
                req = None
                if minerStats != None:
                    req = 'HTTP/1.1 200 OK\n Date: ' + current_date + '\n Server: Simple-Python-HTTP-Server\n Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT\n Content-Length: 3454\n Content-Type: text/html \n Connection: close\n\n' + minerStats
                    print(minerStats)
                else:
                    req = 'HTTP/1.1 200 OK\n Date: ' + current_date + '\n Server: Simple-Python-HTTP-Server\n Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT\n Content-Length: 3454\n Content-Type: text/html \n Connection: close\n\n' 
                print (request_method)
                print(req + '\n')
                print(str(req.encode()))
                try:
                    conn.send(req.encode())
                except SocketError as e:
                        if e.errno != errno.ECONNRESET:
                            raise Exception('Error').with_traceback(e.__traceback__)
                print ("Closing connection with client")
                conn.close()
            elif request_method == 'POST':

                #print (request_method)
                #print(data)
                minerStats = string.split('\n')[8]
                print("Data", data)
                res = self._gen_headers( 200)
                conn.send(res.encode())
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
s = Server(2366)  
s.activate_server() 