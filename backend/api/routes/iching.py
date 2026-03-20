from fastapi import APIRouter
from api.schemas import IChingCastRequest, IChingResponse
from core.iching.engine import perform_divination
from core.iching.interpreter import get_ai_interpretation
from core.tts import generate_audio
from core.history import save_reading, update_record_interpretation
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/iching", tags=["IChing"])

@router.post("/cast", response_model=IChingResponse)
def cast_iching(req: IChingCastRequest):
    result = perform_divination()
    
    lines_info = result["lines_info"]
    moving_indices = [i for i, line in enumerate(lines_info) if line["moving"]]
    hex_data = result["original_hexagram"]
    
    interpretation_text = ""
    audio_file = ""
    
    if req.question:
        interpretation_text = get_ai_interpretation(req.question, result, language=req.language)
        
        record_id = save_reading(
            record_type="iching",
            question=req.question,
            result=result,
            interpretation=interpretation_text,
            ai_prompt="",
            search_success=False
        )

        if interpretation_text and "error" not in interpretation_text.lower() and not interpretation_text.startswith("⚠️"):
            # generate audio
            audio_file = generate_audio(interpretation_text, f"{record_id}_iching")
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
