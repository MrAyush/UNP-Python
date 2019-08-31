import threading
import socket
import sys

host = ''
port = 54321

class ClientThread(threading.Thread):
    def __init__(self, addr, sock):
        threading.Thread.__init__(self)
        self.addr = addr
        self.sock = sock
        print('[+] New Connection added', addr)
    def run(self):
        print('[C]', self.addr, 'Connection started')
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            msg = data.decode()
            print('[M] Reading message:', msg)
            self.sock.send(data)
        print('[-] Connection removed', self.addr)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
print('|+| Server started (Press ctrl + c to exit)')
threads = []

while True:
    s.listen(5)
    try:
        conn, addr = s.accept()
        thread = ClientThread(addr, conn)
        thread.start()
        threads.append(thread)
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print('|-| Server terminated')
        conn.close()
        break