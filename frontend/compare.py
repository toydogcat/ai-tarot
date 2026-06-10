import subprocess
import json
import random
from kinliuren.kinliuren import Liuren

# Constants
tiangan = list("甲乙丙丁戊己庚辛壬癸")
dizhi = list("子丑寅卯辰巳午未申酉戌亥")
jieqis = '立春 雨水 驚蟄 春分 清明 穀雨 立夏 小滿 芒種 夏至 小暑 大暑 立秋 處暑 白露 秋分 寒露 霜降 立冬 小雪 大雪 冬至 小寒 大寒'.split()
months = '正 二 三 四 五 六 七 八 九 十 十一 十二'.split()

# 60 Jiazi list
jiazi = [tiangan[i % 10] + dizhi[i % 12] for i in range(60)]

# Day Gan to Hour Gan mapping helper (五鼠遁)
def get_hour_jiazi(day_gan, hour_zhi):
    # 甲己還加甲，乙庚丙作初，丙辛從戊起，丁壬庚子居，戊癸何方發，壬子是真途。
    # Maps day_gan to the starting Gan of '子' hour
    start_gan_idx = {
        '甲': 0, '己': 0,
        '乙': 2, '庚': 2,
        '丙': 4, '辛': 4,
        '丁': 6, '壬': 6,
        '戊': 8, '癸': 8
    }[day_gan]
    
    zhi_idx = dizhi.index(hour_zhi)
    gan_idx = (start_gan_idx + zhi_idx) % 10
    return tiangan[gan_idx] + hour_zhi

def run_js(jieqi, cmonth, day_gz, hour_gz):
    try:
        res = subprocess.run(
            ["node", "frontend/test_daliuren.js", jieqi, cmonth, day_gz, hour_gz],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(res.stdout)
    except Exception as e:
        return {"error": str(e)}

def run_py(jieqi, cmonth, day_gz, hour_gz):
    try:
        lr = Liuren(jieqi, cmonth, day_gz, hour_gz)
        return lr.result(0)
    except Exception as e:
        return {"error": str(e)}

def clean_dict(d):
    # Standardize format for comparison
    return json.loads(json.dumps(d, ensure_ascii=False))

def compare_results():
    random.seed(42)  # Seed for reproducibility
    mismatches = []
    
    # Generate 500 test cases
    test_cases = []
    for _ in range(500):
        jieqi = random.choice(jieqis)
        cmonth = random.choice(months)
        day_gz = random.choice(jiazi)
        hour_zhi = random.choice(dizhi)
        hour_gz = get_hour_jiazi(day_gz[0], hour_zhi)
        test_cases.append((jieqi, cmonth, day_gz, hour_gz))
        
    print(f"Running comparison on {len(test_cases)} test cases...")
    
    checked = 0
    passed = 0
    
    for case in test_cases:
        jieqi, cmonth, day_gz, hour_gz = case
        py_res = run_py(jieqi, cmonth, day_gz, hour_gz)
        js_res = run_js(jieqi, cmonth, day_gz, hour_gz)
        
        checked += 1
        if "error" in js_res or "error" in py_res:
            mismatches.append({
                "case": case,
                "py": py_res,
                "js": js_res,
                "type": "error"
            })
            continue
            
        # Compare key fields
        fields_to_compare = ["格局", "三傳", "四課", "天地盤"]
        diff = {}
        for field in fields_to_compare:
            py_val = py_res.get(field)
            js_val = js_res.get(field)
            
            # For 三傳, compare without the last element if it's the hidden branch/gan reference
            if field == "三傳":
                # Py format: "初傳": ["子", "虎", "子", "戊"]
                # Sometimes the third/fourth elements might differ due to minor bugs, but let's check exact match first.
                pass
                
            if py_val != js_val:
                diff[field] = {"py": py_val, "js": js_val}
                
        if diff:
            mismatches.append({
                "case": case,
                "diff": diff
            })
        else:
            passed += 1
            
    print(f"Passed: {passed}/{checked}")
    if mismatches:
        print(f"Found {len(mismatches)} mismatches.")
        # Print first 5 mismatches in detail
        for m in mismatches[:5]:
            print(f"Case: {m['case']}")
            if "diff" in m:
                for f, vals in m["diff"].items():
                    print(f"  Field: {f}")
                    print(f"    Py: {vals['py']}")
                    print(f"    Js: {vals['js']}")
            else:
                print(f"  Py Error: {m.get('py')}")
                print(f"  Js Error: {m.get('js')}")
    else:
        print("All test cases matched perfectly!")

if __name__ == "__main__":
    compare_results()
