from fastapi import APIRouter
from api.schemas import DaliurenCastRequest, DaliurenResponse
from core.daliuren.engine import DaliurenEngine
from core.daliuren.interpreter import interpret_daliuren
from core.tts import generate_audio
from core.history import save_reading, update_record_interpretation
from core.config_manager import config_manager
from api.websocket_manager import manager
from datetime import datetime

from core.db import check_and_deduct_usage

router = APIRouter(prefix="/api/daliuren", tags=["Daliuren"])

@router.post("/cast", response_model=DaliurenResponse)
async def cast_daliuren(req: DaliurenCastRequest):
    mentor_settings = check_and_deduct_usage(req.mentor_id)
    enable_multiuser = mentor_settings["enable_multiuser"]
    ai_enabled = mentor_settings["ai_enabled"]

    engine = DaliurenEngine()
    result = engine.draw_lesson()
    
    interpretation_text = ""
    audio_file = ""
    
    if req.question:
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
            conf = config_manager.get()
            model_name = conf.ai_models.get("divination_model", "gemini-3.1-flash-lite-preview")
            interpretation_text = interpret_daliuren(req.question, result, language=req.language, selected_model=model_name)
        else:
            # Solo Mode, Trial Mode, or AI Disabled by Mentor
            if not enable_multiuser:
                interpretation_text = "⚠️ [Trial Mode] AI Interpretation Disabled. Support the project to unlock!"
            elif not ai_enabled:
                interpretation_text = "💡 AI Interpretation is currently DISABLED in your room settings."
            else:
                interpretation_text = "💡 [Solo Mode] Mentor testing - AI interpretation skipped."
            
        record_id = save_reading(
            record_type="daliuren",
            question=req.question,
            result=result,
            interpretation=interpretation_text,
            client_id=client_name,
            mentor_id=req.mentor_id,
            is_multiuser=enable_multiuser
        )

        if interpretation_text and "error" not in interpretation_text.lower() and not interpretation_text.startswith("⚠️"):
            # generate audio
            audio_file = await generate_audio(interpretation_text, f"{record_id}_daliuren")
            if audio_file:
                update_record_interpretation(datetime.now().strftime("%Y-%m-%d"), record_id, interpretation_text, audio_file)
            
    return DaliurenResponse(
        date=result.get("date", ""),
        jieqi=result.get("jieqi", ""),
        pattern=result.get("pattern", []),
        san_chuan=result.get("san_chuan", {}),
        si_ke=result.get("si_ke", {}),
        interpretation=interpretation_text if req.question else None,
        audio_path=audio_file if audio_file else None
    )
