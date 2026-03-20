"""塔羅牌資料模型"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CardMeaning:
    """牌意資料"""
    keywords: list[str]
    meaning: str


@dataclass
class Card:
    """塔羅牌"""
    id: str
    number: int
    name: str
    name_zh: str
    image: str
    upright: CardMeaning
    reversed: CardMeaning
    # 小阿爾克那專用欄位
    suit: Optional[str] = None
    suit_zh: Optional[str] = None
    rank: Optional[str] = None

    @property
    def is_major(self) -> bool:
        return self.id.startswith("major")


@dataclass
class DrawnCard:
    """抽出的牌（含正逆位資訊）"""
    card: Card
    is_reversed: bool

    @property
    def display_name(self) -> str:
        orientation = "逆位" if self.is_reversed else "正位"
        return f"{self.card.name_zh}（{orientation}）"

    @property
    def current_meaning(self) -> CardMeaning:
        return self.card.reversed if self.is_reversed else self.card.upright


@dataclass
class SpreadPosition:
    """牌陣中的位置定義"""
    index: int
    name: str
    description: str


@dataclass
class SpreadType:
    """牌陣定義"""
    id: str
    name: str
    description: str
    positions: list[SpreadPosition]
    icon: str = "🃏"

    @property
    def card_count(self) -> int:
        return len(self.positions)


@dataclass
class SpreadResult:
    """抽牌結果"""
    spread: SpreadType
    drawn_cards: list[DrawnCard] = field(default_factory=list)
