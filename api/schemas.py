from pydantic import BaseModel
from typing import List, Optional

class TarotDrawRequest(BaseModel):
    spread_id: str = "single"
    question: Optional[str] = None

class TarotCardResponse(BaseModel):
    name: str
    name_zh: str
    is_reversed: bool
    meaning: str
    position_name: str

class TarotResponse(BaseModel):
    spread_name: str
    cards: List[TarotCardResponse]
    interpretation: Optional[str] = None
    audio_path: Optional[str] = None

class IChingCastRequest(BaseModel):
    question: Optional[str] = None

class IChingResponse(BaseModel):
    hexagram_name: str
    hexagram_description: str
    lines: List[str]
    moving_indices: List[int]
    upper_trigram: str
    lower_trigram: str
    interpretation: Optional[str] = None
    audio_path: Optional[str] = None
