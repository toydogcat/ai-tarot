import random
from kinliuren.kinliuren import Liuren

class DaliurenEngine:
    def __init__(self):
        self.jieqis = ['立春', '雨水', '驚蟄', '春分', '清明', '穀雨', '立夏', '小滿', '芒種', '夏至', '小暑', '大暑', '立秋', '處暑', '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至', '小寒', '大寒']
        self.cmonths = ['正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']
        self.tiangans = list("甲乙丙丁戊己庚辛壬癸")
        self.dizhis = list("子丑寅卯辰巳午未申酉戌亥")
        self.jiazis = [self.tiangans[i % 10] + self.dizhis[i % 12] for i in range(60)]

    def draw_lesson(self):
        max_retries = 5
        for _ in range(max_retries):
            try:
                jq = random.choice(self.jieqis)
                cm = random.choice(self.cmonths)
                day_gz = random.choice(self.jiazis)
                hour_gz = random.choice(self.jiazis)
                
                lr = Liuren(jq, cm, day_gz, hour_gz)
                result = lr.result(0)  # 0 indicates daytime guiren rule parsing
                
                # Make it serializable and a string representation for LLM to digest easily
                # result is a dictionary containing 節氣, 日期, 格局, 三傳, 四課, etc.
                if isinstance(result, dict):
                    formatted = {
                        "jieqi": result.get("節氣") or jq,
                        "date": result.get("日期") or f"{day_gz}日{hour_gz}時",
                        "pattern": result.get("格局") or [],
                        "san_chuan": result.get("三傳") or {},
                        "si_ke": result.get("四課") or {}
                    }
                    return formatted
            except Exception as e:
                print(f"Daliuren generation error: {e}")
                continue
        
        # Fallback if generation completely fails
        return {
            "jieqi": "不明",
            "date": "未定",
            "pattern": "隨機起課失敗",
            "san_chuan": "無傳",
            "si_ke": "無課"
        }
