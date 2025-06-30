# app/routes/auth_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.auth_service import *
from app.utils.email_utils import send_otp_email

router = APIRouter(prefix="/auth")

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class OTPRequest(BaseModel):
    email: str

class PasswordResetRequest(BaseModel):
    email: str
    otp: str
    new_password: str

@router.post("/register")
def register(req: RegisterRequest):
    success, msg = register_user(req.username, req.email, req.password)
    if success:
        return {"message": msg}
    raise HTTPException(status_code=400, detail=msg)

@router.post("/login")
def login(req: LoginRequest):
    if verify_login(req.username, req.password):
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/send-otp")
def send_otp(req: OTPRequest):
    otp = generate_otp(req.email)
    if send_otp_email(req.email, otp):
        return {"message": "OTP sent"}
    raise HTTPException(status_code=500, detail="Email send failed")

@router.post("/reset-password")
def reset_password_route(req: PasswordResetRequest):
    if not validate_otp(req.email, req.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    username = next((u for u, d in load_users().items() if d["email"] == req.email), None)
    if not username:
        raise HTTPException(status_code=404, detail="User not found")
    reset_password(username, req.new_password)
    return {"message": "Password reset successful"}
