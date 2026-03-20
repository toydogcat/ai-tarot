from fastapi import APIRouter
from api.schemas import TarotDrawRequest, TarotResponse, TarotCardResponse
from core.tarot.engine import DrawEngine
from core.tarot.spreads import get_spread_by_id, SINGLE_CARD
from core.tarot.interpreter import get_ai_interpretation
from core.tts import generate_audio
import uuid

router = APIRouter(prefix="/api/tarot", tags=["Tarot"])
engine = DrawEngine()

@router.post("/draw", response_model=TarotResponse)
def draw_tarot(req: TarotDrawRequest):
    spread = get_spread_by_id(req.spread_id)
    if not spread:
        spread = SINGLE_CARD
    
    result = engine.draw_spread(spread=spread)
    
    cards_res = []
    for i, drawn in enumerate(result.drawn_cards):
        cards_res.append(TarotCardResponse(
            name=drawn.card.name,
            name_zh=drawn.card.name_zh,
            is_reversed=drawn.is_reversed,
            meaning=drawn.current_meaning.meaning,
            position_name=spread.positions[i].name if i < len(spread.positions) else ""
        ))
        
    interpretation_text = ""
    audio_file = ""
    
    if req.question:
        interpretation_text = get_ai_interpretation(req.question, result)
        if interpretation_text and "error" not in interpretation_text.lower() and not interpretation_text.startswith("⚠️"):
            # generate audio
            audio_file = generate_audio(interpretation_text, f"{uuid.uuid4().hex[:8]}_tarot")
            
    return TarotResponse(
        spread_name=spread.name,
        cards=cards_res,
        interpretation=interpretation_text if req.question else None,
        audio_path=audio_file if audio_file else None
    )
