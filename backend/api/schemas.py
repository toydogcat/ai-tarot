from pydantic import BaseModel
from typing import List, Optional, Any, Dict

class TarotDrawRequest(BaseModel):
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
    ai_interpretation_audio_path: Optional[str] = None
