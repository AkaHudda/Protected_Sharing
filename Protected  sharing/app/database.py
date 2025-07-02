import os

# In-memory simulated databases
USERS = {}  # email -> {"password": ..., "role": ..., "verified": ...}
FILES = {}  # file_id -> {"filename": ..., "path": ..., "uploaded_by": ...}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
