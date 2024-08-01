import socket
import ssl

port = 1234

# Create an SSL context for the server
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='ssl/cert.pem', keyfile='ssl/key.pem')

# Create a socket and bind it to localhost and port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('localhost', port))
    s.listen()
    print(f'Listening on port {port}')

    # Wrap the socket with SSL/TLS
    with context.wrap_socket(s, server_side=True) as sock:
        try:
            client_socket, address = sock.accept()
            print(f"{address} connected")

            with client_socket:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    print(f'client: {data.decode()}')
                    resp = input('server: ')
                    client_socket.sendall(resp.encode())

        except ConnectionError as e:
            print(f"Connection error occurred: {e}")

print("Server is shut down")
