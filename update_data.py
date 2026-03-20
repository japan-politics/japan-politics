import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time
import re

def get_shugiin_data():
    all_members = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    # 衆議院は1〜10ページ
    for i in range(1, 11):
        url = f"https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/{i}giin.htm"
        print(f"衆議院 {i}ページ目取得中...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'shift_jis'
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.find_all('tr'):
                cols = row.find_all('td')
                # 衆議院の有効な行は通常「氏名(aタグ)」「ふりがな」「党派」「選挙区」の順
                # ただし、一部余分な空セルがある場合があるためaタグを基準に探します
                a_tag = row.find('a')
                if a_tag and 'id=' in a_tag.get('href', ''):
                    # aタグがあるセルを0番目としてカウント
                    idx = -1
                    for i, td in enumerate(cols):
                        if td.find('a'):
                            idx = i
                            break
                    
                    if idx != -1 and len(cols) > idx + 2:
                        name = a_tag.get_text(strip=True).replace('君', '').replace('　', '')
                        party = cols[idx+2].get_text(strip=True).strip()
                        district = cols[idx+3].get_text(strip=True).strip() if len(cols) > idx+3 else ""
                        
                        # 党派の正規化
                        party = '自民' if '自民' in party else party
                        party = '立憲' if ('立憲' in party or '中道' in party) else party
                        
                        match = re.search(r'id=([^&]+)', a_tag.get('href', ''))
                        img_url = f"https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/giin/photo/{match.group(1)}.jpg" if match else ""
                        
                        all_members.append({'chamber': '衆議院', 'name': name, 'party': party, 'district': district, 'img_url': img_url})
            time.sleep(1)
        except: continue
    return all_members

def get_sangiin_data():
    all_members = []
    url = "https://www.sangiin.go.jp/japanese/joho1/kousei/giin/221/giin.htm"
    headers = {'User-Agent': 'Mozilla/5.0'}
    print("参議院データ取得中...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='list_h25')
        if table:
            for row in table.find_all('tr'):
                # <th>（あ行、さ行など）がある行は完全にスキップ
                if row.find('th'): continue
                
                cols = row.find_all('td')
                if len(cols) >= 4:
                    a_tag = cols[0].find('a')
                    if a_tag:
                        name = a_tag.get_text(strip=True).replace('　', '')
                        party = cols[2].get_text(strip=True).strip()
                        district = cols[3].get_text(strip=True).strip()
                        
                        match = re.search(r'profile/(\d+)\.htm', a_tag.get('href', ''))
                        img_url = f"https://www.sangiin.go.jp/japanese/joho1/kousei/giin/photo/{match.group(1)}.jpg" if match else ""
                        all_members.append({'chamber': '参議院', 'name': name, 'party': party, 'district': district, 'img_url': img_url})
    except: pass
    return all_members

def main():
    data = get_shugiin_data() + get_sangiin_data()
    if data:
        df = pd.DataFrame(data)
        # 不要な見出し（あ行など）が混入しないよう再度フィルタリング
        df = df[~df['name'].str.contains('行')]
        os.makedirs('_data', exist_ok=True)
        df.to_csv('_data/politicians.csv', index=False, encoding='utf-8-sig')
        print(f"成功: 合計 {len(df)} 名のデータを保存しました。")

if __name__ == "__main__":
    main()