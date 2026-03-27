from pydantic import BaseModel
from typing import List, Optional, Any, Dict

class TarotDrawRequest(BaseModel):
    mentor_id: str
    spread_id: str = "single"
    question: Optional[str] = None
    language: Optional[str] = "繁體中文"

class TarotCardResponse(BaseModel):
    name: str
    name_zh: str
    is_reversed: bool
    meaning: str
    position_name: str
    image_path: str

class TarotResponse(BaseModel):
    spread_name: str
    cards: List[TarotCardResponse]
    interpretation: Optional[str] = None
    audio_path: Optional[str] = None

class IChingCastRequest(BaseModel):
    mentor_id: str
    question: Optional[str] = None
    language: Optional[str] = "繁體中文"

class IChingResponse(BaseModel):
    hexagram_id: int
    hexagram_name: str
    hexagram_description: str
    lines: List[str]
    lines_binary: List[int]
    moving_indices: List[int]
    upper_trigram: str
    lower_trigram: str
    changed_hexagram_id: Optional[int] = None
    changed_hexagram_name: Optional[str] = None
    interpretation: Optional[str] = None
    audio_path: Optional[str] = None

class SpreadInfoResponse(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    card_count: int

class HistoryRecordResponse(BaseModel):
    id: str
    timestamp: str
    question: str
    
    # Defaults for older records
    type: str = "tarot"
    time_display: str = ""
    result: Dict[str, Any] = {}
    
    # Legacy fields
    spread: Optional[Dict[str, Any]] = None
    cards: Optional[List[Dict[str, Any]]] = None
    original_hexagram: Optional[str] = None
    changed_hexagram: Optional[str] = None
    
    ai_interpretation: Optional[str] = None
    audio_path: Optional[str] = None

class ZhugeDrawRequest(BaseModel):
    mentor_id: str
    question: Optional[str] = None
    language: Optional[str] = "繁體中文"

class ZhugeResponse(BaseModel):
    id: str
    poem: str
    explanation: Optional[str] = None
    interp1: Optional[str] = None
    interp2: Optional[str] = None
    interpretation: Optional[str] = None
    audio_path: Optional[str] = None

class DaliurenCastRequest(BaseModel):
    mentor_id: str
    question: Optional[str] = None
    language: Optional[str] = "繁體中文"

class DaliurenResponse(BaseModel):
    date: str
    jieqi: str
    pattern: List[str]
    san_chuan: Dict[str, Any]
    si_ke: Dict[str, Any]
    interpretation: Optional[str] = None
    audio_path: Optional[str] = None

class DivinationRequest(BaseModel):
    mentor_id: str
    question: Optional[str] = None
    language: Optional[str] = "繁體中文"
    enable_ai: Optional[bool] = True

class DivinationResponse(BaseModel):
    record_id: Optional[str] = None
    result: Dict[str, Any]
    interpretation: Optional[str] = None
    audio_path: Optional[str] = None

# ---- Social Networking Schemas ----

class FriendRequest(BaseModel):
    mentor_id: str
    target_id: str

class FriendStatusResponse(BaseModel):
    id: int
    requester_id: str
    receiver_id: str
    status: str

class SendMessageRequest(BaseModel):
    mentor_id: str
    receiver_id: str
    message: str

class ChatMessageResponse(BaseModel):
    id: int
    sender_id: str
    receiver_id: str
    message: str
    timestamp: str

class FriendInfo(BaseModel):
    mentor_id: str
    status: str
    is_online: bool

# ---- Notification Schemas ----

class NotificationItem(BaseModel):
    type: str # 'friend_request', 'unread_message', 'system'
    sender_id: str
    message: str
    timestamp: str
    payload: Optional[Dict[str, Any]] = None

class NotificationSummary(BaseModel):
    unread_messages_count: int
    pending_friends_count: int
    recent_notifications: List[NotificationItem]

class FriendRequestItem(BaseModel):
    id: int
    requester_id: str
    created_at: str

class FriendResponseRequest(BaseModel):
    mentor_id: str
    requester_id: str
    action: str # 'accept' or 'decline'
