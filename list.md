---
layout: default
title: 議員一覧
---

<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>

<style>
/* 顔写真のスタイル調整 */
.giin-photo {
    width: 50px;       /* 横幅を固定 */
    height: auto;      /* 縦横比を維持 */
    border-radius: 5px; /* 角を丸く */
    border: 1px solid #ccc; /* 枠線 */
}
/* DataTablesのセル内の配置調整 */
#politicianTable td {
    vertical-align: middle; /* 上下中央揃え */
}
</style>

# 議員一覧

衆議院および参議院の全議員リストです。顔写真は各院の公式サイトへリンクしています。

<table id="politicianTable" class="display" style="width:100%">
    <thead>
        <tr>
            <th>顔写真</th> <th>院</th>
            <th>氏名</th>
            <th>政党</th>
            <th>選挙区</th>
        </tr>
    </thead>
    <tbody>
        {% for p in site.data.politicians %}
        <tr>
            <td>{{ p.img_url }}</td> <td>{{ p.chamber }}</td>
            <td>{{ p.name }}</td>
            <td>{{ p.party }}</td>
            <td>{{ p.district }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<script>
$(document).ready(function() {
    $('#politicianTable').DataTable({
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.13.6/i18n/ja.json"
        },
        "pageLength": 50,
        "order": [[ 1, "desc" ]], // 院（2列目）でソート
        
        // 列の定義を設定
        "columnDefs": [
            {
                "targets": 0, // 1列目（顔写真）に対して設定
                "orderable": false, // ソート不可にする
                "searchable": false, // 検索対象外にする
                # データ（URL）を<img>タグに変換して表示
                "render": function ( data, type, row ) {
                    if (data) {
                        return '<img src="' + data + '" alt="顔写真" class="giin-photo" loading="lazy">';
                    } else {
                        return 'なし'; // 画像がない場合
                    }
                }
            }
        ]
    });
});
</script>

[⬅ ホームへ戻る](index.html)