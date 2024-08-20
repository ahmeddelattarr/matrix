
# Matrix: Secure Asyncio Server/Client

<picture>
  <source media="(prefers-color-scheme: light)" srcset="src/logo.png">
  <img alt="tiny corp logo" src="src/logo.png" width="50%" height="50%">
</picture>

A simple, SSL-enabled server/client application written in Python using `asyncio` and `ssl`.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Key Components](#key-components)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

## Features
- Asynchronous server and client communication
- SSL encryption for secure data transfer
- JWT-based authentication
- PostgreSQL database integration
- Automatic SSL certificate generation

## Project Structure
```plaintext
src/
│
├── ssl/
│   ├── cert.pem
│   ├── key.pem
├── client.py
├── openssl.cnf
├── requirements.txt
├── dbConnection.py
└── server.py
```

- `ssl/`: Contains SSL certificate (`cert.pem`) and key (`key.pem`)
- `client.py`: Asyncio-based client implementation
- `openssl.cnf`: OpenSSL configuration for certificate generation
- `requirements.txt`: Project dependencies
- `dbConnection.py`: Database connection and table initialization
- `server.py`: Main server code handling connections, JWT, and verification

## Requirements
- Python 3.8+
- Dependencies (installed via `requirements.txt`):
  - asyncio
  - ssl
  - os
  - subprocess
  - pyjwt
  - python-dotenv
  - asyncpg

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/matrix.git
   cd matrix
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the project root and add:
   ```
   DATABASE_URL=<your-postgresql-connection-string>
   ```

## Usage
### Starting the Server
```bash
python server.py
```

### Running the Client
```bash
python client.py
```

The client will establish an SSL connection with the server, receive a JWT token, and can then send authenticated messages.

## Key Components
### SSL Certificate
The server automatically generates SSL certificates if not present in the `ssl/` directory, using the `openssl.cnf` configuration.

### JWT Authentication
- Clients receive a JWT token upon connection, valid for 1 hour
- The server verifies the JWT token with each communication
- Clients are notified upon token expiration

### Database Integration
- Utilizes Neon DB (PostgreSQL)
- Initializes connection and creates `Users` and `Messages` tables on server start

## Security
- SSL encryption ensures secure data transfer
- JWT tokens provide stateless authentication
- Automatic certificate generation enhances ease of deployment

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the [MIT License](LICENSE).
