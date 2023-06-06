import socket

HOST = 'localhost'
PORT = 9090
 
while True:
    sock = socket.socket()
    sock.connect((HOST, PORT))
    
    request = input('ilya@fa$ ')
    sock.send(request.encode())
    
    response = sock.recv(1024).decode()
    print(response)
    
    sock.close()