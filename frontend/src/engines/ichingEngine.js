import hexagramsData from '../data/iching/64_hexagrams.json';

const TRIGRAM_MAP = {
  '1,1,1': '乾',
  '0,0,0': '坤',
  '1,0,0': '震',
  '0,1,0': '坎',
  '0,0,1': '艮',
  '0,1,1': '巽',
  '1,0,1': '離',
  '1,1,0': '兌'
};

function getTrigramName(binarySlice) {
  const key = binarySlice.join(',');
  return TRIGRAM_MAP[key] || '未知';
}

function findHexagram(trigrams) {
  return hexagramsData.find(h => 
    h.trigrams.upper === trigrams.upper && 
    h.trigrams.lower === trigrams.lower
  ) || null;
}

export function castIChing({ question, language }) {
  // 1. Simulate 6 tosses (each toss is 3 coins, each coin value is 2 [Yin] or 3 [Yang])
  const tosses = [];
  const linesInfo = [];

  for (let i = 0; i < 6; i++) {
    const coins = [
      Math.random() < 0.5 ? 2 : 3,
      Math.random() < 0.5 ? 2 : 3,
      Math.random() < 0.5 ? 2 : 3
    ];
    const sum = coins.reduce((a, b) => a + b, 0);
    tosses.push(sum);

    if (sum === 6) {
      linesInfo.push({ original: 0, changed: 1, moving: true, value: 6, symbol: 'x' });
    } else if (sum === 7) {
      linesInfo.push({ original: 1, changed: 1, moving: false, value: 7, symbol: '—' });
    } else if (sum === 8) {
      linesInfo.push({ original: 0, changed: 0, moving: false, value: 8, symbol: '--' });
    } else if (sum === 9) {
      linesInfo.push({ original: 1, changed: 0, moving: true, value: 9, symbol: 'o' });
    }
  }

  const originalBinary = linesInfo.map(l => l.original);
  const changedBinary = linesInfo.map(l => l.changed);

  const originalTrigrams = {
    lower: getTrigramName(originalBinary.slice(0, 3)),
    upper: getTrigramName(originalBinary.slice(3, 6))
  };

  const changedTrigrams = {
    lower: getTrigramName(changedBinary.slice(0, 3)),
    upper: getTrigramName(changedBinary.slice(3, 6))
  };

  const originalHexagram = findHexagram(originalTrigrams);
  const changedHexagram = findHexagram(changedTrigrams);
  const hasMovingLines = linesInfo.some(l => l.moving);

  // Generate local interpretation
  let interpretation = `☯️ 【離線本機卜卦：周易八卦】 ☯️\n`;
  if (question) {
    interpretation += `問卜內容：${question}\n`;
  }
  interpretation += `\n【起卦結果】：\n`;
  interpretation += `• 本卦：第 ${originalHexagram.id} 卦 — ${originalHexagram.name} (${originalHexagram.description})\n`;
  
  if (hasMovingLines && changedHexagram && changedHexagram.id !== originalHexagram.id) {
    interpretation += `• 變卦：第 ${changedHexagram.id} 卦 — ${changedHexagram.name} (${changedHexagram.description})\n`;
  } else {
    interpretation += `• 變卦：無變爻，以本卦卦辭解析。\n`;
  }

  interpretation += `\n【卦辭指引】：\n`;
  originalHexagram.lines.forEach((lineText, idx) => {
    const isMoving = linesInfo[idx].moving;
    interpretation += `${idx + 1}爻：${lineText}${isMoving ? ' 🌟 (動爻)' : ''}\n`;
  });

  interpretation += `\n💡 *提示：本機離線模式不消耗 Token。如需 AI 深度解讀與語音解說，請切換至 API 連線模式。*`;

  return {
    hexagram_id: originalHexagram.id,
    hexagram_name: originalHexagram.name,
    hexagram_description: originalHexagram.description,
    lines: originalHexagram.lines,
    lines_binary: originalBinary,
    moving_indices: linesInfo.map((l, idx) => l.moving ? idx : -1).filter(idx => idx !== -1),
    upper_trigram: originalHexagram.trigrams.upper,
    lower_trigram: originalHexagram.trigrams.lower,
    changed_hexagram_id: (hasMovingLines && changedHexagram) ? changedHexagram.id : null,
    changed_hexagram_name: (hasMovingLines && changedHexagram) ? changedHexagram.name : null,
    interpretation: question ? interpretation : null,
    audio_path: null
  };
}
