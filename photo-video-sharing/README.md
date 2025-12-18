pp Flow Overview

User Registration & Authentication

Users can register with email/username & password.

Passwords are hashed and stored in the database.

Users can log in and get a JWT token for protected routes.

Media Upload (Photo/Video)

Authenticated users can upload images or videos.

Files are stored locally (or on cloud later).

Each post stores: file path, user, timestamp, optional caption.

Feed / Display Posts

Fetch all posts sorted by timestamp (newest first).

Display user info, file (image/video), and posting date.

Database Models

User → stores user info and password.

Post → stores uploaded media info, user reference, timestamp.

API Endpoints

/register → Register new user.

/login → Authenticate and get JWT token.

/upload → Upload photo/video (authenticated).

/posts → Get all posts.

Security

Passwords hashed using passlib.

JWT tokens for authentication.
