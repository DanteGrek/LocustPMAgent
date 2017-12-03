import socket
import pickle


sock = socket.socket()
sock.connect(('localhost', 9090))
sock.send('hello, world!')

while True:
    data = sock.recv(1024)
    if not data:
        break
    dict = pickle.loads(data)
    print dict

sock.close()

print dict