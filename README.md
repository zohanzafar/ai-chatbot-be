# Chatbot Backend API

This is a Django REST API backend for a user-authenticated chatbot. Users can register, log in, send messages, and retrieve chat histories.

## Table of Contents

- [How It Works](#how-it-works)
- [Features](#features)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [API Structure](#api-structure)
  - [Authentication (Accounts)](#authentication-accounts)
  - [Chat API](#chat-api)
- [URL Reference](#url-reference)
- [Notes](#notes)

## How It Works

1. **User Registration and Login:** Users register and log in using secure endpoints. A token is provided on successful login.
2. **Chat Sessions:** Each conversation is saved in a unique chat session (`session_id`).
3. **Message Flow:**
   - When a user sends a message:
     - If `session_id` is provided, the message is added to that session.
     - If `session_id` is omitted or `null`, a new session is automatically created.
4. **Session History:** Users can retrieve all session IDs and full chat logs by session.

## Features

- User authentication using token-based system.
- Chat sessions with full memory preservation.
- Full history retrieval per session.
- Session listing with timestamps.
- Secure handling of passwords and user data.
- Clean error handling with meaningful messages.
- Environment-ready for deployment with PostgreSQL, CORS, and OpenAI integration.

## Requirements

- Python 3.8+
- Django 5.x
- Django REST Framework
- PostgreSQL 
- OpenAI Python SDK

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/zohanzafar/ai-chatbot-be.git
cd ai-chatbot-be
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory with the following:

```dotenv
# Keys
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_secure_django_secret_key

# DEBUG
DEBUG=False

# Allowed Hosts
ALLOWED_HOSTS=yourdomain.com,localhost

# CORS Config
CORS_ALLOWED_ORIGINS=https://yourfrontend.com
CORS_ALLOW_CREDENTIALS=True

# PostgreSQL Database
POSTGRES_DB=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

## API Structure

All API endpoints are prefixed with `/api/v1/`.

### Authentication (Accounts)

| Method | Endpoint                     | Description                  |
|--------|------------------------------|------------------------------|
| POST   | `/api/v1/accounts/register/` | Register a new user          |
| POST   | `/api/v1/accounts/login/`    | Log in and receive auth token |
| POST   | `/api/v1/accounts/logout/`   | Log out and revoke token     |

**Register Request:**
```json
{
  "username": "zohanzafar",
  "email": "zohanzafar@example.com",
  "password1": "securepassword",
  "password2": "securepassword"
}
```

**Login Request:**
```json
{
  "username": "zohanzafar",
  "password": "securepassword"
}
```

> All protected routes require the `Authorization: Token <your_token>` header.

### Chat API

| Method | Endpoint                              | Description                          |
|--------|---------------------------------------|--------------------------------------|
| POST   | `/api/v1/chat/`                       | Send a message and get a response    |
| GET    | `/api/v1/chat/chats-history/`         | Get list of user's session IDs       |
| GET    | `/api/v1/chat/chats/<session_id>/`    | Get full chat messages for a session |

**POST `/api/v1/chat/` Example:**

```json
{
  "session_id": null,
  "message": "Hello, how are you?"
}
```

**Behavior:**
- `session_id` is **optional**.
- If omitted or `null`, a **new session** is created.
- Use the returned `session_id` to continue a session and maintain memory.

**Response Example:**

```json
{
  "session_id": "a1b2c3d4-e5f6-7890-1234-56789abcdef0",
  "message": "Hi there! How can I assist you today?"
}
```

## URL Reference

### Base Path

```
http://<your-domain>/api/v1/
```

### Full Endpoint List

#### Accounts

| Endpoint                      | Purpose                    |
|-------------------------------|----------------------------|
| `/accounts/register/`         | Register new users         |
| `/accounts/login/`            | Obtain auth token          |
| `/accounts/logout/`           | Revoke token and logout    |

#### Chat

| Endpoint                          | Purpose                            |
|-----------------------------------|------------------------------------|
| `/chat/`                          | Send a chat message                |
| `/chat/chats-history/`           | Get all chat session IDs           |
| `/chat/chats/<session_id>/`      | Get detailed messages for session  |

## Notes

- All authenticated routes require a token in the `Authorization` header:
  ```http
  Authorization: Token your_token_here
  ```
- Chat sessions automatically track message history per user.
- Clear error messages are returned for:
  - Missing fields
  - Incorrect login credentials
  - Unauthorized access
  - Invalid session IDs

