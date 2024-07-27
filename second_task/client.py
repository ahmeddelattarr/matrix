import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#AF stands for address family so here we are dealing with ipv4
#sock_stream stands for tcp

s.connect((socket.gethostname(),1234))

while True:
    msg = s.recv(8)
    print(msg.decode("utf-8"))
    