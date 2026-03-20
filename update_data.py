import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from io import StringIO

def get_shugiin_data():
    # 衆議院の議員一覧（五十音順）ページ
    url = "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/giin/giin_kousei.htm"
    
    response = requests.get(url, verify=True)
    response.encoding = 'utf-8'

    # 文字列をStringIOでラップして渡すことで警告を回避
    dfs = pd.read_html(StringIO(response.text))
    
    all_members = []
    for df in dfs:
        # 「氏名」という列が含まれるテーブルを抽出
        if any('氏名' in str(col) for col in df.columns):
            all_members.append(df)
            
    if not all_members:
        print("衆議院のデータテーブルが見つかりませんでした。")
        return pd.DataFrame()

    final_df = pd.concat(all_members)
    
    # サイトの列構成に合わせてリネーム（氏名, 党派, 選挙区）
    # 衆議院サイトは1列目が氏名、2列目が党派、3列目が選挙区
    final_df = final_df.iloc[:, :3] 
    final_df.columns = ['name', 'party', 'district']
    
    # ゴミデータの除去（ヘッダー行が混じる場合があるため）
    final_df = final_df[final_df['name'] != '氏名'].dropna(subset=['name'])
    final_df['chamber'] = '衆議院'
    
    return final_df

def main():
    print("データ取得を開始します...")
    
    try:
        df_shugiin = get_shugiin_data()
        
        if df_shugiin.empty:
            print("取得データが空です。処理を中断します。")
            return

        os.makedirs('_data', exist_ok=True)
        
        # 保存
        df_shugiin.to_csv('_data/politicians.csv', index=False, encoding='utf-8-sig')
        print(f"成功: {len(df_shugiin)} 名のデータを保存しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        exit(1) # エラーをGitHub Actionsに通知

if __name__ == "__main__":
    main()