from fastapi import APIRouter, HTTPException
from api.schemas import TarotDrawRequest, TarotResponse, TarotCardResponse, SpreadInfoResponse
from core.tarot.engine import DrawEngine
from core.tarot.spreads import get_spread_by_id, ALL_SPREADS, SINGLE_CARD
from core.tarot.interpreter import get_ai_interpretation
from core.tts import generate_audio
from core.history import save_reading, update_record_interpretation
from core.config_manager import config_manager
from api.websocket_manager import manager
from datetime import datetime
import uuid
from typing import List

router = APIRouter(prefix="/api/tarot", tags=["Tarot"])
engine = DrawEngine()

@router.get("/spreads", response_model=List[SpreadInfoResponse])
def get_spreads():
    """取得所有支援的塔羅牌陣"""
    return [
        SpreadInfoResponse(
            id=s.id,
            name=s.name,
            description=s.description,
            icon=s.icon,
            card_count=s.card_count
        )
        for s in ALL_SPREADS
    ]

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
            position_name=spread.positions[i].name if i < len(spread.positions) else "",
            image_path=f"/assets/images/tarot/{drawn.card.image}"
        ))
        
    interpretation_text = ""
    audio_file = ""
    
    if req.question:
        interpretation_text = get_ai_interpretation(req.question, result, language=req.language)
        
        client_name = config_manager.get().app.get("guide_name", "toby")
        if manager.active_client:
            client_name = manager.active_client[1]
            
        record_id = save_reading(
            record_type="tarot",
            question=req.question,
            result=result,
            interpretation=interpretation_text,
            ai_prompt="",
            search_success=False,
            client_name=client_name
        )

        if interpretation_text and "error" not in interpretation_text.lower() and not interpretation_text.startswith("⚠️"):
            # generate audio
            audio_file = generate_audio(interpretation_text, f"{record_id}_tarot")
            if audio_file:
                update_record_interpretation(datetime.now().strftime("%Y-%m-%d"), record_id, interpretation_text, audio_file)
            
    return TarotResponse(
        spread_name=spread.name,
        cards=cards_res,
        interpretation=interpretation_text if req.question else None,
        audio_path=audio_file if audio_file else None
    )
