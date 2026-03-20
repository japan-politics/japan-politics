"""
国会議員データ取得スクリプト
- 衆議院: www.shugiin.go.jp の 1giin.htm〜10giin.htm（cp932）
- 参議院: ローカル保存済みHTML or ライブ取得（utf-8）
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os, time, re


# ─── 衆議院 ───────────────────────────────────────────────────
def get_shugiin_data():
    all_members = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for i in range(1, 11):
        url = f"https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/{i}giin.htm"
        print(f"衆議院 {i}ページ目取得中...")
        try:
            response = requests.get(url, headers=headers, timeout=15)
            # ポイント: .content（生バイト）+ from_encoding='cp932'
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='cp932')

            # テーブルは5列構造: 漢字名 | よみがな | 党派 | 選挙区 | 当選回数
            found = 0
            for row in soup.find_all('tr'):
                tds = row.find_all('td')
                if len(tds) != 5:
                    continue
                kanji = tds[0].get_text(strip=True)
                if not kanji or not re.search(r'[\u4e00-\u9fff\u3040-\u30ff]', kanji):
                    continue
                name     = re.sub(r'[君\s\u3000]', '', kanji)
                yomi     = tds[1].get_text(separator='', strip=True)
                party    = tds[2].get_text(strip=True)
                district = tds[3].get_text(strip=True)
                wins     = tds[4].get_text(strip=True)
                all_members.append({
                    'chamber': '衆議院', 'name': name, 'yomi': yomi,
                    'party': party, 'district': district,
                    'term': '', 'wins': wins, 'img_url': '',
                })
                found += 1
            print(f"  → {found}名取得")
            time.sleep(1)
        except Exception as e:
            print(f"  → エラー: {e}")
    return all_members


# ─── 参議院（ライブ取得） ─────────────────────────────────────
def get_sangiin_data_live():
    all_members = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    # 最新会期から降順に試みる
    for session in range(221, 204, -1):
        url = f"https://www.sangiin.go.jp/japanese/joho1/kousei/giin/{session}/giin.htm"
        print(f"参議院 会期{session} 試行中...")
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                continue
            response.encoding = 'utf-8'
            members = _parse_sangiin_html(response.text)
            if members:
                print(f"  → {len(members)}名取得（会期{session}）")
                return members
            time.sleep(1)
        except Exception as e:
            print(f"  → エラー: {e}")
    return all_members


# ─── 参議院（保存済みHTMLから取得） ──────────────────────────
def get_sangiin_data_from_file(filepath: str):
    """
    ブラウザで保存した参議院議員一覧HTMLからデータを取得する。
    文字コードがUTF-8で正常に保存されている前提。
    """
    print(f"参議院データをファイルから取得: {filepath}")
    with open(filepath, 'rb') as f:
        raw = f.read()
    text = raw.decode('utf-8', errors='replace')
    members = _parse_sangiin_html(text)
    print(f"  → {len(members)}名取得")
    return members


def _parse_sangiin_html(html_text: str):
    """参議院議員一覧HTMLの共通パーサー"""
    soup = BeautifulSoup(html_text, 'html.parser')
    members = []
    for row in soup.find_all('tr'):
        tds = row.find_all('td')
        # 6列構造: 氏名 | 読み方 | 会派 | 選挙区 | 任期満了 | （空）
        if len(tds) != 6:
            continue
        a_tags = row.find_all('a', href=re.compile(r'profile/\d+\.htm'))
        if not a_tags:
            continue

        # 余分な全角スペースを整理
        name  = re.sub(r'\u3000+', '\u3000', tds[0].get_text(strip=True)).strip('\u3000')
        yomi  = tds[1].get_text(strip=True).replace('\u3000', ' ')
        party = tds[2].get_text(strip=True)
        dist  = tds[3].get_text(strip=True)
        term  = tds[4].get_text(strip=True)

        href  = a_tags[0].get('href', '')
        m = re.search(r'profile/(\d+)\.htm', href)
        pid = m.group(1) if m else ''
        img_url = (
            f"https://www.sangiin.go.jp/japanese/joho1/kousei/giin/photo/g{pid}.jpg"
            if pid else ''
        )
        members.append({
            'chamber': '参議院', 'name': name, 'yomi': yomi,
            'party': party, 'district': dist,
            'term': term, 'wins': '', 'img_url': img_url,
        })
    return members


# ─── メイン ──────────────────────────────────────────────────
def main():
    os.makedirs('_data', exist_ok=True)

    print("=== 衆議院データ取得 ===")
    shugiin = get_shugiin_data()
    print(f"衆議院合計: {len(shugiin)}名\n")

    print("=== 参議院データ取得 ===")
    # 保存済みHTMLがある場合はこちらを使う（確実）
    sangiin_html = "議員一覧_50音順__参議院.html"
    if os.path.exists(sangiin_html):
        sangiin = get_sangiin_data_from_file(sangiin_html)
    else:
        sangiin = get_sangiin_data_live()
    print(f"参議院合計: {len(sangiin)}名\n")

    data = shugiin + sangiin
    if data:
        df = pd.DataFrame(data)
        df.to_csv('_data/politicians.csv', index=False, encoding='utf-8-sig')
        print(f"✅ 完了: {len(df)}名のデータを _data/politicians.csv に保存しました。")
        print(df[['chamber', 'name', 'party', 'district']].head(10).to_string(index=False))
    else:
        print("❌ データが取得できませんでした。")


if __name__ == '__main__':
    main()