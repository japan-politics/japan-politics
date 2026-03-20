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
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'shift_jis'
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.find_all('tr'):
                cols = row.find_all('td')
                # 衆議院の構造: 0:氏名(a), 1:ふりがな, 2:党派, 3:選挙区
                if len(cols) >= 3:
                    a_tag = cols[0].find('a')
                    if a_tag:
                        name = a_tag.get_text(strip=True).replace('君', '').replace('　', '')
                        # 列ズレ修正: 2番目(Index 2)が党派、3番目(Index 3)が選挙区
                        party = cols[2].get_text(strip=True).strip() if len(cols) > 2 else ""
                        district = cols[3].get_text(strip=True).strip() if len(cols) > 3 else ""
                        
                        # 党派名の正規化
                        party = '自民' if '自民' in party else party
                        party = '立憲' if ('中道' in party or '立憲' in party) else party
                        
                        # 画像URL
                        img_url = ""
                        match = re.search(r'id=([^&]+)', a_tag.get('href', ''))
                        if match:
                            img_url = f"https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/giin/photo/{match.group(1)}.jpg"
                        
                        if name and name != "氏名":
                            all_members.append({'chamber': '衆議院', 'name': name, 'party': party, 'district': district, 'img_url': img_url})
            time.sleep(1)
        except: continue
    return all_members

def get_sangiin_data():
    all_members = []
    # 第221回国会の最新URL
    url = "https://www.sangiin.go.jp/japanese/joho1/kousei/giin/221/giin.htm"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 参議院は特定のclassを持つtableを探す
        table = soup.find('table', class_='list_h25')
        if table:
            for row in table.find_all('tr'):
                # <th>が含まれる行（あ行、さ行など）はデータではないのでスキップ
                if row.find('th'): continue
                
                cols = row.find_all('td')
                # 参議院の構造: 0:氏名(a), 1:ふりがな, 2:党派, 3:選挙区
                if len(cols) >= 4:
                    a_tag = cols[0].find('a')
                    if a_tag:
                        name = a_tag.get_text(strip=True).replace('　', '')
                        party = cols[2].get_text(strip=True).strip()
                        district = cols[3].get_text(strip=True).strip()
                        
                        # 画像URL (profile/ID.htm から IDを抽出)
                        img_url = ""
                        match = re.search(r'profile/(\d+)\.htm', a_tag.get('href', ''))
                        if match:
                            img_url = f"https://www.sangiin.go.jp/japanese/joho1/kousei/giin/photo/{match.group(1)}.jpg"
                        
                        all_members.append({'chamber': '参議院', 'name': name, 'party': party, 'district': district, 'img_url': img_url})
    except: pass
    return all_members

def main():
    data = get_shugiin_data() + get_sangiin_data()
    if data:
        df = pd.DataFrame(data)
        # 不正な行（空の名前など）を除外
        df = df[df['name'].str.len() > 0]
        os.makedirs('_data', exist_ok=True)
        df.to_csv('_data/politicians.csv', index=False, encoding='utf-8-sig')
        print(f"成功: {len(df)}名のデータを保存しました。")

if __name__ == "__main__":
    main()