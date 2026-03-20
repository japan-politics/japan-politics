---
layout: default
title: Home
---
<meta name="referrer" content="no-referrer">
<link rel="stylesheet" href="{{ '/assets/css/style.css' | relative_url }}">
<link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="{{ '/assets/js/dashboard.js' | relative_url }}"></script>
{% assign all = site.data.politicians %}
{% assign syu = all | where: "chamber", "衆議院" %}
{% assign san = all | where: "chamber", "参議院" %}
<div id="chart-data"
  data-all='{% assign g = all | group_by: "party" %}{ {% for i in g %}"{{ i.name | replace: '"', '\"' }}":{{ i.size }}{% unless forloop.last %},{% endunless %}{% endfor %} }'
  data-syu='{% assign g = syu | group_by: "party" %}{ {% for i in g %}"{{ i.name | replace: '"', '\"' }}":{{ i.size }}{% unless forloop.last %},{% endunless %}{% endfor %} }'
  data-san='{% assign g = san | group_by: "party" %}{ {% for i in g %}"{{ i.name | replace: '"', '\"' }}":{{ i.size }}{% unless forloop.last %},{% endunless %}{% endfor %} }'
  style="display:none">
</div>
<div class="dashboard-container">
    <div class="section-block">
        <h2 class="section-title">Parliamentary Strength Analysis</h2>
        <div class="chart-grid">
            <div><strong style="display:block;text-align:center;">NATIONAL DIET</strong><canvas id="chartAll"></canvas></div>
            <div><strong style="display:block;text-align:center;color:var(--wh-accent);">REPRESENTATIVES</strong><canvas id="chartSyu"></canvas></div>
            <div><strong style="display:block;text-align:center;color:var(--wh-blue);">COUNCILLORS</strong><canvas id="chartSan"></canvas></div>
        </div>
    </div>
    <div class="section-block">
        <h2 class="section-title">Official Registry of Members</h2>
        <table id="politicianTable" class="display">
            <thead>
                <tr><th>IMAGE</th><th>CHAMBER</th><th>NAME</th><th>PARTY</th><th>DISTRICT</th></tr>
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
    var el = document.getElementById('chart-data');
    var dataAll = JSON.parse(el.dataset.all);
    var dataSyu = JSON.parse(el.dataset.syu);
    var dataSan = JSON.parse(el.dataset.san);
    setupDashboard(dataAll, dataSyu, dataSan);
});