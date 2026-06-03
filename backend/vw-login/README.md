# Valorant Wishlist - Auth API

A dedicated microservice for secure user authentication and identity management for the Valorant Wishlist platform.

## Security Features

- **JWT Authentication**: Industry-standard JSON Web Tokens for secure session handling.
- **HTTP-only Cookies**: Protection against XSS by storing tokens in secure, server-side cookies.
- **Argon2id Hashing**: Modern, side-channel resistant password encryption for user data protection.
- **Rate Limiting**: Integrated protection against brute-force attacks using Slowapi.
- **Security Headers**: Standardized XSS, Frame Options, and CSP headers.

## Setup & Installation

1.  Ensure PostgreSQL is running.
2.  Configure your .env file (see .env.example).
3.  Install dependencies: pip install -r requirements.txt.
4.  Run the server: uvicorn app.main:app --reload.

## API Endpoints

| Method | Route | Description |
| :--- | :--- | :--- |
| POST | /auth/register | Create a new agent account |
| POST | /auth/login | Authenticate and receive a secure session cookie |
| POST | /auth/logout | Clear the session cookie |
| GET | /health-check | Check service health |

## Authentication Mechanism

The service uses Secure Cookies:
- Upon successful login, the server sets an `access_token` cookie.
- The cookie is marked as `HttpOnly`, `Secure` (in production), and `SameSite=Strict`.
- The frontend does not need to manually handle the token for subsequent requests to this domain.

## Example Requests

### Register
```bash
curl -X 'POST' 'http://localhost:8001/auth/register' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "jett_main",
  "email": "jett@example.com",
  "password": "securepassword123",
  "display_name": "Jett",
  "bio": "I am the wind!"
}'
```

### Login
```bash
curl -X 'POST' 'http://localhost:8001/auth/login' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "jett_main",
  "password": "securepassword123"
}'
```

## License
Developed for academic purposes at the University of Fortaleza (UNIFOR).
