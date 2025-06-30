# app/services/auth_service.py

import random
from app.models.user_model import load_users, save_users

otp_store = {}

def register_user(username, email, password):
    users = load_users()
    if username in users:
        return False, "Username already exists"
    users[username] = {"email": email, "password": password}
    save_users(users)
    return True, "User registered successfully"

def verify_login(username, password):
    users = load_users()
    if username in users and users[username]["password"] == password:
        return True
    return False

def get_email_by_username(username):
    users = load_users()
    return users.get(username, {}).get("email")

def generate_otp(email):
    otp = str(random.randint(100000, 999999))
    otp_store[email] = otp
    return otp

def validate_otp(email, otp):
    return otp_store.get(email) == otp

def reset_password(username, new_password):
    users = load_users()
    if username in users:
        users[username]["password"] = new_password
        save_users(users)
        return True
    return False
