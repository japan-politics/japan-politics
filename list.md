---
layout: default
title: 議員一覧
---
<meta name="referrer" content="no-referrer">

<link rel="stylesheet" href="{{ '/assets/css/style.css' | relative_url }}">
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">

<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
<script src="{{ '/assets/js/dashboard.js' | relative_url }}"></script>

<div class="dashboard-container">
    <div class="card">
        <h2 class="section-title">議員データベース</h2>
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
    </div>
</div>

<script>
$(document).ready(function() {
    // 外部JSファイルに定義した初期化関数を呼び出し
    if (typeof setupDashboard === 'function') {
        setupDashboard();
    }
});
</script>