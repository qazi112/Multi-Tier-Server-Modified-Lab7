from sys import flags, setcheckinterval
from threading import Thread
import socket
import time
from typing import Tuple

ADDRESS = "127.0.0.1"
PORT = 5050

scheme = 'utf-8'
bufsize = 1024

# This socket is connected with main server
s = socket.socket()
s.connect((ADDRESS,PORT))

# ===========================================
def communicate(service_socket):
    serv_soc = socket.socket()
    serv_soc.connect(service_socket)
    message = input("Enter Your String ?> ")
    serv_soc.send(f"{message}".encode(scheme))
    print(serv_soc.recv(bufsize).decode(scheme))

# ======================================
# send username & password
username = input("Enter Username > ")
password = input("Enter Password > ")
s.send(f"{username},{password}".encode(scheme))
# -----------------

response = s.recv(bufsize).decode().split(",")
if response[0] == "0":
    print("USER DON'T exists")
else:
    print("USER EXISTS")
    print("1 -> service 1 Echo , 2 -> service 2 Palindrome, 3 -> Service 3 Length")

    # receive Token and it means user is valid user
    token = str(s.recv(bufsize).decode(scheme))

    option = int(input("Select Options 1 (Echo) , 2(palindrome) , 3(find length) ?> "))
    s.send(f"{username}  {token}  {int(option)}".encode(scheme))

    status = s.recv(bufsize).decode(scheme)
    if status == "1":
        print("Token Validated")
        addr , port = s.recv(bufsize).decode(scheme).split(",")
        port = int(port)

        # now we can talk with relevant server
        communicate(tuple((addr,int(port))))


    else:
        print("In Valid Token")
    


s.close()

