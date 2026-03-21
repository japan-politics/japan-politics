"""
国会議員データ取得スクリプト
- 衆議院: www.shugiin.go.jp の 1giin.htm〜10giin.htm（cp932）
- 参議院: ローカル保存済みHTML or ライブ取得（utf-8）
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os, time, re


# ─── 党名正規化マップ ─────────────────────────────────────────
# 衆議院・参議院で略称が共通のものは同じ正式名称に統一
# ※ Pythonの dict はキー重複不可（後勝ち）のため院ごとに分離

_PARTY_MAP_SYU = {
    '自民':    '自由民主党',
    '維新':    '日本維新の会',
    '国民':    '国民民主党',
    '共産':    '日本共産党',
    '参政':    '参政党',
    'みらい':  'チームみらい',
    '中道':    '中道改革連合',
    '無':      '無所属',
    # 以下は念のため（衆議院に出現した場合）
    '立憲':    '立憲民主党',
    '公明':    '公明党',
}

_PARTY_MAP_SAN = {
    '自民':    '自由民主党',
    '立憲':    '中道改革連合',
    '民主':    '国民民主党',
    '公明':    '中道改革連合',
    '維新':    '日本維新の会',
    '参政':    '参政党',
    '共産':    '日本共産党',
    'れ新':    'れいわ新選組',
    '保守':    '日本保守党',
    '沖縄':    '沖縄の風',
    'みら':    'チームみらい',
    '社民':    '社会民主党',
    '無所属':  '無所属',
}

def normalize_party(party: str, chamber: str) -> str:
    """院名に応じた略称→正式名称変換。マップにない場合はそのまま返す"""
    party = party.strip()
    mapping = _PARTY_MAP_SYU if chamber == '衆議院' else _PARTY_MAP_SAN
    return mapping.get(party, party)


# ─── 共通ユーティリティ ───────────────────────────────────────

def clean_name(s: str) -> str:
    """氏名のスペース・全角スペース・「君」・旧姓[]表記を除去"""
    s = re.sub(r'\[.*?\]', '', s)          # [旧姓] を除去
    return re.sub(r'[君\s\u3000]+', '', s)

def clean_yomi(s: str) -> str:
    """ふりがなのスペース・全角スペースを除去"""
    return re.sub(r'[\s\u3000]+', '', s)



# ─── 衆議院 ───────────────────────────────────────────────────

def get_shugiin_data():
    all_members = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for i in range(1, 11):
        url = f"https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/{i}giin.htm"
        print(f"衆議院 {i}ページ目取得中...")
        try:
            response = requests.get(url, headers=headers, timeout=15)
            # .content（生バイト）+ from_encoding='cp932' で文字化けを防ぐ
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='cp932')

            # テーブルは5列構造: 漢字名 | よみがな | 党派 | 選挙区 | 当選回数
            found = 0
            for row in soup.find_all('tr'):
                tds = row.find_all('td')
                if len(tds) != 5:
                    continue
                kanji = tds[0].get_text(strip=True)
                # ヘッダー行をスキップ
                if not kanji or kanji in ('氏名', '名前', '議員氏名'):
                    continue
                if not re.search(r'[\u4e00-\u9fff\u3040-\u30ff]', kanji):
                    continue

                all_members.append({
                    'chamber':  '衆議院',
                    'name':     clean_name(kanji),
                    'yomi':     clean_yomi(tds[1].get_text(separator='', strip=True)),
                    'party':    normalize_party(tds[2].get_text(strip=True), '衆議院'),
                    'district': tds[3].get_text(strip=True),
                    'img_url':  '',
                })
                found += 1

            print(f"  → {found}名取得")
            time.sleep(1)

        except Exception as e:
            print(f"  → エラー: {e}")

    return all_members


# ─── 参議院（ライブ取得） ─────────────────────────────────────

def get_sangiin_data_live():
    headers = {'User-Agent': 'Mozilla/5.0'}

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

    return []


# ─── 参議院（保存済みHTMLから取得） ──────────────────────────

def get_sangiin_data_from_file(filepath: str):
    """ブラウザで保存した参議院議員一覧HTMLからデータを取得する"""
    print(f"参議院データをファイルから取得: {filepath}")
    with open(filepath, 'rb') as f:
        raw = f.read()
    members = _parse_sangiin_html(raw.decode('utf-8', errors='replace'))
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

        href = a_tags[0].get('href', '')
        m    = re.search(r'profile/(\d+)\.htm', href)
        pid  = m.group(1) if m else ''

        members.append({
            'chamber':  '参議院',
            'name':     clean_name(tds[0].get_text(strip=True)),
            'yomi':     clean_yomi(tds[1].get_text(strip=True)),
            'party':    normalize_party(tds[2].get_text(strip=True), '参議院'),
            'district': tds[3].get_text(strip=True),
            'img_url':  (
                f"https://www.sangiin.go.jp/japanese/joho1/kousei/giin/photo/g{pid}.jpg"
                if pid else ''
            ),
        })

    return members


# ─── メイン ──────────────────────────────────────────────────

def main():
    os.makedirs('_data', exist_ok=True)

    print("=== 衆議院データ取得 ===")
    shugiin = get_shugiin_data()
    print(f"衆議院合計: {len(shugiin)}名\n")

    print("=== 参議院データ取得 ===")
    sangiin_html = "議員一覧_50音順__参議院.html"
    if os.path.exists(sangiin_html):
        sangiin = get_sangiin_data_from_file(sangiin_html)
    else:
        sangiin = get_sangiin_data_live()
    print(f"参議院合計: {len(sangiin)}名\n")

    data = shugiin + sangiin
    if data:
        df = pd.DataFrame(data)
        # BOMなしUTF-8で保存（JekyllのCSV読み込みでBOMが列名認識を妨げるため）
        df.to_csv('_data/politicians.csv', index=False, encoding='utf-8')
        print(f"✅ 完了: {len(df)}名のデータを _data/politicians.csv に保存しました。")
        print(df[['chamber', 'name', 'party', 'district']].head(10).to_string(index=False))

        print("\n=== 取得後の party 一覧 ===")
        for party, count in df['party'].value_counts().items():
            print(f"  {party}: {count}名")
    else:
        print("❌ データが取得できませんでした。")


if __name__ == '__main__':
    main()