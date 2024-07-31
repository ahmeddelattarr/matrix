import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#AF stands for address family so here we are dealing with ipv4
#sock_stream stands for tcp
try:
  with s:
    s.connect((socket.gethostname(),1234))

    while True:
      msg = input('client: ')
      s.sendall(msg.encode())
      data = s.recv(1024)
      if not data:
        print('connection closed by server')
        break
      print(f'server: {data.decode()}')

except:
  print("Client is shuted down")

