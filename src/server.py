import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #AF stands for address family so here we are dealing with ipv4
s.bind((socket.gethostname(),1234))
s.listen(5)

while True:
  clientSocket ,address =s.accept()
  print(f"All is good with{address}")
  clientSocket.send(bytes("Hey there!!!","utf-8"))
  clientSocket.close()
