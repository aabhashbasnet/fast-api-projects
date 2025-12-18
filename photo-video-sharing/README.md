# Photo/Video Sharing App (FastAPI Backend)

A simple backend for a photo/video sharing application built with FastAPI, PostgreSQL, and SQLAlchemy.
Supports user registration, login (JWT authentication), creating posts with captions, and retrieving a feed of posts.

## Features

User Registration & Login

Password hashing with bcrypt

JWT authentication for protected endpoints

Create posts with captions (dummy file path for now)

Retrieve feed of posts (anyone can view)

Auto table creation on app startup

Swagger UI for testing endpoints

## Project Structure

photo-video-sharing/
│
├── main.py # FastAPI app + router setup
├── db.py # Database connection & session
├── models.py # SQLAlchemy models (User, Post)
├── schemas.py # Pydantic schemas
├── auth.py # Authentication & JWT helpers
│
├── routers/
│ ├── users.py # Register & login
│ └── posts.py # Create & get posts
│
└── requirements.txt # Python dependencies

## Installation

### Clone the repo:

git clone <repo-url>
cd photo-video-sharing

### Create a virtual environment:

python -m venv venv
venv\Scripts\activate # Windows

# source venv/bin/activate # macOS/Linux

### Install dependencies:

pip install -r requirements.txt

### Set up PostgreSQL database:

CREATE DATABASE photo_app;

Update db.py with your database credentials:

DATABASE_URL = "postgresql://postgres:password@localhost:5432/photo_app"

### Running the App

uvicorn main:app --reload

Open in browser:

Swagger UI: http://127.0.0.1:8000/docs

OpenAPI JSON: http://127.0.0.1:8000/openapi.json

## Endpoints

Users
Method Path Description
POST /users/register Register a new user
POST /users/login Login user and get JWT token
Posts
Method Path Description Auth Required
POST /posts/ Create a new post ✅ Yes
GET /posts/ Get all posts feed ❌ No
Example Requests

1. Register
   POST /users/register
   {
   "username": "aabhashbasnet25",
   "email": "aabhashbasnet25@gmail.com",
   "password": "123"
   }

2. Login
   POST /users/login
   {
   "email": "aabhashbasnet25@gmail.com",
   "password": "123"
   }

Response:

{
"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
"token_type": "bearer"
}

3. Create Post

Headers:

Authorization: Bearer <access_token>
Content-Type: application/json

Body:

{
"caption": "Hello world!"
}

4. Get Posts
   GET /posts/

Response:

[
{
"id": 1,
"file_path": "uploads/dummy.jpg",
"caption": "Hello world!",
"created_at": "2025-12-18T12:00:00+00:00",
"owner_id": 1
}
]

### Notes

Currently file_path is dummy (uploads/dummy.jpg)

Future improvements:

File upload (photos/videos)

Pagination for feed

Likes & comments

### User profiles

JWT Auth

All protected endpoints require Bearer token in Authorization header

Token valid for 24 hours (configurable in auth.py)

### Dependencies

FastAPI

SQLAlchemy

PostgreSQL (psycopg2-binary)

python-jose

passlib (bcrypt)

pydantic

uvicorn
