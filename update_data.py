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
# スクレイピングで取得される略称 → 正式名称
PARTY_MAP = {
    # 衆議院
    '自民':    '自由民主党',
    '中道':    '中道改革連合',
    '維新':    '日本維新の会',
    '国民':    '国民民主党',
    '共産':    '日本共産党',
    '参政':    '参政党',
    'みらい':  'チームみらい',
    '無':      '無所属',
    # 参議院
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
    '無所属':    '無所属'
}

def normalize_party(party: str) -> str:
    """略称を正式名称に変換。マップにない場合はそのまま返す"""
    return PARTY_MAP.get(party.strip(), party.strip())


# ─── 共通ユーティリティ ───────────────────────────────────────

def clean_name(s: str) -> str:
    """氏名のスペース・全角スペース・「君」を除去"""
    return re.sub(r'[君\s\u3000]+', '', s)

def clean_yomi(s: str) -> str:
    """ふりがなのスペース・全角スペースを除去"""
    return re.sub(r'[\s\u3000]+', '', s)

_REIWA_BASE  = 2018  # 令和N年 = 2018+N
_HEISEI_BASE = 1988  # 平成N年 = 1988+N
_SHOWA_BASE  = 1925  # 昭和N年 = 1925+N

def wareki_to_yyyymmdd(s: str) -> str:
    """和暦日付文字列を yyyymmdd に変換。変換不能な場合は元の文字列を返す"""
    s = s.strip()
    if not s:
        return ''
    for pattern, base in [
        (r'令和\s*(\d+)\s*年\s*(\d+)\s*月\s*(\d+)\s*日', _REIWA_BASE),
        (r'平成\s*(\d+)\s*年\s*(\d+)\s*月\s*(\d+)\s*日', _HEISEI_BASE),
        (r'昭和\s*(\d+)\s*年\s*(\d+)\s*月\s*(\d+)\s*日', _SHOWA_BASE),
    ]:
        m = re.match(pattern, s)
        if m:
            y = base + int(m.group(1))
            return f"{y}{int(m.group(2)):02d}{int(m.group(3)):02d}"
    m = re.match(r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', s)
    if m:
        return f"{m.group(1)}{int(m.group(2)):02d}{int(m.group(3)):02d}"
    return s


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
                    'party':    normalize_party(tds[2].get_text(strip=True)),
                    'district': tds[3].get_text(strip=True),
                    'term':     '',
                    'wins':     tds[4].get_text(strip=True),
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
            'party':    normalize_party(tds[2].get_text(strip=True)),
            'district': tds[3].get_text(strip=True),
            'term':     wareki_to_yyyymmdd(tds[4].get_text(strip=True)),
            'wins':     '',
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
        df.to_csv('_data/politicians.csv', index=False, encoding='utf-8-sig')
        print(f"✅ 完了: {len(df)}名のデータを _data/politicians.csv に保存しました。")
        print(df[['chamber', 'name', 'party', 'district']].head(10).to_string(index=False))

        # 党名一覧を表示して確認
        print("\n=== 取得後の party 一覧 ===")
        for party, count in df['party'].value_counts().items():
            print(f"  {party}: {count}名")
    else:
        print("❌ データが取得できませんでした。")


if __name__ == '__main__':
    main()