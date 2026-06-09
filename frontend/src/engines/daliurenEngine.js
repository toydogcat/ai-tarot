import lessons from '../data/daliuren/lessons.json';

export function castDaliuren({ question, language }) {
  if (!lessons || lessons.length === 0) {
    throw new Error("Daliuren lessons data is not loaded.");
  }

  // Draw a random lesson
  const randomIndex = Math.floor(Math.random() * lessons.length);
  const lesson = lessons[randomIndex];

  // Generate local interpretation
  let interpretation = `🌊 【離線本機起課：大六壬式盤】 🌊\n`;
  if (question) {
    interpretation += `問卜內容：${question}\n`;
  }
  interpretation += `\n【起課時間】：${lesson.date} (${lesson.jieqi})\n`;
  interpretation += `【課式格局】：${lesson.pattern.join('、') || '無特殊格局'}\n\n`;
  
  interpretation += `【三傳（初、中、末）】：\n`;
  Object.entries(lesson.san_chuan).forEach(([k, v]) => {
    const dizhi = Array.isArray(v) && v.length > 0 ? v[0] : '';
    const tianjiang = Array.isArray(v) && v.length > 1 ? v[1] : '';
    interpretation += `• ${k}：${dizhi} (${tianjiang})\n`;
  });
  
  interpretation += `\n【四課（一、二、三、四）】：\n`;
  Object.entries(lesson.si_ke).forEach(([k, v]) => {
    const tian = (Array.isArray(v) && v.length > 0 && v[0] && v[0][0]) || '';
    const di = (Array.isArray(v) && v.length > 0 && v[0] && v[0][1]) || '';
    interpretation += `• ${k}：天盤 ${tian} / 地盤 ${di}\n`;
  });

  interpretation += `\n💡 *提示：本機離線模式不消耗 Token。如需 AI 深度解讀與語音解說，請切換至 API 連線模式。*`;

  return {
    date: lesson.date,
    jieqi: lesson.jieqi,
    pattern: lesson.pattern,
    san_chuan: lesson.san_chuan,
    si_ke: lesson.si_ke,
    interpretation: question ? interpretation : null,
    audio_path: null
  };
}
