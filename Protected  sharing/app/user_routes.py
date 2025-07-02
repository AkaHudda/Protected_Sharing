from fastapi import APIRouter, HTTPException, Depends
from app.models import UserLogin, UserSignup
from app.auth import create_token, get_current_user, decode_token
from app.database import USERS

router = APIRouter()

@router.post("/signup")
def signup(user: UserSignup):
    if user.email in USERS:
        raise HTTPException(status_code=400, detail="Email exists")
    USERS[user.email] = {"password": user.password, "role": "client", "verified": False}
    token = create_token({"email": user.email})
    verify_url = f"http://localhost:8000/client/verify-email/{token}"
    return {"verify_link": verify_url}

@router.get("/verify-email/{token}")
def verify_email(token: str):
    data = decode_token(token)
    if not data or data['email'] not in USERS:
        raise HTTPException(status_code=400, detail="Invalid token")
    USERS[data['email']]['verified'] = True
    return {"message": "Email verified successfully"}

@router.post("/login")
def client_login(user: UserLogin):
    data = USERS.get(user.email)
    if not data or data['password'] != user.password or data['role'] != 'client':
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": create_token({"email": user.email, "role": "client"})}

@router.get("/files")
def list_files(user=Depends(get_current_user)):
    from app.database import FILES
    if user['role'] != 'client':
        raise HTTPException(status_code=403, detail="Access denied")
    return [{"file_id": fid, "filename": meta['filename']} for fid, meta in FILES.items()]

@router.get("/download-file/{file_id}")
def generate_download_link(file_id: str, user=Depends(get_current_user)):
    from app.database import FILES
    if user['role'] != 'client':
        raise HTTPException(status_code=403, detail="Only clients can download")
    if file_id not in FILES:
        raise HTTPException(status_code=404, detail="File not found")
    secure_token = create_token({"file_id": file_id, "email": user['email']})
    return {"download-link": f"/secure-download/{secure_token}", "message": "success"}
