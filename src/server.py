import socket

port = 1234
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
  s.bind((socket.gethostname(),port))
  s.listen()
  print(f'Listening on port {port}')

  try:
    clientSocket, address = s.accept()

    with clientSocket:
      print(f"{address} connected")

      while True:
        data = clientSocket.recv(1024)
        if not data:
          break
        print(f'client: {data.decode()}')
        resp = input('server: ')
        clientSocket.sendall(resp.encode())
  except:
    print("Server shuted down")


