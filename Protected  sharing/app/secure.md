How to secure your file sharing file api ?
ech stack

Python FastAPI
In-memory DB (Replace with PostgreSQL in prod)
Uvicorn ASGI Server
Gunicorn for production (optional)
Nginx Reverse Proxy (recommended)
Gmail SMTP for email verification
hosting options

Render
Railway
DigitalOcean
AWS EC2
security measures

Use .env to store secrets (Fernet key, DB creds, Gmail app password)
HTTPS (SSL) via Nginx or automatic via Render
CORS enabled only for known domains
File type and size validation
Auth tokens (optional enhancement)
deployment

Push code to GitHub
Go to https://github.com/AkaHudda/Protected_Sharing
Create a new Web Service from GitHub repo
Set environment variables:
FERNET_KEY
GMAIL_USER, GMAIL_PASS
Start command:python -m uvicorn app.main:app --reload
