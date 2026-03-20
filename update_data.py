import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time
import re

def get_shugiin_data():
    all_members = []
    base_url = "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/{giin_page}giin.htm"
    img_base_url = "https://www.shugiin.go.jp"
    headers = {'User-Agent': 'Mozilla/5.0'}

    for i in range(1, 11):
        url = base_url.format(giin_page=i)
        print(f"衆議院 {i}ページ目取得中...")
        try:
            response = requests.get(url, headers=headers)
            response.encoding = 'shift_jis'
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            for table in tables:
                for row in table.find_all('tr'):
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        name_raw = cols[0].get_text(strip=True)
                        # 「氏名」という文字や空行をスキップ
                        if not name_raw or "氏名" in name_raw or "一覧" in name_raw:
                            continue

                        name = name_raw.replace('　', '').replace(' ', '').replace('君', '')
                        party = cols[1].get_text(strip=True).replace('\n', '').replace(' ', '')
                        district = cols[2].get_text(strip=True).replace('\n', '').replace(' ', '')
                        
                        img_url = ""
                        a_tag = cols[0].find('a')
                        if a_tag and 'href' in a_tag.attrs:
                            href = a_tag['href']
                            match = re.search(r'id=([^&]+)', href)
                            if match:
                                giin_id = match.group(1)
                                img_url = f"{img_base_url}/internet/itdb_annai.nsf/html/statics/giin/photo/{giin_id}.jpg"

                        all_members.append({
                            'chamber': '衆議院',
                            'name': name,
                            'party': party,
                            'district': district,
                            'img_url': img_url
                        })
            time.sleep(1)
        except Exception as e:
            print(f"衆議院 {i}ページ目でエラー: {e}")
    return all_members

def get_sangiin_data():
    all_members = []
    url = "https://www.sangiin.go.jp/japanese/joho1/kousei/giin/221/giin.htm"
    img_base_url = "https://www.sangiin.go.jp"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find('table', class_='list_h25') or soup.find('table')
        if table:
            for row in table.find_all('tr'):
                # <th>（見出し）が含まれる行は完全にスキップ
                if row.find('th'):
                    continue
                    
                cols = row.find_all('td')
                # 参議院の有効なデータ行は通常6列程度あります
                if len(cols) >= 4:
                    name_raw = cols[0].get_text(strip=True)
                    # 不要な単語が含まれる行を除外
                    if not name_raw or "氏名" in name_raw or "当選回数" in name_raw:
                        continue

                    name = name_raw.replace('　', '').replace(' ', '')
                    party = cols[2].get_text(strip=True).replace('\n', '').replace(' ', '')
                    district = cols[3].get_text(strip=True).replace('\n', '').replace(' ', '')
                    
                    img_url = ""
                    a_tag = cols[0].find('a')
                    if a_tag and 'href' in a_tag.attrs:
                        href = a_tag['href']
                        # 参議院のパス構造 profile/70xxxxx.htm からIDを抽出
                        match = re.search(r'profile/(\d+)\.htm', href)
                        if match:
                            giin_id = match.group(1)
                            img_url = f"{img_base_url}/japanese/joho1/kousei/giin/photo/{giin_id}.jpg"

                    all_members.append({
                        'chamber': '参議院',
                        'name': name,
                        'party': party,
                        'district': district,
                        'img_url': img_url
                    })
    except Exception as e:
        print(f"参議院データ取得エラー: {e}")
    
    return all_members

def main():
    print("データ取得を開始します...")
    shugiin = get_shugiin_data()
    sangiin = get_sangiin_data()
    
    total_data = shugiin + sangiin
    
    if total_data:
        df = pd.DataFrame(total_data)
        # 列の順番をHTMLの表示順（顔写真以外）に合わせる
        df = df[['chamber', 'name', 'party', 'district', 'img_url']]
        os.makedirs('_data', exist_ok=True)
        # CSV保存
        df.to_csv('_data/politicians.csv', index=False, encoding='utf-8-sig')
        print(f"成功: 合計 {len(df)} 名のデータを保存しました。")
    else:
        print("データが取得できませんでした。")
        exit(1)

if __name__ == "__main__":
    main()