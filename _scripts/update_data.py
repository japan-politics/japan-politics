"""
蝗ｽ莨夊ｭｰ蜩｡繝・・繧ｿ蜿門ｾ励せ繧ｯ繝ｪ繝励ヨ
- 陦・ｭｰ髯｢: www.shugiin.go.jp 縺ｮ 1giin.htm縲・0giin.htm・・p932・・
- 蜿りｭｰ髯｢: 繝ｭ繝ｼ繧ｫ繝ｫ菫晏ｭ俶ｸ医∩HTML or 繝ｩ繧､繝門叙蠕暦ｼ・tf-8・・
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os, time, re


# 笏笏笏 蜈壼錐豁｣隕丞喧繝槭ャ繝・笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏
# 陦・ｭｰ髯｢繝ｻ蜿りｭｰ髯｢縺ｧ逡･遘ｰ縺悟・騾壹・繧ゅ・縺ｯ蜷後§豁｣蠑丞錐遘ｰ縺ｫ邨ｱ荳
# 窶ｻ Python縺ｮ dict 縺ｯ繧ｭ繝ｼ驥崎､・ｸ榊庄・亥ｾ悟享縺｡・峨・縺溘ａ髯｢縺斐→縺ｫ蛻・屬

_PARTY_MAP_SYU = {
    '閾ｪ豌・:    '閾ｪ逕ｱ豌台ｸｻ蜈・,
    '邯ｭ譁ｰ':    '譌･譛ｬ邯ｭ譁ｰ縺ｮ莨・,
    '蝗ｽ豌・:    '蝗ｽ豌第ｰ台ｸｻ蜈・,
    '蜈ｱ逕｣':    '譌･譛ｬ蜈ｱ逕｣蜈・,
    '蜿よ帆':    '蜿よ帆蜈・,
    '縺ｿ繧峨＞':  '繝√・繝縺ｿ繧峨＞',
    '荳ｭ驕・:    '荳ｭ驕捺隼髱ｩ騾｣蜷・,
    '辟｡':      '辟｡謇螻・,
    # 莉･荳九・蠢ｵ縺ｮ縺溘ａ・郁｡・ｭｰ髯｢縺ｫ蜃ｺ迴ｾ縺励◆蝣ｴ蜷茨ｼ・
    '遶区・':    '遶区・豌台ｸｻ蜈・,
    '蜈ｬ譏・:    '蜈ｬ譏主・',
}

_PARTY_MAP_SAN = {
    '閾ｪ豌・:    '閾ｪ逕ｱ豌台ｸｻ蜈・,
    '遶区・':    '荳ｭ驕捺隼髱ｩ騾｣蜷・,
    '豌台ｸｻ':    '蝗ｽ豌第ｰ台ｸｻ蜈・,
    '蜈ｬ譏・:    '荳ｭ驕捺隼髱ｩ騾｣蜷・,
    '邯ｭ譁ｰ':    '譌･譛ｬ邯ｭ譁ｰ縺ｮ莨・,
    '蜿よ帆':    '蜿よ帆蜈・,
    '蜈ｱ逕｣':    '譌･譛ｬ蜈ｱ逕｣蜈・,
    '繧梧眠':    '繧後＞繧乗眠驕ｸ邨・,
    '菫晏ｮ・:    '譌･譛ｬ菫晏ｮ亥・',
    '豐也ｸ・:    '豐也ｸ・・鬚ｨ',
    '縺ｿ繧・:    '繝√・繝縺ｿ繧峨＞',
    '遉ｾ豌・:    '遉ｾ莨壽ｰ台ｸｻ蜈・,
    '辟｡謇螻・:  '辟｡謇螻・,
}

def normalize_party(party: str, chamber: str) -> str:
    """髯｢蜷阪↓蠢懊§縺溽払遘ｰ竊呈ｭ｣蠑丞錐遘ｰ螟画鋤縲ゅ・繝・・縺ｫ縺ｪ縺・ｴ蜷医・縺昴・縺ｾ縺ｾ霑斐☆"""
    party = party.strip()
    mapping = _PARTY_MAP_SYU if chamber == '陦・ｭｰ髯｢' else _PARTY_MAP_SAN
    return mapping.get(party, party)


# 笏笏笏 蜈ｱ騾壹Θ繝ｼ繝・ぅ繝ｪ繝・ぅ 笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏

def clean_name(s: str) -> str:
    """豌丞錐縺ｮ繧ｹ繝壹・繧ｹ繝ｻ蜈ｨ隗偵せ繝壹・繧ｹ繝ｻ縲悟菅縲阪・譌ｧ蟋甜]陦ｨ險倥ｒ髯､蜴ｻ"""
    s = re.sub(r'\[.*?\]', '', s)          # [譌ｧ蟋転 繧帝勁蜴ｻ
    return re.sub(r'[蜷媾s\u3000]+', '', s)

def clean_yomi(s: str) -> str:
    """縺ｵ繧翫′縺ｪ縺ｮ繧ｹ繝壹・繧ｹ繝ｻ蜈ｨ隗偵せ繝壹・繧ｹ繧帝勁蜴ｻ"""
    return re.sub(r'[\s\u3000]+', '', s)



# 笏笏笏 陦・ｭｰ髯｢ 笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏

def get_shugiin_data():
    all_members = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for i in range(1, 11):
        url = f"https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/{i}giin.htm"
        print(f"陦・ｭｰ髯｢ {i}繝壹・繧ｸ逶ｮ蜿門ｾ嶺ｸｭ...")
        try:
            response = requests.get(url, headers=headers, timeout=15)
            # .content・育函繝舌う繝茨ｼ・ from_encoding='cp932' 縺ｧ譁・ｭ怜喧縺代ｒ髦ｲ縺・
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='cp932')

            # 繝・・繝悶Ν縺ｯ5蛻玲ｧ矩: 貍｢蟄怜錐 | 繧医∩縺後↑ | 蜈壽ｴｾ | 驕ｸ謖吝玄 | 蠖馴∈蝗樊焚
            found = 0
            for row in soup.find_all('tr'):
                tds = row.find_all('td')
                if len(tds) != 5:
                    continue
                kanji = tds[0].get_text(strip=True)
                # 繝倥ャ繝繝ｼ陦後ｒ繧ｹ繧ｭ繝・・
                if not kanji or kanji in ('豌丞錐', '蜷榊燕', '隴ｰ蜩｡豌丞錐'):
                    continue
                if not re.search(r'[\u4e00-\u9fff\u3040-\u30ff]', kanji):
                    continue

                all_members.append({
                    'chamber':  '陦・ｭｰ髯｢',
                    'name':     clean_name(kanji),
                    'yomi':     clean_yomi(tds[1].get_text(separator='', strip=True)),
                    'party':    normalize_party(tds[2].get_text(strip=True), '陦・ｭｰ髯｢'),
                    'district': tds[3].get_text(strip=True),
                    'img_url':  '',
                })
                found += 1

            print(f"  竊・{found}蜷榊叙蠕・)
            time.sleep(1)

        except Exception as e:
            print(f"  竊・繧ｨ繝ｩ繝ｼ: {e}")

    return all_members


# 笏笏笏 蜿りｭｰ髯｢・医Λ繧､繝門叙蠕暦ｼ・笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏

def get_sangiin_data_live():
    headers = {'User-Agent': 'Mozilla/5.0'}

    for session in range(221, 204, -1):
        url = f"https://www.sangiin.go.jp/japanese/joho1/kousei/giin/{session}/giin.htm"
        print(f"蜿りｭｰ髯｢ 莨壽悄{session} 隧ｦ陦御ｸｭ...")
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                continue
            response.encoding = 'utf-8'
            members = _parse_sangiin_html(response.text)
            if members:
                print(f"  竊・{len(members)}蜷榊叙蠕暦ｼ井ｼ壽悄{session}・・)
                return members
            time.sleep(1)
        except Exception as e:
            print(f"  竊・繧ｨ繝ｩ繝ｼ: {e}")

    return []


# 笏笏笏 蜿りｭｰ髯｢・井ｿ晏ｭ俶ｸ医∩HTML縺九ｉ蜿門ｾ暦ｼ・笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏

def get_sangiin_data_from_file(filepath: str):
    """繝悶Λ繧ｦ繧ｶ縺ｧ菫晏ｭ倥＠縺溷盾隴ｰ髯｢隴ｰ蜩｡荳隕ｧHTML縺九ｉ繝・・繧ｿ繧貞叙蠕励☆繧・""
    print(f"蜿りｭｰ髯｢繝・・繧ｿ繧偵ヵ繧｡繧､繝ｫ縺九ｉ蜿門ｾ・ {filepath}")
    with open(filepath, 'rb') as f:
        raw = f.read()
    members = _parse_sangiin_html(raw.decode('utf-8', errors='replace'))
    print(f"  竊・{len(members)}蜷榊叙蠕・)
    return members


def _parse_sangiin_html(html_text: str):
    """蜿りｭｰ髯｢隴ｰ蜩｡荳隕ｧHTML縺ｮ蜈ｱ騾壹ヱ繝ｼ繧ｵ繝ｼ"""
    soup = BeautifulSoup(html_text, 'html.parser')
    members = []

    for row in soup.find_all('tr'):
        tds = row.find_all('td')
        # 6蛻玲ｧ矩: 豌丞錐 | 隱ｭ縺ｿ譁ｹ | 莨壽ｴｾ | 驕ｸ謖吝玄 | 莉ｻ譛滓ｺ莠・| ・育ｩｺ・・
        if len(tds) != 6:
            continue
        a_tags = row.find_all('a', href=re.compile(r'profile/\d+\.htm'))
        if not a_tags:
            continue

        href = a_tags[0].get('href', '')
        m    = re.search(r'profile/(\d+)\.htm', href)
        pid  = m.group(1) if m else ''

        members.append({
            'chamber':  '蜿りｭｰ髯｢',
            'name':     clean_name(tds[0].get_text(strip=True)),
            'yomi':     clean_yomi(tds[1].get_text(strip=True)),
            'party':    normalize_party(tds[2].get_text(strip=True), '蜿りｭｰ髯｢'),
            'district': tds[3].get_text(strip=True),
            'img_url':  (
                f"https://www.sangiin.go.jp/japanese/joho1/kousei/giin/photo/g{pid}.jpg"
                if pid else ''
            ),
        })

    return members


# 笏笏笏 繝｡繧､繝ｳ 笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏笏

def main():
    os.makedirs('_data', exist_ok=True)

    print("=== 陦・ｭｰ髯｢繝・・繧ｿ蜿門ｾ・===")
    shugiin = get_shugiin_data()
    print(f"陦・ｭｰ髯｢蜷郁ｨ・ {len(shugiin)}蜷構n")

    print("=== 蜿りｭｰ髯｢繝・・繧ｿ蜿門ｾ・===")
    sangiin_html = "隴ｰ蜩｡荳隕ｧ_50髻ｳ鬆・_蜿りｭｰ髯｢.html"
    if os.path.exists(sangiin_html):
        sangiin = get_sangiin_data_from_file(sangiin_html)
    else:
        sangiin = get_sangiin_data_live()
    print(f"蜿りｭｰ髯｢蜷郁ｨ・ {len(sangiin)}蜷構n")

    data = shugiin + sangiin
    if data:
        df = pd.DataFrame(data)
        # BOM縺ｪ縺誘TF-8縺ｧ菫晏ｭ假ｼ・ekyll縺ｮCSV隱ｭ縺ｿ霎ｼ縺ｿ縺ｧBOM縺悟・蜷崎ｪ崎ｭ倥ｒ螯ｨ縺偵ｋ縺溘ａ・・
        df.to_csv('_data/politicians.csv', index=False, encoding='utf-8')
        print(f"笨・螳御ｺ・ {len(df)}蜷阪・繝・・繧ｿ繧・_data/politicians.csv 縺ｫ菫晏ｭ倥＠縺ｾ縺励◆縲・)
        print(df[['chamber', 'name', 'party', 'district']].head(10).to_string(index=False))

        print("\n=== 蜿門ｾ怜ｾ後・ party 荳隕ｧ ===")
        for party, count in df['party'].value_counts().items():
            print(f"  {party}: {count}蜷・)
    else:
        print("笶・繝・・繧ｿ縺悟叙蠕励〒縺阪∪縺帙ｓ縺ｧ縺励◆縲・)


if __name__ == '__main__':
    main()