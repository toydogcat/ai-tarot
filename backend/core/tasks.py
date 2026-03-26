import logging
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import text
from core.db import engine, factory_engine
from core.logger import get_logger

logger = get_logger("cleanup_tasks")

def cleanup_old_messages():
    """清理超過 7 天的歷史對話訊息"""
    try:
        with factory_engine.begin() as conn:
            result = conn.execute(text("DELETE FROM mentor_messages WHERE timestamp < NOW() - INTERVAL '7 days'"))
            if result.rowcount > 0:
                logger.info(f"自動清理了 {result.rowcount} 筆超過 7 天的歷史社群訊息。")
    except Exception as e:
        logger.error(f"清理過期訊息失敗: {e}")

def cleanup_inactive_trial_mentors():
    """清理超過 1 個月未活動的試用版單人導師帳號"""
    try:
        with factory_engine.begin() as conn:
            # 排除 toby 以及開通了多人模式的帳號
            result = conn.execute(text("""
                DELETE FROM mentors 
                WHERE enable_multiuser_login = false 
                  AND mentor_id != 'toby'
                  AND last_active_at < NOW() - INTERVAL '1 month'
            """))
            if result.rowcount > 0:
                logger.info(f"自動清理了 {result.rowcount} 名超過 1 個月未活動的單人試用導師帳號。")
    except Exception as e:
        logger.error(f"清理過期導師失敗: {e}")

def cleanup_old_readings():
    """清理超過 7 天的歷史占卜紀錄"""
    try:
        with engine.begin() as conn:
            result = conn.execute(text("DELETE FROM readings WHERE created_at < NOW() - INTERVAL '7 days'"))
            if result.rowcount > 0:
                logger.info(f"自動清理了 {result.rowcount} 筆超過 7 天的歷史占卜紀錄。")
    except Exception as e:
        logger.error(f"清理過期占卜紀錄失敗: {e}")

_scheduler = None

def start_scheduler():
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler()
        # 每天清晨 3 點執行訊息清理
        _scheduler.add_job(cleanup_old_messages, 'cron', hour=3, minute=0)
        # 每天清晨 3 點 15 分執行導師清理
        _scheduler.add_job(cleanup_inactive_trial_mentors, 'cron', hour=3, minute=15)
        # 每天清晨 3 點 30 分執行占卜紀錄清理
        _scheduler.add_job(cleanup_old_readings, 'cron', hour=3, minute=30)
        _scheduler.start()
        logger.info("自動清理背景排程器 (APScheduler) 起啟動完成。")

def shutdown_scheduler():
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown()
        _scheduler = None
        logger.info("自動清理背景排程器已關閉。")
