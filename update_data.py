import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from io import StringIO

def get_shugiin_data():
    # 実際のデータがある五十音順（あ行）のページ
    url = "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/1giin.htm"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        # 添付ファイルと同じく Shift_JIS でデコード
        response.encoding = 'shift_jis'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 議員データが入っているテーブルを特定
        # 衆議院のサイトは class="sh1table1" などのテーブルにデータがある
        tables = soup.find_all('table')
        
        member_list = []
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                # 議員情報の行は通常4〜5列構成
                if len(cols) >= 3:
                    # テキストを抽出して、余分な空白や改行を掃除
                    name = cols[0].get_text(strip=True).replace('\n', '').replace(' ', '').replace('　', '')
                    party = cols[1].get_text(strip=True).replace('\n', '')
                    district = cols[2].get_text(strip=True).replace('\n', '')
                    
                    # ヘッダー行や空行を除外
                    if name and name != '氏名' and '一覧' not in name:
                        member_list.append({
                            'name': name,
                            'party': party,
                            'district': district,
                            'chamber': '衆議院'
                        })
        
        return pd.DataFrame(member_list)

    except Exception as e:
        print(f"スクレイピング中にエラーが発生しました: {e}")
        return pd.DataFrame()

def main():
    print("データ取得を開始します...")
    df_shugiin = get_shugiin_data()
    
    if not df_shugiin.empty:
        os.makedirs('_data', exist_ok=True)
        # GitHubで管理しやすいよう UTF-8 (BOM付き) で保存
        df_shugiin.to_csv('_data/politicians.csv', index=False, encoding='utf-8-sig')
        print(f"成功: {len(df_shugiin)} 名のデータを保存しました。")
    else:
        print("有効なデータを取得できませんでした。")
        exit(1)

if __name__ == "__main__":
    main()