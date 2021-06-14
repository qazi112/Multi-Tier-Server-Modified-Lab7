from socket import socket
from threading import Thread
from users import user
from time import sleep
import string
import secrets
import random
scheme = "utf-8"
bufsize = 1024

class ClientHandler_Thread(Thread):
    def __init__(self,clientSoc):
        Thread.__init__(self)
        self.clientSoc = clientSoc

    def run(self):
        username , password = str(self.clientSoc.recv(bufsize).decode(scheme)).split(",")
        token = -1
        if username in user.keys():
            if password == user[username]:
                token = self.generateToken(username)
                print("User Exists")
            else:
                print("Wrong Password")
        else:
            print("No user Exists")
            token = -1
        self.clientSoc.send(f"{token}".encode(scheme))
        self.clientSoc.close()
        
    def generateToken(self,uname):

        alphabet = string.ascii_letters + string.digits
        while True:
            key_token = ''.join(secrets.choice(alphabet) for i in range(10))
            if (any(c.islower() for c in key_token)
                    and any(c.isupper() for c in key_token)
                    and sum(c.isdigit() for c in key_token) >= 3):
                        break
        hello = str(uname+key_token)
        return hello
