---
layout: default
title: 日本国会議員アーカイブ
---
<meta name="referrer" content="no-referrer">

<link rel="stylesheet" href="{{ '/assets/css/style.css' | relative_url }}">
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">

<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="{{ '/assets/js/dashboard.js' | relative_url }}"></script>

<div class="dashboard-container">
    <div class="card">
        <h2 class="section-title">議会勢力分析</h2>
        <div class="chart-grid">
            <div><strong style="display:block;text-align:center;">全議員合計</strong><canvas id="chartAll"></canvas></div>
            <div><strong style="display:block;text-align:center;color:#e53e3e;">衆議院</strong><canvas id="chartSyu"></canvas></div>
            <div><strong style="display:block;text-align:center;color:#3182ce;">参議院</strong><canvas id="chartSan"></canvas></div>
        </div>
    </div>

    <div class="card">
        <h2 class="section-title">議員データベース</h2>
        <table id="politicianTable" class="display" style="width:100%">
            <thead>
                <tr><th>顔写真</th><th>院</th><th>氏名</th><th>政党</th><th>選挙区</th></tr>
            </thead>
            <tbody>
                {% for p in site.data.politicians %}
                <tr><td>{{ p.img_url }}</td><td>{{ p.chamber }}</td><td>{{ p.name }}</td><td>{{ p.party }}</td><td>{{ p.district }}</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>

{% assign all = site.data.politicians %}
{% assign syu = all | where: "chamber", "衆議院" %}
{% assign san = all | where: "chamber", "参議院" %}

<script>
// JekyllのデータをJSに渡して実行
$(document).ready(function() {
    setupDashboard(
        { {% assign g = all | group_by: "party" %}{% for i in g %}'{{ i.name }}':{{ i.size }}{% unless forloop.last %},{% endunless %}{% endfor %} },
        { {% assign g = syu | group_by: "party" %}{% for i in g %}'{{ i.name }}':{{ i.size }}{% unless forloop.last %},{% endunless %}{% endfor %} },
        { {% assign g = san | group_by: "party" %}{% for i in g %}'{{ i.name }}':{{ i.size }}{% unless forloop.last %},{% endunless %}{% endfor %} }
    );
});
</script>