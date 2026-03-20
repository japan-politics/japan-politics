import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time

def get_shugiin_data():
    all_members = []
    # 衆議院の五十音別URL（1:あ, 2:か, 3:さ, 4:た, 5:な, 6:は, 7:ま, 8:や, 9:ら, 10:わ）
    base_url = "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/{giin_page}giin.htm"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for i in range(1, 11):
        url = base_url.format(giin_page=i)
        print(f"ページ {i} を取得中: {url}")
        
        try:
            response = requests.get(url, headers=headers)
            response.encoding = 'shift_jis'
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        # 氏名から「君」を取り除き、空白を詰める
                        name = cols[0].get_text(strip=True).replace('\n', '').replace(' ', '').replace('　', '').replace('君', '')
                        party = cols[1].get_text(strip=True).replace('\n', '').replace(' ', '').replace('　', '')
                        district = cols[2].get_text(strip=True).replace('\n', '')
                        
                        # ヘッダーやフッターの除外ロジック
                        if name and name != '氏名' and '一覧' not in name and len(name) < 20:
                            all_members.append({
                                'name': name,
                                'party': party,
                                'district': district,
                                'chamber': '衆議院'
                            })
            
            # サーバー負荷軽減のため少し待機
            time.sleep(1)

        except Exception as e:
            print(f"ページ {i} でエラーが発生しました: {e}")
            continue
            
    return pd.DataFrame(all_members)

def main():
    print("全議員データの取得を開始します...")
    df_shugiin = get_shugiin_data()
    
    if not df_shugiin.empty:
        os.makedirs('_data', exist_ok=True)
        # 既存のCSVを上書き
        df_shugiin.to_csv('_data/politicians.csv', index=False, encoding='utf-8-sig')
        print(f"成功: 合計 {len(df_shugiin)} 名のデータを保存しました。")
    else:
        print("有効なデータを取得できませんでした。")
        exit(1)

if __name__ == "__main__":
    main()