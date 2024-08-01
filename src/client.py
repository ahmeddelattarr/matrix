import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

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

except ConnectionError as e :
  print(f"connection error occured :{e}")

finally:
  s.close()
  print("client is shuted down")



