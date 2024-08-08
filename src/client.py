import asyncio
import ssl
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
cert_path = os.path.join(current_dir, 'ssl/cert.pem')

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations(cert_path)

async def client():
    reader, writer = await asyncio.open_connection('localhost', 1234, ssl=context)
    try:
        while True:
            msg = input('send: ')
            writer.write(msg.encode())
            await writer.drain()
            data = await reader.read(1024)
            if not data:
                print('Connection closed by server')
                break
            print(f'server recieved : {data.decode()}')
    except ConnectionError as e:
        print(f"Connection error occurred: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        print("Client is shut down")

if __name__ == "__main__":
    asyncio.run(client())
