import asyncio
import ssl


async def communicate_with_server(host, port, ssl_context):
    reader, writer = await asyncio.open_connection(host, port, ssl=ssl_context)

    try:
        token = await reader.readline()
        print(f"Received token from server: {token.decode().strip()}")

        username = input("Enter your username: ")
        writer.write(username.encode())
        await writer.drain()

        while True:
            message = input("Enter message to send to the server (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break


            # Send the message to the server
            writer.write(message.encode())
            await writer.drain()

            response = await reader.readline()
            print(f"Server: {response.decode().strip()}")

    except ConnectionError as e:
        print(f"Connection error: {e}")
    finally:
        print("Closing the connection...")
        writer.close()
        await writer.wait_closed()

def main():
    host = 'localhost'
    port = 1234

    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ssl_context.check_hostname = False  # Not checking hostname for local connection
    ssl_context.verify_mode = ssl.CERT_NONE  # Not verifying server certificate for local testing

    asyncio.run(communicate_with_server(host, port, ssl_context))

if __name__ == "__main__":
    main()
