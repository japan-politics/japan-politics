import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

def get_shugiin_data():
    # 衆議院の議員一覧（五十音順）ページ
    url = "https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/giin/giin_kousei.htm"
    
    # SSLエラー回避のための設定（官公庁サイトで稀に必要）
    response = requests.get(url, verify=True)
    response.encoding = 'utf-8'

    # pandasのread_htmlを使用してtableタグを抽出
    # 衆議院のサイト構造に合わせて特定の属性を持つテーブルを探す
    dfs = pd.read_html(response.text)
    
    # 議員名簿が含まれるテーブルを特定して結合
    # ページ内に複数のテーブルがあるため、中身があるものを抽出
    all_members = []
    for df in dfs:
        # 「氏名」や「党派」という列名が含まれるテーブルが対象
        if '氏名' in df.columns or 0 in df.columns:
            all_members.append(df)
            
    if not all_members:
        print("データが見つかりませんでした。")
        return pd.DataFrame()

    final_df = pd.concat(all_members)
    
    # 列名の整理（サイトの構造によって列名がズレることがあるため調整）
    # ここでは仮に [氏名, 党派, 選挙区] の形に整形
    # 実際のサイト構造に合わせてリネーム
    final_df.columns = ['name', 'party', 'district', 'extra1', 'extra2'][:len(final_df.columns)]
    
    # データのクリーニング（空行の削除など）
    final_df = final_df.dropna(subset=['name'])
    final_df['chamber'] = '衆議院' # 衆議院フラグを立てる
    
    return final_df[['name', 'party', 'district', 'chamber']]

def main():
    print("データ取得を開始します...")
    
    # 衆議院データの取得
    df_shugiin = get_shugiin_data()
    
    # 保存先ディレクトリの確認
    os.makedirs('_data', exist_ok=True)
    
    # CSVとして保存（BOM付きUTF-8ならExcelでも化けにくい）
    df_shugiin.to_csv('_data/politicians.csv', index=False, encoding='utf-8-sig')
    
    print(f"成功: {len(df_shugiin)} 名のデータを保存しました。")

if __name__ == "__main__":
    main()