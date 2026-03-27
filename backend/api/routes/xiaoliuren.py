from fastapi import APIRouter, HTTPException
from api.schemas import DivinationRequest, DivinationResponse
from core.xiaoliuren.engine import XiaoliurenEngine
from core.xiaoliuren.interpreter import interpret_xiaoliuren
from core.tts import generate_audio
from core.history import save_reading
from core.config_manager import config_manager
from api.websocket_manager import manager
import asyncio

from core.db import check_and_deduct_usage

router = APIRouter(prefix="/api/xiaoliuren", tags=["xiaoliuren"])

@router.post("/draw", response_model=DivinationResponse)
async def draw_xiaoliuren(request: DivinationRequest):
    mentor_settings = check_and_deduct_usage(request.mentor_id)
    enable_multiuser = mentor_settings["enable_multiuser"]
    ai_enabled = mentor_settings["ai_enabled"]

    try:
        conf = config_manager.get()

        # Engine
        engine = XiaoliurenEngine()
        lesson = engine.draw_lesson()
        
        # Audio
        audio_conf = conf.get("audio", {})
        generate_audio_flag = audio_conf.get("generate_audio", False)
        
        # Determine Model
        model_name = conf.ai_models.get("divination_model", "gemini-3.1-flash-lite-preview")
        system_prompt = conf.ai_models.get("system_prompt", "")
        
        # Get AI
        # Determine client name and solo mode status
        client_name = request.mentor_id
        is_solo = True
        room = manager.rooms.get(request.mentor_id)
        if room and room.main_client:
            client_name = room.main_client.name
            is_solo = False
            
        # Interpretation Logic
        interpretation = ""
        # Room-level ai_enabled is the master switch
        if ai_enabled and request.enable_ai and (enable_multiuser or not is_solo):
            interpretation = interpret_xiaoliuren(
                question=request.question,
                result_data=lesson,
                language="繁體中文",
                selected_model=model_name,
                system_prompt=system_prompt
            )
        else:
            # Solo Mode, Trial Mode, or AI Disabled by Mentor
            if not enable_multiuser:
                interpretation = "⚠️ [Trial Mode] AI Interpretation Disabled. Support the project to unlock!"
            elif not ai_enabled:
                interpretation = "💡 AI Interpretation is currently DISABLED in your room settings."
            else:
                interpretation = "💡 [Solo Mode] Mentor testing - AI interpretation skipped."

        audio_path = None
        # Save History
        record_id = save_reading(
            record_type="xiaoliuren",
            question=request.question or "無問題",
            result=lesson,
            interpretation=interpretation,
            ai_prompt=system_prompt,
            ai_interpretation_audio_path=audio_path,
            client_id=client_name,
            mentor_id=request.mentor_id,
            is_multiuser=enable_multiuser
        )
        
        # Audio generation logic
        if interpretation not in ["error", ""] and not interpretation.startswith(("⚠️", "💡")) and generate_audio_flag:
            try:
                actual_audio_path = await generate_audio(interpretation, record_id)
                if actual_audio_path:
                    audio_path = actual_audio_path
                    from core.history import update_record_interpretation
                    import datetime
                    today = datetime.datetime.now().strftime("%Y-%m-%d")
                    update_record_interpretation(today, record_id, interpretation, audio_path)
            except Exception as e:
                print(f"TTS Error: {e}")

        # Notify via Websocket (Only if client is connected)
        if room and room.main_client:
            push_data = {
                "type": "divination_result",
                "mode": "xiaoliuren",
                "question": request.question,
                "result": lesson,
                "interpretation": interpretation,
                "audio_path": audio_path,
                "record_id": record_id
            }
            asyncio.create_task(manager.send_to_client(request.mentor_id, push_data))

        return DivinationResponse(
            record_id=record_id,
            result=lesson,
            interpretation=interpretation,
            audio_path=audio_path
        )
            
    except Exception as e:
        print(f"XiaoLiuRen Endpoint Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
