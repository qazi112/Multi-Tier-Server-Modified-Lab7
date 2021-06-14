from threading import Thread
import socket
import time
from SERVER_DETAIL.servers_detail import servers

from multiThreadedClient import MultiThreadClient

# Main server runnning on 
# {"127.0.0.1" : 5050 }

ADDRESS = "127.0.0.1"
PORT = 5050
bufsize = 1024
scheme = "utf-8"

print("Available servers : ")
print(servers)
# client_server = { client : server_Number,...}

print(f"Server =>  {ADDRESS} : {PORT}")


with socket.socket() as s:
    s.bind((ADDRESS,PORT))
    s.listen(5)
    while True:
        conn,addr = s.accept()
        print(f"Client : {addr}, connected! ")
        client = MultiThreadClient(conn)

        client.start()

     
     
        
        