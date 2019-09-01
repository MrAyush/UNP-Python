import socket
import threading
import time
import os

host = '127.0.0.1'
port = 54321
receivefile = 'Receive' + str(int(time.time())) + '.csv'

class ServerFileReceive(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        print('[+] Connected to host')
        self.conn = conn
    def run(self):
        size = self.conn.recv(1024)
        print('[M] Message from the server:', size.decode())
        msgx = 'Message from ' + threading.current_thread().name
        self.conn.send(msgx.encode())
        f = open(receivefile, 'wb')
        while True:
            msg = self.conn.recv(512)
            stat_down = f'[M] Message from the server: {repr(msg[:20])}... Downloading...{os.path.getsize(receivefile)*100//int(size)}%\r'
            print(stat_down, end='')
            backspace = '\b' * len(stat_down)
            if not msg:
                self.conn.close()
                f.close()
                print('  '*len(stat_down), end='')
                backspace = '\b\b' * len(stat_down)
                print(backspace, end='')
                print(f'[M] Downloaded, saved -> {receivefile}\r')
                print('[-] Connection to host teminated')
                break
            print(backspace, end='')
            f.write(msg)

s = socket.socket()
s.connect((host, port))
thread = ServerFileReceive(s)
thread.start()
thread.join()
