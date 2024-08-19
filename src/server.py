import asyncio
import ssl
import os
import subprocess
import jwt
import datetime
from dbConnection import initialize_database, register_user,get_user ,save_message,get_the_last_id

connection_string = os.getenv('DATABASE_URL')
current_dir = os.path.dirname(os.path.abspath(__file__))
cert_path = os.path.join(current_dir, 'ssl/cert.pem')
key_path = os.path.join(current_dir, 'ssl/key.pem')
config_path = os.path.join(current_dir, 'openssl.cnf')

def generate_ssl_cert(cert_path, key_path, config_path):
    if not os.path.exists(cert_path) or not os.path.exists(key_path):
        print("Generating SSL certificate and key...")
        subprocess.run(['openssl', 'genrsa', '-out', key_path, '2048'], check=True)
        subprocess.run(['openssl', 'req', '-new', '-key', key_path, '-out', 'csr.pem', '-config', config_path], check=True)
        subprocess.run(['openssl', 'x509', '-req', '-days', '365', '-in', 'csr.pem', '-signkey', key_path, '-out', cert_path, '-extensions', 'req_ext', '-extfile', config_path], check=True)
        os.remove('csr.pem')
        print("SSL certificate and key generated.")
    else:
        print("SSL certificate and key already exist.")

os.makedirs(os.path.join(current_dir, 'ssl'), exist_ok=True)

generate_ssl_cert(cert_path, key_path, config_path)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=cert_path, keyfile=key_path)



SECRET_KEY = os.urandom(32)  # Generate once at startup

async def generate_token(user_id):
    token = jwt.encode(
        {
            "user_id": user_id,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"require": ["exp"]})
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return "Token expired"
    except jwt.InvalidTokenError:
        return "Invalid token"
    except Exception as e:
        print(f"Unexpected error during token verification: {e}")
        return None  # Handle any other unexpected errors


async def handle_client(reader, writer):


    client_id =await get_the_last_id()+1



    addr = writer.get_extra_info('peername')
    print(f"Connection from {addr} has been established as client{client_id}!")

    try:
        token = await generate_token(client_id)
        print(f"Generated JWT for client{client_id}: {token}")
        writer.write(f"Your token: {token}\n".encode())
        await writer.drain()

        auth_data = await reader.read(1024)
        username, password = auth_data.decode().strip().split(':')
        user_id = await register_user(username, password)
        user = await get_user(username)
        writer.write(f"{username} has been registered!\n".encode())
        await writer.drain()

        while True:
            data = await reader.read(1024)
            if data == b'':
                print(f"Connection closed by client{client_id} ({username})")
                break

            received_data = data.decode().strip()
            print(f'{username}: {received_data}')
           

            # Verify the token
            verified_user_id = verify_token(token)
            print(f"Token verification result for {username}: {verified_user_id}")

            if isinstance(verified_user_id, int):
                response = f"Token is valid for user_id: {verified_user_id}\n"

                await save_message(verified_user_id,received_data)



            else:
                response = f"{verified_user_id}\n"  # This will be either "Token expired" or "Invalid token"

            print(f"Sending response to {username}: {response.strip()}")
            writer.write(response.encode())
            await writer.drain()

    except ConnectionError as e:
        print(f"Connection error occurred for client{client_id} : {e}")
    finally:
        writer.close()
        await writer.wait_closed()

        print(f"Connection with client{client_id} ({username}) closed")

async def main():
    await initialize_database()
    server = await asyncio.start_server(handle_client, 'localhost', 1234, ssl=context)
    async with server:
        print("Server is listening on port 1234...")
        await server.serve_forever()



if __name__ == "__main__":
    asyncio.run(main())