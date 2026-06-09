const SMALL_SIX_LIST = [
  '大安', '留連', '速喜', '赤口', '小吉', '空亡'
];

const BIG_NINE_LIST = [
  '大安', '留連', '速喜', '赤口', '小吉', '空亡',
  '病符', '桃花', '天德'
];

const STATE_DETAILS = {
  "大安": {
    "attributes": "木 正東",
    "keywords": "長期，緩慢，穩定",
    "description": "求安穩，大安最吉。求變化，大安不吉。有靜止、心安、吉祥之含義。",
    "deity": "三清 / 青龍",
    "poem": "大安事事昌，求財於坤方。失物去不遠。宅舍保安康。行人身未動，病者主無妨，將軍四田野，仔細壬推詳。",
    "resolution": "身不動時，五行屬木，顏色青色，方位東方。臨青龍。謀事主一、五、七。屬吉卦，凡事都可以得到安康，但是此為靜卦，宜靜不動。目前運勢不錯，有穩定成長的情況，但不宜躁進。"
  },
  "留連": {
    "attributes": "水 (玄武) 北 / 原木 西南",
    "keywords": "停止，反覆，複雜",
    "description": "想挽留，留連是吉。其他都很噁心。有喑味不明，延遲。糾纏．拖延、漫長之含義。",
    "deity": "文昌 / 玄武",
    "poem": "連留事難成，求謀事未明。官事只宜緩，去者未回程。失物尋南方，急討方稱心。需防口舌災，人事且平平。",
    "resolution": "人未歸時，五行屬水，顏色黑色，方位北方，臨玄武。謀事主二、八、十。屬凶卦，代表凡事阻礙、遲滯，不宜有過大動作，事宜守。目前運勢低迷，心情不開朗，凡事受阻。"
  },
  "速喜": {
    "attributes": "火 正南",
    "keywords": "驚喜，快速，突然",
    "description": "意想不到的好事，指時機已到。有快速、喜慶，吉利之含義。",
    "deity": "雷祖 / 朱雀",
    "poem": "速喜喜來臨，求財向南行。失物申午未(南兼西南方)，逢人路上尋。官事有福德，病者無禍侵。田宅六畜吉，行人有音信。",
    "resolution": "人即至時，五行屬火，顏色紅色，方位南方，臨朱雀。謀事主三，六，九。屬吉卦，代表凡事皆有喜訊，而且很快就會到來。目前運勢漸開，要積極的行動就可以如願。"
  },
  "赤口": {
    "attributes": "金 正西",
    "keywords": "爭鬥，兇惡，傷害",
    "description": "吵架，打架，鬥爭，訴訟是非。有不吉、驚恐，兇險、口舌是非之含義。",
    "deity": "將帥 / 白虎",
    "poem": "赤口主口舌，是非切要防。失物速速尋，行人有驚慌。六畜多作怪，病者出西方。更須防咒嘴，恐怕染重病。",
    "resolution": "官事凶時，五行屬金，顏色白色，方位西方，臨白虎。謀事主防、七，十。屬凶卦，代表運勢多舛，而且諸多紛爭亦有口舌之禍。大計劃就要趕快實施不要拖延，小事則不成。"
  },
  "小吉": {
    "attributes": "木 (六合)",
    "keywords": "起步，不多，尚可",
    "description": "成中有缺，適合起步。有和合、吉利之含義。",
    "deity": "真武 / 六合",
    "poem": "小吉最吉昌，路上好商量。陰人來報喜，失物在坤方。行人即便至，交關更是強。凡事皆合和，病者叩穹蒼。",
    "resolution": "人來喜時，五行屬木，臨六合。謀事主一、五、七。屬吉卦，代表凡事皆吉，不如大安的安穩也不如速喜快，介於兩者中間。保持目前狀況就會越來越好。"
  },
  "空亡": {
    "attributes": "土 中央 (或內)",
    "keywords": "失去，虛偽，空想",
    "description": "先得再失，尤忌金錢事。現實(空亡差)，虛幻(空亡好)。有不吉、無結果、憂慮之含義。",
    "deity": "玉帝 / 勾陳",
    "poem": "空亡事不祥，陰人多作怪。求財無利益，行人有災殃.失物尋不見，官事有刑傷。病人逢暗鬼，禳解保平安。",
    "resolution": "音信稀時，五行屬土，顏色黃色，方位中央；臨勾陳。謀事主三、六、九。為凶卦，代表凡事穢暗不明，內心不安，運途起伏。自身拿不定主意，無所適從，切莫隨意做判斷。"
  },
  "病符": {
    "attributes": "金 西南",
    "keywords": "病態，異常，治療",
    "description": "先有病，才需要治療。",
    "deity": "后土",
    "poem": "病符星君臨，身心遇不平。須防隱疾發，療養保安寧。",
    "resolution": "代表進入病態或停滯修復期，需要針對異常做處置。"
  },
  "桃花": {
    "attributes": "土 東北",
    "keywords": "欲望，牽絆，異性",
    "description": "人際關係，牽絆此事。",
    "deity": "城隍",
    "poem": "桃花多牽絆，人際結情網。欲望若不節，迷失在路旁。",
    "resolution": "代表情感與人際關係的牽連，吉凶參半，多指欲望與糾葛。"
  },
  "天德": {
    "attributes": "金 西北",
    "keywords": "貴人，上司，高遠",
    "description": "求人辦事，靠人成事。",
    "deity": "紫薇",
    "poem": "天德降祥光，謀事遇貴郎。逢凶能化吉，高步上雲堂。",
    "resolution": "大吉之兆，有上位者、貴人鼎力相助，化險為夷。"
  }
};

export function drawXiaoliuren({ question }) {
  const num1 = Math.floor(Math.random() * 12) + 1;
  const num2 = Math.floor(Math.random() * 12) + 1;
  const num3 = Math.floor(Math.random() * 12) + 1;

  // 6-state Xiao Liu Ren calculation
  const idx1_6 = (num1 - 1) % 6;
  const idx2_6 = (num1 + num2 - 1) % 6;
  const idx3_6 = (num1 + num2 + num3 - 1) % 6;

  // 9-state variant calculation
  const idx1_9 = (num1 - 1) % 9;
  const idx2_9 = (num1 + num2 - 1) % 9;
  const idx3_9 = (num1 + num2 + num3 - 1) % 9;

  const smallStates = [SMALL_SIX_LIST[idx1_6], SMALL_SIX_LIST[idx2_6], SMALL_SIX_LIST[idx3_6]];
  const bigStates = [BIG_NINE_LIST[idx1_9], BIG_NINE_LIST[idx2_9], BIG_NINE_LIST[idx3_9]];

  const finalState = smallStates[2];
  const finalDetails = STATE_DETAILS[finalState];

  const lesson = {
    numbers: [num1, num2, num3],
    small_six_states: smallStates,
    big_nine_states: bigStates,
    final_state: finalState,
    details: finalDetails
  };

  // Generate local interpretation
  let interpretation = `🍂 【離線本機起課：小六壬】 🍂\n`;
  if (question) {
    interpretation += `問卜內容：${question}\n`;
  }
  interpretation += `\n【起課數據】：${num1}、${num2}、${num3}\n`;
  interpretation += `【小六壬三傳】：${smallStates.join(' ➡️ ')}\n`;
  interpretation += `【大六壬變體】：${bigStates.join(' ➡️ ')}\n\n`;
  interpretation += `【終局落宮：${finalState}】\n`;
  interpretation += `• 象意：${finalDetails.description}\n`;
  interpretation += `• 卦意詩：${finalDetails.poem}\n`;
  interpretation += `• 決斷：${finalDetails.resolution}\n\n`;
  interpretation += `💡 *提示：本機離線模式不消耗 Token。如需 AI 深度解讀與語音解說，請切換至 API 連線模式。*`;

  return {
    numbers: [num1, num2, num3],
    small_six_states: smallStates,
    big_nine_states: bigStates,
    final_state: finalState,
    details: finalDetails,
    interpretation: question ? interpretation : null,
    audio_path: null
  };
}
