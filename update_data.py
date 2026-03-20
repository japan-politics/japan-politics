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
        print(f"衆議院 {i}ページ目取得中...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'shift_jis'
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.find_all('tr'):
                cols = row.find_all('td')
                # 衆議院の有効なデータ行は通常4列（氏名、ふりがな、党派、選挙区）
                if len(cols) >= 3:
                    name_tag = cols[0].find('a')
                    if name_tag:
                        name = name_tag.get_text(strip=True).replace('君', '').replace('　', '')
                        # 列ズレ修正: 0=氏名, 1=ふりがな(スキップ), 2=党派, 3=選挙区
                        party = cols[2].get_text(strip=True).replace('\n', '').strip() if len(cols) > 2 else ""
                        district = cols[3].get_text(strip=True).strip() if len(cols) > 3 else ""
                        
                        # 党派名の正規化
                        party = '自民' if '自民' in party else party
                        party = '立憲' if ('中道' in party or '立憲' in party) else party
                        
                        # 画像IDの抽出
                        img_url = ""
                        match = re.search(r'id=([^&]+)', name_tag.get('href', ''))
                        if match:
                            img_url = f"https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/giin/photo/{match.group(1)}.jpg"
                        
                        if name and name != "氏名":
                            all_members.append({'chamber': '衆議院', 'name': name, 'party': party, 'district': district, 'img_url': img_url})
            time.sleep(1)
        except Exception as e:
            print(f"衆議院エラー: {e}")
    return all_members

def get_sangiin_data():
    all_members = []
    # 参議院は1ページにまとまっている（第221回国会）
    url = "https://www.sangiin.go.jp/japanese/joho1/kousei/giin/221/giin.htm"
    headers = {'User-Agent': 'Mozilla/5.0'}
    print("参議院データ取得中...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='list_h25') or soup.find('table')
        if table:
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                # 参議院: 0=氏名, 1=ふりがな, 2=党派, 3=選挙区
                if len(cols) >= 4:
                    name_tag = cols[0].find('a')
                    if name_tag:
                        name = name_tag.get_text(strip=True).replace('　', '')
                        party = cols[2].get_text(strip=True).strip()
                        district = cols[3].get_text(strip=True).strip()
                        
                        # 画像IDの抽出
                        img_url = ""
                        match = re.search(r'profile/(\d+)\.htm', name_tag.get('href', ''))
                        if match:
                            img_url = f"https://www.sangiin.go.jp/japanese/joho1/kousei/giin/photo/{match.group(1)}.jpg"
                        
                        if name and name != "氏名":
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
        # 不要な空行・見出し行の除外を徹底
        df = df[df['name'] != ""]
        os.makedirs('_data', exist_ok=True)
        df.to_csv('_data/politicians.csv', index=False, encoding='utf-8-sig')
        print(f"完了: 合計 {len(df)} 名のデータを保存しました。")
    else:
        print("データが取得できませんでした。")

if __name__ == "__main__":
    main()