from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import logging
import uuid
import secrets
import os
from typing import Any
from datetime import datetime
from sqlalchemy import select, update
from core.db import SessionLocal, mentors
from core.mailer import send_verification_email, log_signup_to_json
from core.firebase_config import verify_token, init_firebase

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["auth"])

# Initialize Firebase on router load
init_firebase()

class LoginRequest(BaseModel):
    mentor: str
    key: str

class RegisterRequest(BaseModel):
    email: str
    mentor_id: str

class LoginResponse(BaseModel):
    role: str
    mentor_id: str
    client_id: str | None = None
    room_level: str = "single"
    ai_enabled: bool = True
    max_clients: int = 1
    message: str

from core.db import FactorySessionLocal, mentors, PasswordHasher
from sqlalchemy import select, insert, update
from sqlalchemy.sql import func

@router.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest):
    mentor_id = req.mentor.lower().strip()
    provided_key = req.key.strip()
    
    if not mentor_id:
        raise HTTPException(status_code=400, detail="Mentor (Account) cannot be empty.")
        
    if not provided_key:
        raise HTTPException(status_code=400, detail="Key (Password) cannot be empty.")
        
    with FactorySessionLocal() as db:
        mentor = db.execute(select(mentors).where(mentors.c.mentor_id == mentor_id)).first()
        
        if mentor:
            if mentor.status != 'active' and mentor_id != 'toby':
                 raise HTTPException(status_code=403, detail=f"Account status: {mentor.status}. Please wait for admin approval.")

            if PasswordHasher.verify(provided_key, mentor.password):
                # Login as Mentor
                db.execute(update(mentors).where(mentors.c.mentor_id == mentor_id).values(last_active_at=func.now()))
                db.commit()
                logger.info(f"Mentor {mentor_id} logged in successfully.")
                return LoginResponse(
                    role="toby", 
                    mentor_id=mentor_id, 
                    room_level=mentor.room_level,
                    ai_enabled=mentor.ai_enabled,
                    max_clients=mentor.max_clients,
                    message="Welcome back, Mentor!"
                )
            else:
                # Login as Client
                logger.info(f"Client '{provided_key}' logging into mentor '{mentor_id}' room.")
                return LoginResponse(role="client", mentor_id=mentor_id, client_id=provided_key, message=f"Welcome, Client {provided_key}!")
        else:
            # Enforce security: No auto-registration via login
            logger.warning(f"Login attempt for non-existent mentor: {mentor_id}")
            raise HTTPException(status_code=404, detail="導師房間不存在，請檢查 ID 是否正確 (Mentor room not found).")

class GoogleLoginRequest(BaseModel):
    credential: str

@router.post("/google_login", response_model=LoginResponse)
async def google_login(req: GoogleLoginRequest):
    try:
        # Verify Firebase ID Token
        payload = verify_token(req.credential)
        email = payload.get("email")
        
        if not email:
            raise HTTPException(status_code=400, detail="Firebase account has no email.")
            
        with FactorySessionLocal() as db:
            mentor = db.execute(select(mentors).where(mentors.c.email == email)).first()
            
            if mentor:
                if mentor.status != 'active' and mentor.mentor_id != 'toby':
                     raise HTTPException(status_code=403, detail=f"Account status: {mentor.status}. Please wait for admin approval.")
                
                db.execute(update(mentors).where(mentors.c.mentor_id == mentor.mentor_id).values(last_active_at=func.now()))
                db.commit()
                logger.info(f"Mentor {mentor.mentor_id} logged in via Firebase Auth ({email}).")
                return LoginResponse(
                    role="toby", 
                    mentor_id=mentor.mentor_id, 
                    room_level=mentor.room_level,
                    ai_enabled=mentor.ai_enabled,
                    max_clients=mentor.max_clients,
                    message=f"Welcome back, {mentor.mentor_id}!"
                )
            else:
                # User doesn't exist, tell frontend to show signup
                logger.info(f"Firebase user {email} not found in mentors table.")
                raise HTTPException(status_code=404, detail="NOT_REGISTERED")
                
    except Exception as e:
        logger.error(f"Firebase Login Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/register")
async def register_mentor(req: RegisterRequest):
    mentor_id = req.mentor_id.lower().strip()
    email = req.email.strip()
    
    if not mentor_id or not email:
        raise HTTPException(status_code=400, detail="ID and Email required.")
        
    with FactorySessionLocal() as db:
        # Check if exists
        exists = db.execute(select(mentors).where((mentors.c.mentor_id == mentor_id) | (mentors.c.email == email))).first()
        if exists:
             raise HTTPException(status_code=400, detail="Mentor ID or Email already registered.")
        
        token = secrets.token_urlsafe(32)
        # Temporary random password
        temp_pw = secrets.token_hex(4)
        
        db.execute(insert(mentors).values(
            mentor_id=mentor_id,
            password=PasswordHasher.hash(temp_pw),
            email=email,
            status='pending',
            verification_token=token,
            enable_multiuser_login=False,
            usage_limit=5,
            bgm_id=1
        ))
        db.commit()
        
        # Log to JSON as requested
        log_signup_to_json(email, mentor_id)
        
        # Send Email
        sent = send_verification_email(email, token)
        
        return {
            "message": "Registration submitted. Please check your email for verification.",
            "email_sent": sent
        }

@router.get("/verify")
async def verify_email(token: str):
    if not token:
        raise HTTPException(status_code=400, detail="Token required.")
        
    with FactorySessionLocal() as db:
        user = db.execute(select(mentors).where(mentors.c.verification_token == token)).first()
        if not user:
            return {"error": "Invalid or expired token."}
            
        db.execute(update(mentors).where(mentors.c.verification_token == token).values(
            status='verifying_done',
            verification_token=None
        ))
        db.commit()
        
        return {
            "message": "Email verified! Your account is now pending admin approval.",
            "status": "verifying_done"
        }

class SettingsUpdate(BaseModel):
    mentor_id: str
    ai_enabled: bool | None = None
    max_clients: int | None = None
    announcement: str | None = None

@router.post("/settings")
async def update_settings(req: SettingsUpdate):
    with FactorySessionLocal() as db:
        mentor = db.execute(select(mentors).where(mentors.c.mentor_id == req.mentor_id)).first()
        if not mentor:
            raise HTTPException(status_code=404, detail="Mentor not found")
            
        update_vals: dict[str, any] = {}
        if req.ai_enabled is not None:
            # Restrictions: only double/multi can toggle AI
            if mentor.room_level == 'single':
                ai_val = True # Forced True for single? or whatever default.
            else:
                ai_val = req.ai_enabled
            update_vals["ai_enabled"] = ai_val
            
        if req.max_clients is not None:
            # Restrictions: only multi can change capacity
            if mentor.room_level == 'multi':
                update_vals["max_clients"] = max(1, min(20, req.max_clients))
            else:
                update_vals["max_clients"] = 1
                
        if req.announcement is not None:
            update_vals["announcement"] = req.announcement
                
        if update_vals:
            db.execute(update(mentors).where(mentors.c.mentor_id == req.mentor_id).values(**update_vals))
            db.commit()
            
            # Sync with in-memory room
            from api.websocket_manager import manager
            room = manager.get_room(req.mentor_id)
            if "ai_enabled" in update_vals:
                room.ai_enabled = update_vals["ai_enabled"]
            if "max_clients" in update_vals:
                room.max_clients_override = update_vals["max_clients"]
            if "announcement" in update_vals:
                await manager.broadcast_announcement(req.mentor_id, update_vals["announcement"])
                
        return {"status": "success", "updated": list(update_vals.keys())}

@router.get("/me")
def get_me(mentor_id: str):
    with FactorySessionLocal() as db:
        mentor = db.execute(select(mentors).where(mentors.c.mentor_id == mentor_id)).first()
        if not mentor:
            raise HTTPException(status_code=404, detail="Mentor not found")
        return {
            "mentor_id": mentor.mentor_id,
            "room_level": mentor.room_level,
            "ai_enabled": mentor.ai_enabled,
            "max_clients": mentor.max_clients,
            "usage_limit": mentor.usage_limit,
            "announcement": mentor.announcement or ""
        }
