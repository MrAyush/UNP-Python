import socket
import selectors
import types

messages = [b'Message one', b'Message two']
host = '127.0.0.1'
port = 54321

sel = selectors.DefaultSelector()

def start_connection(host, port, num_conns):
    server_addr = (host, port)
    for i in range(1, num_conns + 1):
        print(f'Starting connection {i} to {server_addr}')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_WRITE | selectors.EVENT_READ
        data = types.SimpleNamespace(connid=i, msg_total = sum((len(m) for m in messages)), recv_total=0, messages=list(messages), outb=b'')
        sel.register(sock, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print('Received', repr(recv_data), 'from connection', data.connid)
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print('Closing connection', data.connid)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print('Sending', repr(data.outb), 'to connection', data.connid)
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]



start_connection(host, port, 2)

try:
    while True:
        event = sel.select(timeout=1)
        if event:
            for key, mask in event:
                service_connection(key, mask)
        if not sel.get_map():
            break    
except:
    pass