from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import or_, and_, select, insert, update, desc, delete, func
from typing import List

from api.schemas import (
    FriendRequest, FriendStatusResponse, SendMessageRequest, ChatMessageResponse, FriendInfo,
    NotificationSummary, NotificationItem, FriendRequestItem, FriendResponseRequest
)
from core.db import FactorySessionLocal, mentor_friends, mentor_messages, mentors
from api.websocket_manager import manager

router = APIRouter(prefix="/api/social", tags=["Social"])

def get_db():
    db = FactorySessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/friends/request", response_model=FriendStatusResponse)
async def add_friend(req: FriendRequest, db=Depends(get_db)):
    import asyncio
    
    def db_op():
        if req.mentor_id == req.target_id:
            raise HTTPException(status_code=400, detail="不能加自己為好友")

        target = db.execute(select(mentors).where(mentors.c.mentor_id == req.target_id)).first()
        if not target:
            raise HTTPException(status_code=404, detail="目標導師不存在")

        existing = db.execute(select(mentor_friends).where(
            or_(
                and_(mentor_friends.c.requester_id == req.mentor_id, mentor_friends.c.receiver_id == req.target_id),
                and_(mentor_friends.c.requester_id == req.target_id, mentor_friends.c.receiver_id == req.mentor_id)
            )
        )).first()

        if existing:
            raise HTTPException(status_code=400, detail="好友邀請已存在或是已經是好友")

        # Insert pending request
        result = db.execute(insert(mentor_friends).values(
            requester_id=req.mentor_id,
            receiver_id=req.target_id,
            status="pending"
        ).returning(mentor_friends.c.id))
        db.commit()
        return result.scalar()

    new_id = await asyncio.to_thread(db_op)

    await manager.send_to_mentor(req.target_id, {
        "type": "friend_request",
        "from": req.mentor_id
    })

    return FriendStatusResponse(id=new_id, requester_id=req.mentor_id, receiver_id=req.target_id, status="pending")

@router.post("/friends/accept", response_model=FriendStatusResponse)
async def accept_friend(req: FriendRequest, db=Depends(get_db)):
    import asyncio

    def db_op():
        existing = db.execute(select(mentor_friends).where(
            and_(mentor_friends.c.requester_id == req.target_id, mentor_friends.c.receiver_id == req.mentor_id, mentor_friends.c.status == 'pending')
        )).first()

        if not existing:
            raise HTTPException(status_code=404, detail="找不到待處理的好友邀請")

        db.execute(update(mentor_friends).where(mentor_friends.c.id == existing.id).values(status='accepted'))
        db.commit()
        return existing

    existing = await asyncio.to_thread(db_op)

    await manager.send_to_mentor(req.target_id, {
        "type": "friend_accepted",
        "from": req.mentor_id
    })

    return FriendStatusResponse(id=existing.id, requester_id=req.target_id, receiver_id=req.mentor_id, status="accepted")

@router.post("/friends/respond", response_model=FriendStatusResponse)
async def respond_friend(req: FriendResponseRequest, db=Depends(get_db)):
    import asyncio
    
    def db_op():
        existing = db.execute(select(mentor_friends).where(
            and_(mentor_friends.c.requester_id == req.requester_id, mentor_friends.c.receiver_id == req.mentor_id, mentor_friends.c.status == 'pending')
        )).first()

        if not existing:
            raise HTTPException(status_code=404, detail="找不到待處理的好友邀請")

        new_status = 'accepted' if req.action == 'accept' else 'declined'
        if req.action == 'accept':
            db.execute(update(mentor_friends).where(mentor_friends.c.id == existing.id).values(status='accepted'))
        else:
            db.execute(delete(mentor_friends).where(mentor_friends.c.id == existing.id)) # Or just delete for decline
        
        db.commit()
        return existing, new_status

    existing, actual_status = await asyncio.to_thread(db_op)

    if actual_status == 'accepted':
        await manager.send_to_mentor(req.requester_id, {
            "type": "friend_accepted",
            "from": req.mentor_id
        })

    return FriendStatusResponse(id=existing.id, requester_id=req.requester_id, receiver_id=req.mentor_id, status=actual_status)

@router.get("/friends/pending", response_model=List[FriendRequestItem])
def list_pending_friends(mentor_id: str, db=Depends(get_db)):
    pending = db.execute(select(mentor_friends).where(
        and_(mentor_friends.c.receiver_id == mentor_id, mentor_friends.c.status == 'pending')
    )).fetchall()
    
    return [FriendRequestItem(id=p.id, requester_id=p.requester_id, created_at=p.created_at.isoformat()) for p in pending]

@router.get("/notifications", response_model=NotificationSummary)
def get_notifications(mentor_id: str, db=Depends(get_db)):
    # 1. Pending friend requests
    pending_count = db.execute(select(func.count(mentor_friends.c.id)).where(
        and_(mentor_friends.c.receiver_id == mentor_id, mentor_friends.c.status == 'pending')
    )).scalar() or 0
    
    # 2. Unread messages count (distinct senders)
    unread_senders = db.execute(select(func.count(func.distinct(mentor_messages.c.sender_id))).where(
        and_(mentor_messages.c.receiver_id == mentor_id, mentor_messages.c.is_read == False)
    )).scalar() or 0
    
    # 3. Recent notifications (mix of friend req and unread msg)
    recent: List[NotificationItem] = []
    
    # Latest 5 pending friend requests
    pending_list = db.execute(select(mentor_friends).where(
        and_(mentor_friends.c.receiver_id == mentor_id, mentor_friends.c.status == 'pending')
    ).order_by(desc(mentor_friends.c.created_at)).limit(5)).fetchall()
    
    for p in pending_list:
        recent.append(NotificationItem(
            type='friend_request',
            sender_id=p.requester_id,
            message=f"{p.requester_id} 向您送出了好友邀請",
            timestamp=p.created_at.isoformat(),
            payload={"id": p.id}
        ))
        
    # Latest 5 unread messages
    unread_list = db.execute(select(mentor_messages).where(
        and_(mentor_messages.c.receiver_id == mentor_id, mentor_messages.c.is_read == False)
    ).order_by(desc(mentor_messages.c.timestamp)).limit(5)).fetchall()
    
    for m in unread_list:
        recent.append(NotificationItem(
            type='unread_message',
            sender_id=m.sender_id,
            message=m.message[:30] + ("..." if len(m.message) > 30 else ""),
            timestamp=m.timestamp.isoformat(),
            payload={"id": m.id}
        ))
        
    # Sort recent by timestamp
    recent.sort(key=lambda x: x.timestamp, reverse=True)
    
    final_recent = recent[:10]
    
    return NotificationSummary(
        unread_messages_count=unread_senders,
        pending_friends_count=pending_count,
        recent_notifications=final_recent
    )

@router.post("/messages/read")
def mark_messages_as_read(mentor_id: str, sender_id: str, db=Depends(get_db)):
    db.execute(update(mentor_messages).where(
        and_(mentor_messages.c.receiver_id == mentor_id, mentor_messages.c.sender_id == sender_id, mentor_messages.c.is_read == False)
    ).values(is_read=True))
    db.commit()
    return {"status": "success"}

@router.get("/friends/list", response_model=List[FriendInfo])
def list_friends(mentor_id: str, db=Depends(get_db)):
    # Fetch friends where status = accepted
    accepted_links = db.execute(select(mentor_friends).where(
        and_(
            or_(mentor_friends.c.requester_id == mentor_id, mentor_friends.c.receiver_id == mentor_id),
            mentor_friends.c.status == 'accepted'
        )
    )).fetchall()

    friends = []
    for link in accepted_links:
        friend_id = link.receiver_id if link.requester_id == mentor_id else link.requester_id
        is_online = manager.get_room(friend_id).active_mentor is not None
        friends.append(FriendInfo(mentor_id=friend_id, status="accepted", is_online=is_online))
        
    return friends

@router.post("/chat/send", response_model=ChatMessageResponse)
async def send_chat_message(req: SendMessageRequest, db=Depends(get_db)):
    import asyncio

    def db_op():
        # Verify friendship
        existing = db.execute(select(mentor_friends).where(
            and_(
                or_(
                    and_(mentor_friends.c.requester_id == req.mentor_id, mentor_friends.c.receiver_id == req.receiver_id),
                    and_(mentor_friends.c.requester_id == req.receiver_id, mentor_friends.c.receiver_id == req.mentor_id)
                ),
                mentor_friends.c.status == 'accepted'
            )
        )).first()

        if not existing:
            raise HTTPException(status_code=403, detail="必須互為好友才能傳送訊息")

        result = db.execute(insert(mentor_messages).values(
            sender_id=req.mentor_id,
            receiver_id=req.receiver_id,
            message=req.message
        ).returning(mentor_messages.c.id, mentor_messages.c.timestamp))
        db.commit()
        return result.first()

    inserted = await asyncio.to_thread(db_op)

    await manager.send_to_mentor(req.receiver_id, {
        "type": "chat_message",
        "from": req.mentor_id,
        "message": req.message,
        "timestamp": inserted.timestamp.isoformat()
    })

    return ChatMessageResponse(
        id=inserted.id,
        sender_id=req.mentor_id,
        receiver_id=req.receiver_id,
        message=req.message,
        timestamp=inserted.timestamp.isoformat()
    )

@router.get("/chat/history", response_model=List[ChatMessageResponse])
def get_chat_history(mentor_id: str, target_id: str, db=Depends(get_db)):
    messages = db.execute(select(mentor_messages).where(
        or_(
            and_(mentor_messages.c.sender_id == mentor_id, mentor_messages.c.receiver_id == target_id),
            and_(mentor_messages.c.sender_id == target_id, mentor_messages.c.receiver_id == mentor_id)
        )
    ).order_by(desc(mentor_messages.c.timestamp)).limit(50)).fetchall()

    res = []
    for rm in reversed(messages): # Return chrono order
        res.append(ChatMessageResponse(
            id=rm.id,
            sender_id=rm.sender_id,
            receiver_id=rm.receiver_id,
            message=rm.message,
            timestamp=rm.timestamp.isoformat()
        ))
    return res
