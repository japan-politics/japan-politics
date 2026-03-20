---
layout: default
title: 議員一覧
---

<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>

<style>
    #politicianTable_wrapper { margin-top: 2rem; }
    .giin-photo { width: 60px; height: 75px; object-fit: cover; border-radius: 4px; border: 1px solid #e2e8f0; }
    .badge { padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; color: white; }
    .badge-shugiin { background: #e53e3e; }
    .badge-sangiin { background: #3182ce; }
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
        "language": { "url": "https://cdn.datatables.net/plug-ins/1.13.6/i18n/ja.json" },
        "pageLength": 50,
        "columnDefs": [
            {
                "targets": 0,
                "render": function(data) {
                    return (data && data.includes('http')) ? 
                        '<img src="'+data+'" class="giin-photo" loading="lazy" onerror="this.style.display=\'none\'">' : 
                        '<div style="font-size:10px;color:#ccc;">No Image</div>';
                }
            },
            {
                "targets": 1,
                "render": function(data) {
                    var cls = (data === '衆議院') ? 'badge-shugiin' : 'badge-sangiin';
                    return '<span class="badge '+cls+'">'+data+'</span>';
                }
            }
        ]
    });
});
</script>