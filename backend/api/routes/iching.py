from fastapi import APIRouter
from api.schemas import IChingCastRequest, IChingResponse
from core.iching.engine import perform_divination
from core.iching.interpreter import get_ai_interpretation
from core.tts import generate_audio
from core.history import save_reading, update_record_interpretation
from core.config_manager import config_manager
from api.websocket_manager import manager
from datetime import datetime
import uuid

from core.db import check_and_deduct_usage

router = APIRouter(prefix="/api/iching", tags=["IChing"])

@router.post("/cast", response_model=IChingResponse)
async def cast_iching(req: IChingCastRequest):
    mentor_settings = check_and_deduct_usage(req.mentor_id)
    enable_multiuser = mentor_settings["enable_multiuser"]
    ai_enabled = mentor_settings["ai_enabled"]

    result = perform_divination()
    
    lines_info = result["lines_info"]
    moving_indices = [i for i, line in enumerate(lines_info) if line["moving"]]
    hex_data = result["original_hexagram"]
    
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
            record_type="iching",
            question=req.question,
            result=result,
            interpretation=interpretation_text,
            ai_prompt="",
            search_success=False,
            client_id=client_name,
            mentor_id=req.mentor_id,
            is_multiuser=enable_multiuser
        )

        if interpretation_text and "error" not in interpretation_text.lower() and not interpretation_text.startswith("⚠️"):
            # generate audio
            audio_file = await generate_audio(interpretation_text, f"{record_id}_iching")
            if audio_file:
                update_record_interpretation(datetime.now().strftime("%Y-%m-%d"), record_id, interpretation_text, audio_file)
            
    return IChingResponse(
        hexagram_id=hex_data["id"],
        hexagram_name=hex_data["name"],
        hexagram_description=hex_data["description"],
        lines=hex_data["lines"],
        lines_binary=[line["original"] for line in lines_info],
        moving_indices=moving_indices,
        upper_trigram=hex_data["trigrams"]["upper"],
        lower_trigram=hex_data["trigrams"]["lower"],
        changed_hexagram_id=result.get("changed_hexagram", {}).get("id") if result.get("changed_hexagram") else None,
        changed_hexagram_name=result.get("changed_hexagram", {}).get("name") if result.get("changed_hexagram") else None,
        interpretation=interpretation_text if req.question else None,
        audio_path=audio_file if audio_file else None
    )
