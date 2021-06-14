from os import stat
from threading import Thread
from SERVER_DETAIL.servers_detail import servers
# servers[4] -> ["127.0.0.1",5054] -> idendity server

import socket
import time
import sys
client_token = {}
# client_token[username] = [token,self.soc]
# ========================================

scheme = "utf-8"
bufsize = 1024
# ========================================

class MultiThreadClient(Thread):
    def __init__(self, clientSocket):
        Thread.__init__(self)
        self.clientSocket = clientSocket
        
    def run(self):
        # main server gets the username & password from client
        username, password = str(self.clientSocket.recv(bufsize).decode(scheme)).split(",")

        # contact with identity server
        client_to_identity = socket.socket()
        client_to_identity.connect((servers[4][0],servers[4][1]))

        print(client_to_identity.getpeername())
        client_to_identity.send(f"{username},{password}".encode(scheme))
        # it will rerturn token for that user
        token = str(client_to_identity.recv(bufsize).decode(scheme))
        # Protocol -> if token == -1 -> send to client (0,NOT)
        # if token != -1 -> send(1,OK)

        if token != "-1":
            client_token[username.lower()] = [token,self.clientSocket]

            self.clientSocket.send("1,OK".encode(scheme))
            print(client_token)
            # now main server sends the client token
            self.clientSocket.send(f"{token}".encode(scheme))

            # client can now request for new service
            # client will send username, token and serice 1,2 or 3
            username,token,service = self.clientSocket.recv(bufsize).decode(scheme).split("  ")
            service = int(service)

            if self.is_validToken(username,token):
                self.clientSocket.send("1".encode(scheme))
                # now send client the relevent server address
                addr = str(servers[int(service)][0])
                port = servers[int(service)][1]

                self.clientSocket.send(f"{addr},{port}".encode(scheme))
                # My Work is done
            else:
                self.clientSocket.send("0".encode(scheme))
                # end the connection

        else:
            print("User Don't Exits Database")
            self.clientSocket.send("0,NOT".encode(scheme))
            
       
        self.clientSocket.close()



    # Checks whether the token sent by client is valid or not
    def is_validToken(self,username,token):
        status = False
        if client_token.get(username.lower()) != None:
            print("Valid User")
            if client_token[username.lower()][0] == token:
                status = True
            else:
                status = False
        else:
            print("Invalid User")
        return status