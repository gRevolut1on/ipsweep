import socket

host= '127.0.0.1'
port= 8888

msg= input().encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host,port))
    s.sendall(msg)
    data= s.recv(1024)

print('Received:', data.decode())