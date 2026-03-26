import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.logger import get_logger

logger = get_logger("mailer")

def send_verification_email(to_email: str, token: str):
    """
    發送 Email 驗證連結給使用者。
    需要環境變數: GMAIL_USER, GMAIL_APP_PASSWORD, BASE_URL
    """
    gmail_user = os.getenv("GMAIL_USER")
    gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")
    base_url = os.getenv("BASE_URL") or "http://localhost:5173"

    if not gmail_user or not gmail_app_password:
        logger.warning("GMAIL_USER 或 GMAIL_APP_PASSWORD 未設定，跳過郵件發送。")
        return False

    verify_url = f"{base_url}/api/auth/verify?token={token}"

    msg = MIMEMultipart()
    msg['From'] = f"AI Tarot System <{gmail_user}>"
    msg['To'] = to_email
    msg['Subject'] = "【AI-Tarot】請驗證您的註冊帳號"

    body = f"""
    您好，感謝您註冊 AI-Tarot 導師系統。
    
    請點擊下方連結以驗證您的電子郵件並提交審核：
    {verify_url}
    
    驗證通過後，管理員將進行手動審核。核准後您即可使用 Google 帳號登入系統。
    系統將為您產生一個隨機初始密碼（登入後可修改）。
    
    祝您 占卜愉快！
    AI-Tarot Team
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_app_password)
            server.send_message(msg)
        logger.info(f"驗證信已發送至 {to_email}")
        return True
    except Exception as e:
        logger.error(f"發送郵件失敗: {e}")
        return False

def log_signup_to_json(email: str, mentor_id: str):
    """
    將註冊紀錄寫入 data/signups.json
    """
    import json
    from datetime import datetime
    
    log_dir = "data"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_file = os.path.join(log_dir, "signups.json")
    record = {
        "email": email,
        "mentor_id": mentor_id,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        data = []
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        data.append(record)
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"註冊紀錄已寫入 {log_file}")
    except Exception as e:
        logger.error(f"寫入 signups.json 失敗: {e}")
