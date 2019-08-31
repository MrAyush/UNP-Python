import threading
import socket

host = ''
port = 54321

class ClientFileTransfer(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        print('[+] Connection established to client', addr)
        self.conn = conn
        self.addr = addr
    def run(self):
        while True:
            msg = self.conn.recv(1024)
            if not msg:
                break
            print('[M]', self.addr, 'Message from the client:', msg.decode())
            with open('Text.csv', 'rb') as f:
                r = f.read(1024)
                while r:
                    self.conn.send(r)
                    r = f.read(1024)
                if not r:
                    self.conn.close()
                    print('[S] Sent-> Text.txt to client', self.addr)
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