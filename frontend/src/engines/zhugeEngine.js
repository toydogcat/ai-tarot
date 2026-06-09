import zhugeData from '../data/zhuge/zhuge_data.json';

export function drawZhuge({ question, language }) {
  if (!zhugeData || zhugeData.length === 0) {
    throw new Error("Zhuge lot data is not loaded.");
  }

  // Draw a random lot
  const randomIndex = Math.floor(Math.random() * zhugeData.length);
  const lot = zhugeData[randomIndex];

  let interpretation = `🎯 【離線本機占卜：諸葛神算】 🎯\n`;
  if (question) {
    interpretation += `問卜內容：${question}\n`;
  }
  interpretation += `\n【簽詩籤文】：\n${lot.poem}\n\n`;
  interpretation += `【簽詩解說】：\n${lot.interp1}\n\n`;
  if (lot.interp2) {
    interpretation += `【深層暗示】：\n${lot.interp2}\n\n`;
  }
  interpretation += `💡 *提示：本機離線模式不消耗 Token。如需 AI 深度解讀與語音解說，請切換至 API 連線模式。*`;

  return {
    id: String(lot.id),
    poem: lot.poem,
    explanation: lot.interp1 || "",
    interp1: lot.interp1 || "",
    interp2: lot.interp2 || "",
    interpretation: question ? interpretation : null,
    audio_path: null
  };
}
