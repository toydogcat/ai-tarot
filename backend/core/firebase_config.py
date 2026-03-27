import firebase_admin
from firebase_admin import credentials, auth
import os
from core.logger import get_logger
from pathlib import Path

logger = get_logger("firebase_auth")

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

def init_firebase():
    """Initializes the Firebase Admin SDK if not already initialized."""
    if not firebase_admin._apps:
        # Look for service account key in backend/
        # Check both root and current dir depending on how it's run
        cert_path = BASE_DIR / "serviceAccountKey.json"
        
        if cert_path.exists():
            try:
                cred = credentials.Certificate(str(cert_path))
                firebase_admin.initialize_app(cred)
                logger.info("[Firebase] Admin SDK initialized successfully.")
                return True
            except Exception as e:
                logger.error(f"[Firebase] Initialization failed: {e}")
                return False
        else:
            logger.warning(f"[Firebase] serviceAccountKey.json not found at {cert_path}. Admin features disabled.")
            return False
    return True

def verify_token(id_token: str):
    """Verifies a Firebase ID token and returns the decoded info."""
    try:
        if not firebase_admin._apps:
            if not init_firebase():
                raise Exception("Firebase Admin SDK not initialized.")
        
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        logger.error(f"[Firebase] Token verification failed: {e}")
        raise e
