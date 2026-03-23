from fastapi import APIRouter, HTTPException
from api.schemas import DivinationRequest, DivinationResponse
from core.xiaoliuren.engine import XiaoliurenEngine
from core.xiaoliuren.interpreter import interpret_xiaoliuren
from core.tts import generate_audio
from core.history import save_reading
from core.config_manager import config_manager
from api.websocket_manager import manager
import asyncio

router = APIRouter(prefix="/api/xiaoliuren", tags=["xiaoliuren"])

@router.post("/draw", response_model=DivinationResponse)
async def draw_xiaoliuren(request: DivinationRequest):
    limit = config_manager.get_remaining_usage()
    if limit <= 0:
        raise HTTPException(status_code=403, detail="可用次數已用盡 (Limit Exceeded)")
    config_manager.decrement_usage()

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
        interpretation = "error"
        audio_path = "error" if generate_audio_flag else None
        record_id = None
        
        if request.enable_ai:
            interpretation = interpret_xiaoliuren(
                question=request.question,
                result_data=lesson,
                language="繁體中文",
                selected_model=model_name,
                system_prompt=system_prompt
            )
            
            # Save history early to get record_id
            record_id = save_reading(
                record_type="xiaoliuren",
                question=request.question or "無問題",
                result=lesson,
                interpretation=interpretation,
                ai_prompt=system_prompt,
                ai_interpretation_audio_path=audio_path
            )
            
            if interpretation != "error" and generate_audio_flag:
                try:
                    actual_audio_path = generate_audio(interpretation, record_id)
                    if actual_audio_path:
                        audio_path = actual_audio_path
                        # update
                        from core.history import update_record_interpretation
                        import datetime
                        today = datetime.datetime.now().strftime("%Y-%m-%d")
                        update_record_interpretation(today, record_id, interpretation, audio_path)
                except Exception as e:
                    print(f"TTS Error: {e}")
        else:
            interpretation = "AI解牌已關閉"
            record_id = save_reading(
                record_type="xiaoliuren",
                question=request.question or "無問題",
                result=lesson,
                interpretation=interpretation,
                ai_prompt=system_prompt,
                ai_interpretation_audio_path=None
            )

        # Notify via Websocket
        if manager.active_client:
            push_data = {
                "type": "divination_result",
                "mode": "xiaoliuren",
                "question": request.question,
                "result": lesson,
                "interpretation": interpretation,
                "audio_path": audio_path,
                "record_id": record_id
            }
            asyncio.create_task(manager.send_to_client(push_data))

        return DivinationResponse(
            record_id=record_id,
            result=lesson,
            interpretation=interpretation,
            audio_path=audio_path
        )
            
    except Exception as e:
        print(f"XiaoLiuRen Endpoint Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
