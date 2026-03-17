"""抽牌引擎 — 隨機抽牌與正逆位"""
import random

from config import REVERSE_PROBABILITY
from core.deck import TarotDeck
from core.models import Card, DrawnCard, SpreadResult, SpreadType


class DrawEngine:
    """抽牌引擎"""

    def __init__(self, deck: TarotDeck | None = None):
        self.deck = deck or TarotDeck()

    def draw(self, count: int = 1, allow_reversed: bool = True) -> list[DrawnCard]:
        """
        隨機抽取指定數量的牌
        Args:
            count: 抽幾張
            allow_reversed: 是否允許逆位
        Returns:
            抽出的牌列表
        """
        all_cards = self.deck.get_all_cards()
        selected: list[Card] = random.sample(all_cards, min(count, len(all_cards)))

        drawn_cards = []
        for card in selected:
            is_reversed = allow_reversed and (random.random() < REVERSE_PROBABILITY)
            drawn_cards.append(DrawnCard(card=card, is_reversed=is_reversed))

        return drawn_cards

    def draw_spread(
        self, spread: SpreadType, allow_reversed: bool = True
    ) -> SpreadResult:
        """
        根據牌陣抽牌
        Args:
            spread: 牌陣定義
            allow_reversed: 是否允許逆位
        Returns:
            SpreadResult 抽牌結果
        """
        drawn_cards = self.draw(spread.card_count, allow_reversed)
        return SpreadResult(spread=spread, drawn_cards=drawn_cards)
