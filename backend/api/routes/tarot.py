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

from core.db import check_and_deduct_usage

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
async def draw_tarot(req: TarotDrawRequest):
    mentor_settings = check_and_deduct_usage(req.mentor_id)
    enable_multiuser = mentor_settings["enable_multiuser"]
    ai_enabled = mentor_settings["ai_enabled"]

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
        
    # Determine client name and solo mode status
    client_name = req.mentor_id
    is_solo = True
    room = manager.rooms.get(req.mentor_id)
    if room and room.main_client:
        client_name = room.main_client.name
        is_solo = False
        
    # Interpretation Logic
    interpretation_text = ""
    if enable_multiuser and ai_enabled and not is_solo:
        interpretation_text = get_ai_interpretation(req.question, result, language=req.language)
    else:
        # Solo Mode, Trial Mode, or AI Disabled by Mentor
        if not enable_multiuser:
            interpretation_text = "⚠️ [Trial Mode] AI Interpretation Disabled. Support the project to unlock!"
        elif not ai_enabled:
            interpretation_text = "💡 AI Interpretation is currently DISABLED in your room settings."
        else:
            interpretation_text = "💡 [Solo Mode] Mentor testing - AI interpretation skipped."
        
    record_id = save_reading(
        record_type="tarot",
        question=req.question,
        result=result,
        interpretation=interpretation_text,
        ai_prompt="",
        search_success=False,
        client_id=client_name,
        mentor_id=req.mentor_id,
        is_multiuser=enable_multiuser
    )

    audio_file = ""
    if interpretation_text and "error" not in interpretation_text.lower() and not interpretation_text.startswith("⚠️"):
        # generate audio
        audio_file = await generate_audio(interpretation_text, f"{record_id}_tarot")
        if audio_file:
            update_record_interpretation(datetime.now().strftime("%Y-%m-%d"), record_id, interpretation_text, audio_file)
            
    return TarotResponse(
        spread_name=spread.name,
        cards=cards_res,
        interpretation=interpretation_text if req.question else None,
        audio_path=audio_file if audio_file else None
    )
