import socket
import ssl

# Create an SSL context for a TLS client
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('ssl\cert.pem')

# Create a socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connect to the server before wrapping with SSL
    s.connect(('localhost', 1234))

    
    with context.wrap_socket(s, server_hostname='localhost') as sock:

        try:
            while True:
                msg = input('client: ')
                sock.sendall(msg.encode())
                data = sock.recv(1024)
                if not data:
                    print('Connection closed by server')
                    break
                print(f'server: {data.decode()}')

        except ConnectionError as e:
            print(f"Connection error occurred: {e}")

        # No need for explicit sock.close() as 'with' handles it
        print("Client is shut down")
