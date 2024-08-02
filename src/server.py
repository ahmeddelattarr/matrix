import socket
import ssl
import os
import subprocess

current_dir = os.path.dirname(os.path.abspath(__file__))
cert_path = os.path.join(current_dir, 'ssl/cert.pem')
key_path = os.path.join(current_dir, 'ssl/key.pem')
config_path = os.path.join(current_dir, 'openssl.cnf')

def generate_ssl_cert(cert_path, key_path, config_path):
    if not os.path.exists(cert_path) or not os.path.exists(key_path):
        print("Generating SSL certificate and key...")
        subprocess.run(['openssl', 'genrsa', '-out', key_path, '2048'])
        subprocess.run(['openssl', 'req', '-new', '-key', key_path, '-out', 'csr.pem', '-config', config_path])
        subprocess.run(['openssl', 'x509', '-req', '-days', '365', '-in', 'csr.pem', '-signkey', key_path, '-out', cert_path, '-extensions', 'req_ext', '-extfile', config_path])
        os.remove('csr.pem')
        print("SSL certificate and key generated.")
    else:
        print("SSL certificate and key already exist.")

os.makedirs(os.path.join(current_dir, 'ssl'), exist_ok=True)

generate_ssl_cert(cert_path, key_path, config_path)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=cert_path, keyfile=key_path)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('localhost', 1234))
    s.listen(5)
    print("Server is listening on port 1234...")
    
    with context.wrap_socket(s, server_side=True) as ssock:
        conn, addr = ssock.accept()
        print(f"Connection from {addr} has been established!")
        with conn:
            try:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        print("Connection closed by client")
                        break
                    print(f'client: {data.decode()}')
                    resp = input('server: ')
                    conn.sendall(resp.encode())

            except ConnectionError as e:
                print(f"Connection error occurred: {e}")

            print("Server is shut down")
