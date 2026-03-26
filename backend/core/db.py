import os
import json
from sqlalchemy import create_engine, MetaData, Table, Column, String, Text, DateTime, JSON, Boolean, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy import select, insert, update, text
from dotenv import load_dotenv
from core.logger import get_logger
from fastapi import HTTPException
import bcrypt

load_dotenv()
logger = get_logger("db")

class PasswordHasher:
    @classmethod
    def hash(cls, password: str) -> str:
        if not password:
            return ""
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

    @classmethod
    def verify(cls, plain_password: str, hashed_password: str) -> bool:
        if not plain_password or not hashed_password:
            return False
        try:
            if not (hashed_password.startswith("$2b$") or hashed_password.startswith("$2a$")):
                return plain_password == hashed_password
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False

# --- Database URLs ---
# Default to pgdatabase for project-specific data (Tarot)
PROJECT_DATABASE_URL = os.getenv("PROJECT_DATABASE_URL") or os.getenv("DATABASE_URL")
# Default to ai-factory for global identity data (Mentors/Friends/Messages)
FACTORY_DATABASE_URL = os.getenv("FACTORY_DATABASE_URL")

if not FACTORY_DATABASE_URL:
    # Use same host/user as project but different DB name if not explicitly set
    user = os.getenv("POSTGRES_USER", "toby")
    password = os.getenv("POSTGRES_PASSWORD", "andy1984")
    host = os.getenv("POSTGRES_HOST", "192.168.0.150")
    port = os.getenv("POSTGRES_PORT", "5432")
    FACTORY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/ai-factory"

# --- Engines & Sessions ---
project_engine = create_engine(PROJECT_DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)
ProjectSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=project_engine)

factory_engine = create_engine(FACTORY_DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)
FactorySessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=factory_engine)

# --- Metadata ---
project_metadata = MetaData()
factory_metadata = MetaData()

# --- Backward Compatibility Aliases ---
engine = project_engine
SessionLocal = ProjectSessionLocal
metadata = project_metadata

# --- Project Specific Tables (Tarot) ---
readings = Table(
    'readings', project_metadata,
    Column('id', String(36), primary_key=True),
    Column('record_type', String(50), nullable=False),
    Column('created_at', DateTime(timezone=True), nullable=False),
    Column('time_display', String(20)),
    Column('mentor_id', String(100), nullable=False, default='toby'),
    Column('client_id', String(100), nullable=False, default='toby'),
    Column('question', Text, nullable=False),
    Column('result', JSON, nullable=False),
    Column('ai_prompt', Text),
    Column('ai_interpretation', Text),
    Column('ai_status', JSON),
    Column('audio_path', String(255)),
    Column('recovered_at', DateTime(timezone=True))
)

# --- Global Factory Tables (Identity & Social) ---
mentors = Table(
    'mentors', factory_metadata,
    Column('mentor_id', String(100), primary_key=True),
    Column('password', String(255), nullable=False),
    Column('email', String(255), unique=True, nullable=True),
    Column('status', String(20), default='active'), 
    Column('verification_token', String(100), nullable=True),
    Column('enable_multiuser_login', Boolean, default=False),
    Column('usage_limit', Integer, default=5),
    Column('bgm_id', Integer, default=1),
    Column('room_level', String(20), default='single'),
    Column('ai_enabled', Boolean, default=True),
    Column('max_clients', Integer, default=1),
    Column('created_at', DateTime(timezone=True), server_default=func.now()),
    Column('last_active_at', DateTime(timezone=True), server_default=func.now()),
    Column('announcement', Text, default='')
)

mentor_friends = Table(
    'mentor_friends', factory_metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('requester_id', String(100), ForeignKey('mentors.mentor_id', ondelete='CASCADE'), nullable=False),
    Column('receiver_id', String(100), ForeignKey('mentors.mentor_id', ondelete='CASCADE'), nullable=False),
    Column('status', String(20), default='pending'), 
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)

mentor_messages = Table(
    'mentor_messages', factory_metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sender_id', String(100), ForeignKey('mentors.mentor_id', ondelete='CASCADE'), nullable=False),
    Column('receiver_id', String(100), ForeignKey('mentors.mentor_id', ondelete='CASCADE'), nullable=False),
    Column('message', Text, nullable=False),
    Column('is_read', Boolean, default=False),
    Column('timestamp', DateTime(timezone=True), server_default=func.now())
)

def init_db():
    """初始化兩大資料庫：專案資料庫與全局身分庫"""
    try:
        # 1. 初始化專案資料庫 (Tarot)
        project_metadata.create_all(project_engine)
        logger.info("專案資料庫 (Project DB) 表已確認。")

        # 2. 初始化全局身分庫 (AI-Factory)
        # 注意：這需要 ai-factory 資料庫已存在於 PG Server 中
        factory_metadata.create_all(factory_engine)
        
        # 自動遷移：補齊 mentors 缺失欄位
        with factory_engine.connect() as conn:
            missing_cols = [
                ("email", "VARCHAR(255) UNIQUE"),
                ("status", "VARCHAR(20) DEFAULT 'active'"),
                ("verification_token", "VARCHAR(100)"),
                ("room_level", "VARCHAR(20) DEFAULT 'single'"),
                ("ai_enabled", "BOOLEAN DEFAULT TRUE"),
                ("max_clients", "INTEGER DEFAULT 1"),
                ("announcement", "TEXT DEFAULT ''")
            ]
            for col_name, col_type in missing_cols:
                try:
                    conn.execute(text(f"ALTER TABLE mentors ADD COLUMN {col_name} {col_type}"))
                    conn.commit()
                except Exception:
                    pass
            
            # Auto-migrate mentor_messages
            try:
                conn.execute(text("ALTER TABLE mentor_messages ADD COLUMN is_read BOOLEAN DEFAULT FALSE"))
                conn.commit()
            except Exception:
                pass
        
        logger.info("全局身分庫 (Factory DB) 表已確認並初始化。")
        
        # 預先植入超級管理員 toby 到全局庫
        with FactorySessionLocal() as db:
            toby_exists = db.execute(select(mentors).where(mentors.c.mentor_id == 'toby')).first()
            if not toby_exists:
                db.execute(insert(mentors).values(
                    mentor_id='toby',
                    password='wang',
                    email='admin@ai-tarot.com',
                    status='active',
                    enable_multiuser_login=True,
                    usage_limit=-1,
                    bgm_id=1,
                    room_level='multi',
                    ai_enabled=True,
                    max_clients=10
                ))
                db.commit()
                logger.info("已在全局身分庫建立 SuperAdmin toby 帳號")
    except Exception as e:
        logger.error(f"資料庫初始化失敗: {e}")

def get_db():
    """提供 Project DB Session (預設)"""
    db = ProjectSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_factory_db():
    """提供 Factory Identity DB Session"""
    db = FactorySessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_and_deduct_usage(mentor_id: str) -> bool:
    """檢查並扣除導師的使用額度 (使用 Factory DB)"""
    with FactorySessionLocal() as db:
        mentor = db.execute(select(mentors).where(mentors.c.mentor_id == mentor_id)).first()
        if not mentor:
            raise HTTPException(status_code=403, detail="Mentor 不存在")
            
        if mentor.usage_limit > 0:
            db.execute(update(mentors).where(mentors.c.mentor_id == mentor_id).values(usage_limit=mentor.usage_limit - 1))
            db.commit()
        elif mentor.usage_limit == 0:
            raise HTTPException(status_code=403, detail="可用次數已用盡 (Usage Limit Exceeded). 請聯絡管理員以取得更多點數。")
            
        return {
            "enable_multiuser": mentor.enable_multiuser_login,
            "ai_enabled": mentor.ai_enabled,
            "max_clients": mentor.max_clients,
            "room_level": mentor.room_level
        }
