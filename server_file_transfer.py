import threading
import socket
import os

host = ''
port = 54321
file_path = 'xyz.txt'

class ClientFileTransfer(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        print('[+] Connection established to client', addr)
        self.conn = conn
        self.addr = addr
    def run(self):
        while True:
            size = str.encode(str(os.path.getsize(file_path)))
            self.conn.send(size)
            msg = self.conn.recv(1024)
            if not msg:
                break
            print('[M]', self.addr, 'Message from the client:', msg.decode())
            with open(file_path, 'rb') as f:
                r = f.read(10)
                while r:
                    self.conn.send(r)
                    r = f.read(512)
                if not r:
                    self.conn.close()
                    print(f'[S] Sent-> {file_path} to client', self.addr)
                    print('[-]', self.addr, 'Connection closed')
                    break


s = socket.socket()
s.bind((host, port))
print('|+| Server Initiated')
s.listen()
threads = []
while True:
    conn, addr = s.accept()
    thread = ClientFileTransfer(conn, addr)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()