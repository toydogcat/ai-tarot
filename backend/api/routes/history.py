from fastapi import APIRouter
from typing import List
from api.schemas import HistoryRecordResponse
from core.history import get_history_dates, load_history
from core.tarot.deck import TarotDeck

router = APIRouter(prefix="/api/history", tags=["History"])

# Initialize deck once in memory for history route
deck = TarotDeck()

@router.get("", response_model=List[HistoryRecordResponse])
def get_all_history(limit: int = 50):
    """取得最新的歷史紀錄"""
    dates = get_history_dates()
    all_records = []
    
    for d in dates:
        records = load_history(d)
        
        # Inject missing image paths for older tarot records
        for r in records:
            if r.get("type", "tarot") == "tarot":
                cards = []
                if "result" in r and "cards" in r["result"]:
                    cards = r["result"]["cards"]
                elif "cards" in r:
                    cards = r["cards"]
                    
                for c in cards:
                    if "image_path" not in c and "card_id" in c:
                        try:
                            card_obj = deck.get_card_by_id(c["card_id"])
                            if card_obj:
                                c["image_path"] = f"/assets/images/tarot/{card_obj.image}"
                        except Exception:
                            pass
                    elif "image_path" in c and c["image_path"].startswith("/assets/tarot/"):
                        c["image_path"] = c["image_path"].replace("/assets/tarot/", "/assets/images/tarot/")
            elif r.get("type") == "iching":
                from core.iching.engine import load_hexagrams_data
                try:
                    hex_data = load_hexagrams_data()
                    name2id = {h["name"]: h["id"] for h in hex_data}
                    res = r.get("result", {})
                    orig_name = res.get("original_hexagram")
                    changed_name = res.get("changed_hexagram")
                    if orig_name and orig_name in name2id:
                        res["original_image_path"] = f"/assets/images/iching/hexagrams/{name2id[orig_name]}.png"
                    if changed_name and changed_name in name2id:
                        res["changed_image_path"] = f"/assets/images/iching/hexagrams/{name2id[changed_name]}.png"
                except Exception:
                    pass

        # Reverse to get newest first in that day
        all_records.extend(reversed(records))
        if len(all_records) >= limit:
            break
            
    return all_records[:limit]
