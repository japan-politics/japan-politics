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
                # 衆議院のIDリンクを持つaタグを起点にする
                a_tag = row.find('a', href=re.compile(r'OpenDocument&id='))
                if a_tag:
                    tds = row.find_all('td')
                    # 名前があるセルを0として、2つ隣が党派、3つ隣が選挙区
                    name_idx = -1
                    for j, td in enumerate(tds):
                        if td.find('a') == a_tag:
                            name_idx = j
                            break
                    if name_idx != -1 and len(tds) > name_idx + 2:
                        name = a_tag.get_text(strip=True).replace('君', '').replace('　', '').replace(' ', '')
                        party = tds[name_idx + 2].get_text(strip=True).strip()
                        district = tds[name_idx + 3].get_text(strip=True).strip() if len(tds) > name_idx + 3 else ""
                        
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
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        for row in soup.find_all('tr'):
            a_tag = row.find('a', href=re.compile(r'profile/\d+\.htm'))
            if a_tag:
                cols = row.find_all('td')
                if len(cols) >= 4:
                    name = a_tag.get_text(strip=True).replace('　', '').replace(' ', '')
                    party = cols[2].get_text(strip=True).strip()
                    district = cols[3].get_text(strip=True).strip()
                    match = re.search(r'profile/(\d+)\.htm', a_tag.get('href', ''))
                    img_url = f"https://www.sangiin.go.jp/japanese/joho1/kousei/giin/photo/{match.group(1)}.jpg" if match else ""
                    all_members.append({'chamber': '参議院', 'name': name, 'party': party, 'district': district, 'img_url': img_url})
    except: pass
    return all_members

def main():
    shugiin = get_shugiin_data()
    sangiin = get_sangiin_data()
    data = shugiin + sangiin
    if data:
        df = pd.DataFrame(data)
        os.makedirs('_data', exist_ok=True)
        df.to_csv('_data/politicians.csv', index=False, encoding='utf-8-sig')
        print(f"成功: {len(df)}名のデータを保存しました。")