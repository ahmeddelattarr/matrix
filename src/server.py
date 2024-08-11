import asyncio
import ssl
import os
import subprocess
import jwt
import datetime

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

clients = []
client_counter = 1

SECRET_KEY = os.urandom(32)  # Generate once at startup

def generate_token(client_counter):
    token = jwt.encode(
        {
            "user_id": client_counter,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    return token

async def handle_client(reader, writer):
    global client_counter
    client_id = client_counter
    client_counter += 1
    clients.append((reader, writer))
    addr = writer.get_extra_info('peername')
    print(f"Connection from {addr} has been established as client{client_id}!")

    try:
        token = await generate_token(client_id)
        print(f"Generated JWT for client{client_id}: {token}")


        while True:
            data = await reader.read(1024)
            if data==b'':
                print(f"Connection closed by client{client_id}")
                break
            print(f'client{client_id}: {data.decode()}')

            writer.write(data)
            await writer.drain()
    except ConnectionError as e:
        print(f"Connection error occurred: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        clients.remove((reader, writer))
        print(f"Connection with client{client_id} closed")

async def main():
    server = await asyncio.start_server(handle_client, 'localhost', 1234, ssl=context)
    async with server:
        print("Server is listening on port 1234...")
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
