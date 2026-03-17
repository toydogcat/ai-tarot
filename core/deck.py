"""牌組管理 — 載入 JSON 資料、建立完整 78 張牌組"""
import json
from pathlib import Path

from config import MAJOR_ARCANA_FILE, MINOR_ARCANA_FILE
from core.models import Card, CardMeaning


class TarotDeck:
    """塔羅牌組"""

    def __init__(self):
        self._cards: list[Card] = []
        self._load_cards()

    def _parse_card(self, data: dict) -> Card:
        """將 JSON dict 轉換為 Card 物件"""
        return Card(
            id=data["id"],
            number=data["number"],
            name=data["name"],
            name_zh=data["name_zh"],
            image=data["image"],
            upright=CardMeaning(**data["upright"]),
            reversed=CardMeaning(**data["reversed"]),
            suit=data.get("suit"),
            suit_zh=data.get("suit_zh"),
            rank=data.get("rank"),
        )

    def _load_cards(self):
        """從 JSON 檔載入所有牌"""
        # 載入大阿爾克那
        with open(MAJOR_ARCANA_FILE, "r", encoding="utf-8") as f:
            major_data = json.load(f)
        for card_data in major_data:
            self._cards.append(self._parse_card(card_data))

        # 載入小阿爾克那
        with open(MINOR_ARCANA_FILE, "r", encoding="utf-8") as f:
            minor_data = json.load(f)
        for card_data in minor_data:
            self._cards.append(self._parse_card(card_data))

    def get_all_cards(self) -> list[Card]:
        """取得所有牌"""
        return self._cards.copy()

    def get_major_arcana(self) -> list[Card]:
        """取得大阿爾克那"""
        return [c for c in self._cards if c.is_major]

    def get_minor_arcana(self) -> list[Card]:
        """取得小阿爾克那"""
        return [c for c in self._cards if not c.is_major]

    def get_card_by_id(self, card_id: str) -> Card | None:
        """依 ID 取得特定牌"""
        for card in self._cards:
            if card.id == card_id:
                return card
        return None

    @property
    def total_count(self) -> int:
        return len(self._cards)
