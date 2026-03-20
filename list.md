---
layout: default
title: 議員一覧
---
<meta name="referrer" content="no-referrer">

<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>

<style>
.giin-photo {
    width: 60px;
    height: auto;
    border-radius: 4px;
    border: 1px solid #eee;
    background-color: #f9f9f9;
}
#politicianTable td { vertical-align: middle; }
</style>

# 議員一覧

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
        "order": [[ 1, "desc" ]],
        "columnDefs": [
            {
                "targets": 0,
                "orderable": false,
                "searchable": false,
                "render": function ( data, type, row ) {
                    if (data && data.length > 10) {
                        return '<img src="' + data + '" alt="顔写真" class="giin-photo" onerror="this.src=\'https://placehold.jp/24/cccccc/ffffff/50x70.png?text=なし\'" loading="lazy">';
                    } else {
                        return 'なし';
                    }
                }
            }
        ]
    });
});
</script>