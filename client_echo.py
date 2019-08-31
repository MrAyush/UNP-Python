import socket

host = ''
port = 54321

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(b'Hello, world!!')
    data = s.recv(1024)

print('Received', str(repr(data)))