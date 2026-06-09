import majorArcana from '../data/tarot/major_arcana.json';
import minorArcana from '../data/tarot/minor_arcana.json';

const SPREADS = {
  single: {
    name: "單牌占卜",
    positions: ["指引"]
  },
  three_card: {
    name: "三牌占卜",
    positions: ["過去", "現在", "未來"]
  },
  time_flow: {
    name: "時間之流",
    positions: ["遠因", "近因", "現在", "近期發展", "最終結果"]
  },
  two_options: {
    name: "二擇一牌陣",
    positions: ["現況", "選項 A 發展", "選項 A 結果", "選項 B 發展", "選項 B 結果"]
  },
  horseshoe: {
    name: "馬蹄形牌陣",
    positions: ["過去", "現在", "未來", "你的態度", "外在影響", "建議", "最終結果"]
  },
  celtic_cross: {
    name: "凱爾特十字",
    positions: ["現況", "挑戰", "潛意識", "過去", "頂部（最佳結果）", "近期未來", "你的態度", "外在環境", "希望與恐懼", "最終結果"]
  }
};

export function getSpreads() {
  return Object.entries(SPREADS).map(([id, info]) => ({
    id,
    name: info.name,
    description: `抽 ${info.positions.length} 張牌的本地牌陣。`,
    icon: id === 'single' ? '🎴' : '🃏',
    card_count: info.positions.length
  }));
}

export function drawTarot({ spread_id, question, language }) {
  const spread = SPREADS[spread_id] || SPREADS.single;
  const cardCount = spread.positions.length;

  // Combine full deck
  const fullDeck = [...majorArcana, ...minorArcana];
  
  // Randomly select N unique cards
  const selectedCards = [];
  const deckCopy = [...fullDeck];
  
  for (let i = 0; i < cardCount; i++) {
    if (deckCopy.length === 0) break;
    const randomIndex = Math.floor(Math.random() * deckCopy.length);
    selectedCards.push(deckCopy.splice(randomIndex, 1)[0]);
  }

  const cardsResult = selectedCards.map((card, i) => {
    const isReversed = Math.random() < 0.5;
    const details = isReversed ? card.reversed : card.upright;
    
    // Support either image format
    let imgFile = card.image;
    if (imgFile.endsWith('.png')) {
      imgFile = imgFile.replace('.png', '.jpg');
    }

    return {
      name: card.name,
      name_zh: card.name_zh,
      is_reversed: isReversed,
      meaning: details.meaning,
      keywords: details.keywords,
      position_name: spread.positions[i] || `位置 ${i + 1}`,
      image_path: `/assets/images/tarot/${imgFile}`
    };
  });

  // Local static interpretation template
  let interpretation = `🔮 【離線本機牌陣：${spread.name}】 🔮\n`;
  if (question) {
    interpretation += `問卜內容：${question}\n`;
  }
  interpretation += `\n以下是為您抽出的牌組與解析：\n\n`;

  cardsResult.forEach((c) => {
    interpretation += `📍 **${c.position_name}** —【${c.name_zh}】(${c.is_reversed ? '逆位' : '正位'})\n`;
    interpretation += `• 關鍵字：${c.keywords.join('、')}\n`;
    interpretation += `• 牌義解說：${c.meaning}\n\n`;
  });

  interpretation += `💡 *提示：本機離線模式不消耗 Token。如需 AI 深度解讀與語音解說，請切換至 API 連線模式。*`;

  return {
    spread_name: spread.name,
    cards: cardsResult,
    interpretation: question ? interpretation : null,
    audio_path: null
  };
}
