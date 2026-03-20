import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time
import re

def get_shugiin_data():
    all_members = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    for i in range(1, 11):
        url = f"https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/{i}giin.htm"
        try:
            response = requests.get(url, headers=headers)
            response.encoding = 'shift_jis'
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) >= 3:
                    name_tag = cols[0].find('a')
                    if name_tag:
                        name = name_tag.get_text(strip=True).replace('君', '').replace('　', '')
                        # 衆議院: 0=氏名, 1=ふりがな, 2=党派, 3=選挙区
                        party = cols[2].get_text(strip=True).replace('\n', '').strip()
                        district = cols[3].get_text(strip=True).strip() if len(cols) > 3 else ""
                        
                        # 党派名の正規化
                        party = '自民' if '自民' in party else party
                        party = '立憲' if ('中道' in party or '立憲' in party) else party
                        
                        match = re.search(r'id=([^&]+)', name_tag.get('href', ''))
                        img_url = f"https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/giin/photo/{match.group(1)}.jpg" if match else ""
                        
                        if name and name != "氏名":
                            all_members.append({'chamber': '衆議院', 'name': name, 'party': party, 'district': district, 'img_url': img_url})
            time.sleep(1)
        except: continue
    return all_members

def get_sangiin_data():
    all_members = []
    url = "https://www.sangiin.go.jp/japanese/joho1/kousei/giin/221/giin.htm"
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='list_h25')
        if table:
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) >= 4:
                    name_tag = cols[0].find('a')
                    if name_tag:
                        name = name_tag.get_text(strip=True).replace('　', '')
                        # 参議院: 0=氏名, 1=ふりがな, 2=党派, 3=選挙区
                        party = cols[2].get_text(strip=True).strip()
                        district = cols[3].get_text(strip=True).strip()
                        
                        match = re.search(r'profile/(\d+)\.htm', name_tag.get('href', ''))
                        img_url = f"https://www.sangiin.go.jp/japanese/joho1/kousei/giin/photo/{match.group(1)}.jpg" if match else ""
                        all_members.append({'chamber': '参議院', 'name': name, 'party': party, 'district': district, 'img_url': img_url})
    except: pass
    return all_members

def main():
    data = get_shugiin_data() + get_sangiin_data()
    if data:
        df = pd.DataFrame(data)
        os.makedirs('_data', exist_ok=True)
        df.to_csv('_data/politicians.csv', index=False, encoding='utf-8-sig')
        print(f"Data Update: {len(df)} members.")

if __name__ == "__main__":
    main()