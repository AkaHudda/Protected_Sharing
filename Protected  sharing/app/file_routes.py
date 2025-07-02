from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from uuid import uuid4
import os
import shutil

from app.auth import get_current_user, decode_token
from app.database import FILES, USERS, UPLOAD_DIR
from app.models import UserLogin
from app.auth import create_token

router = APIRouter()

@router.post("/ops/login")
def ops_login(user: UserLogin):
    data = USERS.get(user.email)
    if not data or data['password'] != user.password or data['role'] != 'ops':
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": create_token({"email": user.email, "role": "ops"})}

@router.post("/ops/upload")
def upload_file(file: UploadFile = File(...), user=Depends(get_current_user)):
    if user['role'] != 'ops':
        raise HTTPException(status_code=403, detail="Only Ops can upload")
    if not file.filename.endswith((".pptx", ".docx", ".xlsx")):
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, file_id + "_" + file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    FILES[file_id] = {"filename": file.filename, "path": file_path, "uploaded_by": user['email']}
    return {"file_id": file_id, "filename": file.filename}

@router.get("/secure-download/{token}")
def secure_download(token: str, user=Depends(get_current_user)):
    data = decode_token(token)
    if not data or data['email'] != user['email']:
        raise HTTPException(status_code=403, detail="Invalid download token")
    file_meta = FILES.get(data['file_id'])
    if not file_meta:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_meta['path'], filename=file_meta['filename'])
