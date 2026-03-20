import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time
import re

def get_shugiin_data():
    all_members = []
    base_url = "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/{giin_page}giin.htm"
    # 画像のベースURL
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
                        # 名前、党派、選挙区を取得
                        name_raw = cols[0].get_text(strip=True)
                        name = name_raw.replace('　', '').replace(' ', '').replace('君', '')
                        party = cols[1].get_text(strip=True)
                        district = cols[2].get_text(strip=True)
                        
                        # 画像URLを取得 (aタグのhrefからIDを特定し、画像URLを推測する)
                        img_url = ""
                        a_tag = cols[0].find('a')
                        if a_tag and 'href' in a_tag.attrs:
                            href = a_tag['href']
                            # hrefから議員IDを抽出 (例: OpenDocument&id=...)
                            match = re.search(r'id=([^&]+)', href)
                            if match:
                                giin_id = match.group(1)
                                # 衆議院の画像URLパターン (IDに基づいて画像が配置されている)
                                # 実際にはIDと画像名が完全に一致しない場合があるため、
                                # 確実な方法は詳細ページへアクセスしてimgタグを探すことだが、
                                # 負荷軽減のため、ここでは推測URLを使用（要確認）
                                # ※多くの場合はID.jpgだが、例外もある
                                img_url = f"{img_base_url}/internet/itdb_annai.nsf/html/statics/giin/photo/{giin_id}.jpg"

                        if name and name != '氏名' and '一覧' not in name:
                            all_members.append({
                                'name': name,
                                'party': party,
                                'district': district,
                                'chamber': '衆議院',
                                'img_url': img_url # 画像URLを追加
                            })
            time.sleep(1)
        except Exception as e:
            print(f"衆議院 {i}ページ目でエラー: {e}")
    return all_members

def get_sangiin_data():
    all_members = []
    url = "https://www.sangiin.go.jp/japanese/joho1/kousei/giin/213/giin.htm"
    # 画像のベースURL
    img_base_url = "https://www.sangiin.go.jp"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 参議院のテーブル構造を解析
        table = soup.find('table', class_='list_h25') or soup.find('table')
        if table:
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) >= 3:
                    name_raw = cols[0].get_text(strip=True)
                    name = name_raw.replace('　', '').replace(' ', '')
                    party = cols[2].get_text(strip=True)
                    district = cols[3].get_text(strip=True)
                    
                    # 画像URLを取得 (aタグのhrefから詳細ページのURLを取得し、そこからIDを特定)
                    img_url = ""
                    a_tag = cols[0].find('a')
                    if a_tag and 'href' in a_tag.attrs:
                        href = a_tag['href']
                        # hrefから議員IDを抽出 (例: ../giin/ID.htm)
                        match = re.search(r'giin/([^.]+)\.htm', href)
                        if match:
                            giin_id = match.group(1)
                            # 参議院の画像URLパターン (ID.jpg)
                            img_url = f"{img_base_url}/japanese/joho1/kousei/giin/photo/{giin_id}.jpg"

                    if name and name != '氏名':
                        all_members.append({
                            'name': name,
                            'party': party,
                            'district': district,
                            'chamber': '参議院',
                            'img_url': img_url # 画像URLを追加
                        })
    except Exception as e:
        print(f"参議院データ取得エラー: {e}")
    
    return all_members

def main():
    print("衆議院データの取得中...")
    shugiin = get_shugiin_data()
    
    print("参議院データの取得中...")
    sangiin = get_sangiin_data()
    
    total_data = shugiin + sangiin
    
    if total_data:
        df = pd.DataFrame(total_data)
        # 列の順序を整理
        df = df[['chamber', 'name', 'party', 'district', 'img_url']]
        os.makedirs('_data', exist_ok=True)
        df.to_csv('_data/politicians.csv', index=False, encoding='utf-8-sig')
        print(f"完了: 合計 {len(df)} 名のデータを保存しました（画像URL付き）")
    else:
        print("データが取得できませんでした。")
        exit(1)

if __name__ == "__main__":
    main()