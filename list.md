---
layout: default
title: 議員一覧
---
<meta name="referrer" content="no-referrer">

<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>

<style>
/* 変数定義：信頼感のある濃紺をベースに */
:root {
    --primary-color: #1a365d;
    --border-color: #e2e8f0;
    --shugiin-color: #e53e3e; /* 衆議院：情熱・活気の朱 */
    --sangiin-color: #3182ce; /* 参議院：冷静・知性の青 */
}

/* テーブル全体のモダン化 */
#politicianTable {
    border-collapse: separate;
    border-spacing: 0;
    margin-top: 20px !important;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    overflow: hidden;
}

#politicianTable thead th {
    background-color: var(--primary-color) !important;
    color: white !important;
    font-weight: 600;
    padding: 15px 12px !important;
    border-bottom: none !important;
}

#politicianTable tbody td {
    padding: 12px !important;
    border-bottom: 1px solid var(--border-color);
    vertical-align: middle !important;
}

/* 顔写真のスタイリング：証明写真としての清潔感 */
.giin-photo {
    width: 60px;
    height: 75px;
    object-fit: cover;
    border-radius: 4px;
    border: 1px solid var(--border-color);
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    background-color: #f7fafc;
}

/* 院別バッジ：一目で所属を識別 */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: bold;
    color: white;
    white-space: nowrap;
}
.badge-shugiin { background-color: var(--shugiin-color); }
.badge-sangiin { background-color: var(--sangiin-color); }

/* DataTables 検索窓のデザイン調整 */
.dataTables_wrapper .dataTables_filter input {
    border: 1px solid var(--border-color) !important;
    border-radius: 6px !important;
    padding: 6px 12px !important;
    outline: none;
}
</style>

# 議員一覧

衆議院・参議院の全議員を網羅したデータベースです。各項目でのソートやリアルタイム検索が可能です。

<table id="politicianTable" class="display" style="width:100%">
    <thead>
        <tr>
            <th>顔写真</th>
            <th>院</th>
            <th>氏名</th>
            <th>政党</th>
            <th>選挙区</th>
        </tr>
    </thead>
    <tbody>
        {% for p in site.data.politicians %}
        <tr>
            <td>{{ p.img_url }}</td>
            <td>{{ p.chamber }}</td>
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
        "columnDefs": [
            {
                "targets": 0, // 顔写真列
                "orderable": false,
                "searchable": false,
                "render": function ( data, type, row ) {
                    if (data && data.length > 10) {
                        return '<img src="' + data + '" alt="顔写真" class="giin-photo" onerror="this.src=\'https://placehold.jp/24/cccccc/ffffff/50x70.png?text=なし\'" loading="lazy">';
                    } else {
                        return '<div class="giin-photo" style="display:flex;align-items:center;justify-content:center;font-size:10px;color:#999;">なし</div>';
                    }
                }
            },
            {
                "targets": 1, // 院の列をバッジ化
                "render": function ( data, type, row ) {
                    var badgeClass = (data === '衆議院') ? 'badge-shugiin' : 'badge-sangiin';
                    return '<span class="badge ' + badgeClass + '">' + data + '</span>';
                }
            }
        ]
    });
});
</script>

[⬅ ホームへ戻る](index.html)