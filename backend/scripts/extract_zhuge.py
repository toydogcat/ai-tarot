import json
import re
import os

def main():
    ipynb_path = os.path.join(os.path.dirname(__file__), '../../TMP/孔明神數三百八十四籤.ipynb')
    output_path = os.path.join(os.path.dirname(__file__), '../data/zhuge/zhuge_data.json')
    
    with open(ipynb_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    code_cells = [c for c in data.get("cells", []) if c["cell_type"] == "code"]
    markdown_cells = [c for c in data.get("cells", []) if c["cell_type"] == "markdown"]
    
    source_code = ""
    for cell in code_cells:
        source_code += "".join(cell.get("source", []))

    lines = source_code.split('\n')
    
    results = []

    # Parse Code cells
    current_num = None
    poem = None
    interp1 = None
    interp2 = None
    
    for line in lines:
        m_num = re.search(r'(?:if|elif)\s+(?:num_384|num\s*%\s*384|num\s*%\s*\d+)\s*==\s*(\d+):', line)
        if m_num:
            if current_num is not None:
                results.append({
                    "id": current_num,
                    "poem": poem or "",
                    "interp1": interp1 or "",
                    "interp2": interp2 or ""
                })
            current_num = int(m_num.group(1))
            poem = None
            interp1 = None
            interp2 = None
            continue
            
        m_print = re.search(r'console\.print\(\s*"([^"]*)"\s*,', line)
        if m_print and current_num is not None:
            text = m_print.group(1)
            if text.startswith("解籤一："):
                interp1 = text.replace("解籤一：", "").strip()
            elif text.startswith("解籤二："):
                interp2 = text.replace("解籤二：", "").strip()
            elif text.startswith("解籤二:"):
                interp2 = text.replace("解籤二:", "").strip()
            elif text.startswith("籤詩：") or text.startswith("籤 詩："):
                poem = text.replace("籤詩：", "").replace("籤 詩：", "").strip()
                
    if current_num is not None:
        results.append({
            "id": current_num,
            "poem": poem or "",
            "interp1": interp1 or "",
            "interp2": interp2 or ""
        })

    # Parse Markdown cells
    md_lines = []
    for cell in markdown_cells:
        md_lines.extend(cell.get("source", []))

    current_md = None
    md_poem = ""
    md_i1 = ""
    md_i2 = ""

    for line in md_lines:
        line = line.strip()
        m_head = re.match(r'^第\s*(\d+)\s*籤', line)
        if m_head:
            if current_md is not None:
                results.append({
                    "id": current_md,
                    "poem": md_poem,
                    "interp1": md_i1,
                    "interp2": md_i2
                })
            current_md = int(m_head.group(1))
            md_poem = ""
            md_i1 = ""
            md_i2 = ""
            continue
            
        if current_md is not None:
            if line.startswith("籤 詩：") or line.startswith("籤詩："):
                md_poem = line.split("：", 1)[1].strip()
            elif line.startswith("解籤一："):
                md_i1 = line.split("：", 1)[1].strip()
            elif line.startswith("解籤二："):
                md_i2 = line.split("：", 1)[1].strip()
            elif "略解" in line and "籤" in line:
                results.append({
                    "id": current_md,
                    "poem": md_poem,
                    "interp1": md_i1,
                    "interp2": md_i2
                })
                current_md = None

    if current_md is not None:
        results.append({
            "id": current_md,
            "poem": md_poem,
            "interp1": md_i1,
            "interp2": md_i2
        })

    # Standardize IDs (1 to 384), map 0 back to 384
    unique_items = {}
    for r in results:
        id_val = r["id"]
        if id_val == 0:
            id_val = 384
        
        r["id"] = id_val
        unique_items[id_val] = r

    final_list = [unique_items[k] for k in sorted(unique_items.keys())]
    
    print(f"Extracted {len(final_list)} unique lots.")
    
    missing = [i for i in range(1, 385) if i not in unique_items]
    if missing:
        print(f"Missing lots: {missing}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)
        
    print(f"Saved into {os.path.abspath(output_path)}")

if __name__ == "__main__":
    main()
