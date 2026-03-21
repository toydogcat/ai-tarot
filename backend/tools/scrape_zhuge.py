import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re

def scrape_zhuge():
    os.makedirs('data/zhuge', exist_ok=True)
    all_lots = []
    
    # 嘗試不同的來源網站，如果一個失敗就換另一個
    sources = [
        "https://www.zgjm.org/chouqian/zhuge/{}.html",
        "https://m.httpcn.com/zhuge/{}.html"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    }
    
    print("Starting scraping Zhuge Shensuan (384 lots)...")
    
    for i in range(1, 10): # 先測試 1-10
        url = sources[0].format(i)
        try:
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                resp.encoding = 'utf-8' # or 'gbk' depending on site
                soup = BeautifulSoup(resp.text, 'lxml')
                # zgjm.org specific parsing
                content_div = soup.find('div', class_='intro') or soup.find('div', class_='content')
                if content_div:
                    text = content_div.get_text(separator='\n', strip=True)
                    all_lots.append({
                        "id": str(i),
                        "poem": text
                    })
                    print(f"Successfully scraped lot {i}")
                else:
                    print(f"Could not find content div for lot {i}")
            else:
                print(f"Failed to fetch lot {i}, status code: {resp.status_code}")
        except Exception as e:
            print(f"Error fetching lot {i}: {e}")
            break
        time.sleep(1) # delay to avoid rate limit
        
    print(f"Scraped {len(all_lots)} lots.")
    if len(all_lots) > 0:
        with open('data/zhuge/zhuge_data_test.json', 'w', encoding='utf-8') as f:
            json.dump(all_lots, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scrape_zhuge()
