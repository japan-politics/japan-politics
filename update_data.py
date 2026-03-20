import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time
import re

def get_shugiin_data():
    all_members = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    for i in range(1, 11):
        url = f"https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/{i}giin.htm"
        print(f"衆議院 {i}ページ目取得中...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'shift_jis'
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.find_all('tr'):
                cols = row.find_all('td')
                # 衆議院: 氏名リンクがあるtdを探し、その行の2つ隣(党派)と3つ隣(選挙区)を取る
                a_tag = row.find('a', href=re.compile(r'OpenDocument&id='))
                if a_tag:
                    name = a_tag.get_text(strip=True).replace('君', '').replace('　', '').replace(' ', '')
                    # aタグがあるtdのインデックスを特定
                    tds = list(row.find_all('td'))
                    idx = -1
                    for j, td in enumerate(tds):
                        if td.find('a') == a_tag:
                            idx = j
                            break
                    
                    if idx != -1 and len(tds) > idx + 2:
                        party = tds[idx+2].get_text(strip=True)
                        district = tds[idx+3].get_text(strip=True) if len(tds) > idx+3 else ""
                        
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
        # 参議院: profileリンクを持つaタグが含まれる行だけを抽出（見出し行を排除）
        rows = soup.find_all('tr')
        for row in rows:
            a_tag = row.find('a', href=re.compile(r'profile/\d+\.htm'))
            if not a_tag:
                continue # 議員へのリンクがない行（見出し等）はスキップ
            
            cols = row.find_all('td')
            if len(cols) >= 4:
                name = a_tag.get_text(strip=True).replace('　', '').replace(' ', '')
                party = cols[2].get_text(strip=True).strip()
                district = cols[3].get_text(strip=True).strip()
                
                match = re.search(r'profile/(\d+)\.htm', a_tag.get('href', ''))
                img_url = f"https://www.sangiin.go.jp/japanese/joho1/kousei/giin/photo/{match.group(1)}.jpg" if match else ""
                all_members.append({'chamber': '参議院', 'name': name, 'party': party, 'district': district, 'img_url': img_url})
    except Exception as e:
        print(f"参議院エラー: {e}")
    return all_members

def main():
    shugiin = get_shugiin_data()
    sangiin = get_sangiin_data()
    data = shugiin + sangiin
    if data:
        df = pd.DataFrame(data)
        # 最終クレンジング：名前が「あ行」などの2文字以下の見出しっぽいものを排除
        df = df[df['name'].str.len() >= 2]
        os.makedirs('_data', exist_ok=True)
        df.to_csv('_data/politicians.csv', index=False, encoding='utf-8-sig')
        print(f"成功: 合計 {len(df)} 名（衆:{len(shugiin)} 参:{len(sangiin)}）を保存")
    else:
        print("データが空です")

if __name__ == "__main__":
    main()