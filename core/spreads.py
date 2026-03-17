"""牌陣定義"""
from core.models import SpreadPosition, SpreadType

# === 單牌占卜 ===
SINGLE_CARD = SpreadType(
    id="single",
    name="單牌占卜",
    description="抽出一張牌，獲得簡潔直接的指引。適合每日一牌或快速提問。",
    icon="🎴",
    positions=[
        SpreadPosition(0, "指引", "此刻宇宙給你的訊息"),
    ],
)

# === 三牌占卜 ===
THREE_CARD = SpreadType(
    id="three_card",
    name="三牌占卜",
    description="過去、現在、未來的時間之流，幫助你了解事情的脈絡與走向。",
    icon="🃏",
    positions=[
        SpreadPosition(0, "過去", "影響現況的過去因素"),
        SpreadPosition(1, "現在", "當前的狀態與能量"),
        SpreadPosition(2, "未來", "事情可能的發展方向"),
    ],
)

# === 時間之流（五牌） ===
TIME_FLOW = SpreadType(
    id="time_flow",
    name="時間之流",
    description="更詳細的時間線分析，從遠因到最終結果，全面了解事態發展。",
    icon="🌊",
    positions=[
        SpreadPosition(0, "遠因", "事件的根本原因"),
        SpreadPosition(1, "近因", "近期影響事態的因素"),
        SpreadPosition(2, "現在", "此刻的狀態"),
        SpreadPosition(3, "近期發展", "即將發生的變化"),
        SpreadPosition(4, "最終結果", "事情的最終走向"),
    ],
)

# === 二擇一牌陣 ===
TWO_OPTIONS = SpreadType(
    id="two_options",
    name="二擇一牌陣",
    description="當你面臨兩個選擇時，幫助你看清兩條路各自的發展與結果。",
    icon="⚖️",
    positions=[
        SpreadPosition(0, "現況", "你目前面對的狀態"),
        SpreadPosition(1, "選項 A 發展", "選擇 A 可能的發展"),
        SpreadPosition(2, "選項 A 結果", "選擇 A 的最終結果"),
        SpreadPosition(3, "選項 B 發展", "選擇 B 可能的發展"),
        SpreadPosition(4, "選項 B 結果", "選擇 B 的最終結果"),
    ],
)

# === 馬蹄形牌陣 ===
HORSESHOE = SpreadType(
    id="horseshoe",
    name="馬蹄形牌陣",
    description="七張牌的全面分析，從過去到未來，涵蓋你的態度、外在影響與最佳行動。",
    icon="🧲",
    positions=[
        SpreadPosition(0, "過去", "過去的影響"),
        SpreadPosition(1, "現在", "目前的狀況"),
        SpreadPosition(2, "未來", "未來的發展"),
        SpreadPosition(3, "你的態度", "你對事件的態度與心理狀態"),
        SpreadPosition(4, "外在影響", "周圍環境與他人的影響"),
        SpreadPosition(5, "建議", "你應該採取的行動"),
        SpreadPosition(6, "最終結果", "事情最可能的結果"),
    ],
)

# === 凱爾特十字 ===
CELTIC_CROSS = SpreadType(
    id="celtic_cross",
    name="凱爾特十字",
    description="最經典、最完整的塔羅牌陣。十張牌的深度占卜，全面解析你的處境。",
    icon="✝️",
    positions=[
        SpreadPosition(0, "現況", "你目前面對的核心議題"),
        SpreadPosition(1, "挑戰", "眼前最大的阻礙或挑戰"),
        SpreadPosition(2, "潛意識", "你內心深處的想法與感受"),
        SpreadPosition(3, "過去", "已經過去但仍有影響的事件"),
        SpreadPosition(4, "頂部（最佳結果）", "最好的可能結果"),
        SpreadPosition(5, "近期未來", "即將發生的事"),
        SpreadPosition(6, "你的態度", "你對此事的態度與看法"),
        SpreadPosition(7, "外在環境", "周遭環境與他人的影響"),
        SpreadPosition(8, "希望與恐懼", "你最深的希望或最大的恐懼"),
        SpreadPosition(9, "最終結果", "事情最可能的結局"),
    ],
)

# 所有牌陣列表
ALL_SPREADS: list[SpreadType] = [
    SINGLE_CARD,
    THREE_CARD,
    TIME_FLOW,
    TWO_OPTIONS,
    HORSESHOE,
    CELTIC_CROSS,
]


def get_spread_by_id(spread_id: str) -> SpreadType | None:
    """依 ID 取得牌陣"""
    for spread in ALL_SPREADS:
        if spread.id == spread_id:
            return spread
    return None
