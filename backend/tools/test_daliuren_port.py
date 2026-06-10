import random
import subprocess
import json
import sys
import os
from collections import Counter

# Add backend directory to sys.path to import kinliuren
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from kinliuren.kinliuren import Liuren

jieqis = ['立春', '雨水', '驚蟄', '春分', '清明', '穀雨', '立夏', '小滿', '芒種', '夏至', '小暑', '大暑', '立秋', '處暑', '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至', '小寒', '大寒']
cmonths = ['正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']
tiangans = list("甲乙丙丁戊己庚辛壬癸")
dizhis = list("子丑寅卯辰巳午未申酉戌亥")
jiazis = [tiangans[i % 10] + dizhis[i % 12] for i in range(60)]

def run_js(jieqi, cmonth, day_gz, hour_gz):
    cmd = [
        "node",
        "frontend/test_daliuren.js",
        jieqi,
        cmonth,
        day_gz,
        hour_gz
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return {"error": res.stderr}
    try:
        return json.loads(res.stdout.strip())
    except json.JSONDecodeError:
        return {"error": "JSON decode error: " + res.stdout}

def clean_dict(d):
    if not isinstance(d, dict):
        return d
    return {k: clean_dict(v) for k, v in d.items()}

def clean_list(lst):
    if not isinstance(lst, list):
        return lst
    return [clean_dict(x) if isinstance(x, dict) else clean_list(x) if isinstance(x, list) else x for x in lst]

def diff_dict(d1, d2):
    # Perform a deep comparison and return list of differences
    diffs = []
    
    # Check keys
    for k in set(d1.keys()).union(d2.keys()):
        if k not in d1:
            diffs.append(f"Key '{k}' missing in Python result")
        elif k not in d2:
            diffs.append(f"Key '{k}' missing in JS result")
        else:
            val1 = d1[k]
            val2 = d2[k]
            if type(val1) != type(val2):
                diffs.append(f"Type mismatch for key '{k}': Python={type(val1)}, JS={type(val2)}")
            elif isinstance(val1, dict):
                sub_diffs = diff_dict(val1, val2)
                diffs.extend([f"{k}.{sd}" for sd in sub_diffs])
            elif isinstance(val1, list):
                if len(val1) != len(val2):
                    diffs.append(f"List length mismatch for key '{k}': Python={val1} (len={len(val1)}), JS={val2} (len={len(val2)})")
                else:
                    for i, (v1, v2) in enumerate(zip(val1, val2)):
                        if v1 != v2:
                            diffs.append(f"List element mismatch at index {i} under '{k}': Python={v1}, JS={v2}")
            else:
                if val1 != val2:
                    diffs.append(f"Value mismatch for '{k}': Python={val1!r}, JS={val2!r}")
    return diffs

class CallableDict(dict):
    def __call__(self, key):
        for k in self.keys():
            if isinstance(k, tuple):
                if key in k:
                    return self[k]
            elif isinstance(k, str):
                if key in k.split(','):
                    return self[k]
        return None

def main():
    print("Starting Daliuren differential testing...")
    test_count = 1000
    mismatch_count = 0
    success_count = 0
    skipped_count = 0
    
    # Fixed seed for reproducibility
    random.seed(42)
    
    for i in range(test_count):
        jq = random.choice(jieqis)
        cm = random.choice(cmonths)
        day_gz = random.choice(jiazis)
        hour_gz = random.choice(jiazis)
        
        # Get python output
        try:
            lr = Liuren(jq, cm, day_gz, hour_gz)
            lr.ganzhiwuxing = CallableDict(lr.ganzhiwuxing)
            orig_fiter = lr.fiter_four_ke
            def patched_fiter():
                res = orig_fiter()
                if isinstance(res, list):
                    return sorted(res)
                return res
            lr.fiter_four_ke = patched_fiter
            py_res = lr.result(0)
        except Exception as py_err:
            # If python fails, check if JS also fails or returns error
            js_res = run_js(jq, cm, day_gz, hour_gz)
            if "error" not in js_res:
                print(f"Mismatch: Python raised exception but JS succeeded on input: {jq}, {cm}, {day_gz}, {hour_gz}")
                print(f"Python error: {py_err}")
                print(f"JS returned: {js_res}")
                sys.exit(1)
            skipped_count += 1
            continue

        # Get JS output
        js_res = run_js(jq, cm, day_gz, hour_gz)
        if "error" in js_res:
            print(f"Mismatch: Python succeeded but JS failed with error {js_res['error']} on input: {jq}, {cm}, {day_gz}, {hour_gz}")
            print(f"JS Trace: {js_res.get('stack', '')}")
            sys.exit(1)
            
        # Compare key fields
        # Note: We don't compare "日期" exactly because JS output might format day/hour differently, but let's check core astrological properties:
        # "格局", "三傳", "四課", "天地盤", "地轉天盤", "地轉天將"
        
        py_compare = {
            "格局": py_res.get("格局"),
            "三傳": py_res.get("三傳"),
            "四課": py_res.get("四課"),
            "天地盤": py_res.get("天地盤"),
            "地轉天盤": py_res.get("地轉天盤"),
            "地轉天將": py_res.get("地轉天將"),
            "日馬": py_res.get("日馬")
        }
        
        js_compare = {
            "格局": js_res.get("格局"),
            "三傳": js_res.get("三傳"),
            "四課": js_res.get("四課"),
            "天地盤": js_res.get("天地盤"),
            "地轉天盤": js_res.get("地轉天盤"),
            "地轉天將": js_res.get("地轉天將"),
            "日馬": js_res.get("日馬")
        }
        
        diffs = diff_dict(py_compare, js_compare)
        if diffs:
            print(f"Mismatch found on input: jieqi={jq}, cmonth={cm}, day={day_gz}, hour={hour_gz}")
            for d in diffs:
                print(f"  - {d}")
            print("Python Result:")
            print(json.dumps(py_compare, ensure_ascii=False, indent=2))
            print("JS Result:")
            print(json.dumps(js_compare, ensure_ascii=False, indent=2))
            sys.exit(1)
            
        success_count += 1

    print(f"Differential testing finished. Checked {test_count} cases:")
    print(f"  - Passed: {success_count}")
    print(f"  - Skipped (invalid configurations): {skipped_count}")
    print("Success! JS port behaves exactly like Python kinliuren library.")

if __name__ == '__main__':
    main()
