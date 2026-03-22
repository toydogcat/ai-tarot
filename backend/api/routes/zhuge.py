from fastapi import APIRouter
from api.schemas import ZhugeDrawRequest, ZhugeResponse
from core.zhuge.engine import ZhugeEngine
from core.zhuge.interpreter import interpret_zhuge
from core.tts import generate_audio
from core.history import save_reading, update_record_interpretation
from core.config_manager import config_manager
from api.websocket_manager import manager
from datetime import datetime

router = APIRouter(prefix="/api/zhuge", tags=["ZhugeShensuan"])
engine = ZhugeEngine()

@router.post("/draw", response_model=ZhugeResponse)
def draw_zhuge(req: ZhugeDrawRequest):
    result = engine.draw_lot()
    
    interpretation_text = ""
    audio_file = ""
    
    if req.question:
        conf = config_manager.get()
        model_name = conf.ai_models.get("divination_model", "gemini-3.1-flash-lite-preview")
        interpretation_text = interpret_zhuge(req.question, result, language=req.language, selected_model=model_name)
        
        client_name = config_manager.get().app.get("guide_name", "toby")
        if manager.active_client:
            client_name = manager.active_client[1]

        record_id = save_reading(
            record_type="zhuge",
            question=req.question,
            result=result,
            interpretation=interpretation_text,
            client_name=client_name
        )

        if interpretation_text and "error" not in interpretation_text.lower() and not interpretation_text.startswith("⚠️"):
            # generate audio
            audio_file = generate_audio(interpretation_text, f"{record_id}_zhuge")
            if audio_file:
                update_record_interpretation(datetime.now().strftime("%Y-%m-%d"), record_id, interpretation_text, audio_file)
            
    return ZhugeResponse(
        id=result.get("id"),
        poem=result.get("poem"),
        explanation=result.get("explanation"),
        interpretation=interpretation_text if req.question else None,
        audio_path=audio_file if audio_file else None
    )
