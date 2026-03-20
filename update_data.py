import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time
import re

def get_shugiin_data():
    all_members = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for i in range(1, 11):
        url = f"https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/{i}giin.htm"
        print(f"衆議院 {i}ページ目取得中...")
        try:
            response = requests.get(url, headers=headers, timeout=15)

            # ポイント1: .content（生バイト）をBeautifulSoupに渡し from_encoding='cp932' を指定する
            # response.encoding = 'shift_jis' + response.text ではブラウザ保存と同様に漢字が文字化けする
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='cp932')

            # ポイント2: このページに OpenDocument リンクは存在しない
            # テーブルは5列構造: 漢字名 | よみがな | 党派 | 選挙区 | 当選回数
            found = 0
            for row in soup.find_all('tr'):
                tds = row.find_all('td')
                if len(tds) != 5:
                    continue

                kanji    = tds[0].get_text(strip=True)
                yomi     = tds[1].get_text(separator='', strip=True)
                party    = tds[2].get_text(strip=True)
                district = tds[3].get_text(strip=True)
                wins     = tds[4].get_text(strip=True)

                # ヘッダ行・空行をスキップ（漢字または仮名を含む行だけ残す）
                if not kanji or not re.search(r'[\u4e00-\u9fff\u3040-\u30ff]', kanji):
                    continue

                name = re.sub(r'[君\s\u3000]', '', kanji)

                # ポイント3: ページ内に個人IDリンクがないため img_url は組み立て不可 → 空欄
                all_members.append({
                    'chamber': '衆議院',
                    'name': name,
                    'yomi': yomi,
                    'party': party,
                    'district': district,
                    'wins': wins,
                    'img_url': '',
                })
                found += 1

            print(f"  → {found}名取得")
            time.sleep(1)

        except Exception as e:
            print(f"  → エラー: {e}")
            continue

    return all_members


def get_sangiin_data():
    all_members = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    # ポイント4: 参議院URLは会期番号入り。最新会期から降順に試みて最初に取れた会期を使う
    for session in range(217, 204, -1):
        url = f"https://www.sangiin.go.jp/japanese/joho1/kousei/giin/{session}/giin.htm"
        print(f"参議院 会期{session} 試行中...")
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                continue
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            found = 0
            for row in soup.find_all('tr'):
                a_tag = row.find('a', href=re.compile(r'profile/\d+\.htm'))
                if not a_tag:
                    continue
                cols = row.find_all('td')
                if len(cols) < 4:
                    continue

                name     = re.sub(r'[\s\u3000]', '', a_tag.get_text(strip=True))
                party    = cols[2].get_text(strip=True)
                district = cols[3].get_text(strip=True)

                match = re.search(r'profile/(\d+)\.htm', a_tag.get('href', ''))
                img_url = (
                    f"https://www.sangiin.go.jp/japanese/joho1/kousei/giin/photo/{match.group(1)}.jpg"
                    if match else ''
                )
                all_members.append({
                    'chamber': '参議院',
                    'name': name,
                    'yomi': '',
                    'party': party,
                    'district': district,
                    'wins': '',
                    'img_url': img_url,
                })
                found += 1

            if found > 0:
                print(f"  → {found}名取得（会期{session}）")
                break  # 取得成功したら終了
            time.sleep(1)

        except Exception as e:
            print(f"  → エラー: {e}")
            continue

    return all_members


def main():
    print("=== 衆議院データ取得 ===")
    shugiin = get_shugiin_data()
    print(f"衆議院合計: {len(shugiin)}名\n")

    print("=== 参議院データ取得 ===")
    sangiin = get_sangiin_data()
    print(f"参議院合計: {len(sangiin)}名\n")

    data = shugiin + sangiin
    if data:
        df = pd.DataFrame(data)
        os.makedirs('_data', exist_ok=True)
        df.to_csv('_data/politicians.csv', index=False, encoding='utf-8-sig')
        print(f"成功: {len(df)}名のデータを _data/politicians.csv に保存しました。")
        print(df[['chamber', 'name', 'party', 'district']].head(10).to_string(index=False))
    else:
        print("データが取得できませんでした。")


if __name__ == '__main__':
    main()