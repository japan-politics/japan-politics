---
layout: default
title: 日本の政治
---
<meta name="referrer" content="no-referrer">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
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

{% include header.html %}

<div class="dashboard-container">

  <div class="section-block">
    <div class="section-header">
      <h2 class="section-title">議席勢力分析</h2>
      <p class="section-subtitle">現在の議席配分 ― 国会</p>
      <div class="section-mark"></div>
    </div>
    <div class="chart-grid">
      <div class="chart-cell">
        <span class="chart-label chart-label-all">国　会</span>
        <canvas id="chartAll"></canvas>
      </div>
      <div class="chart-cell">
        <span class="chart-label chart-label-syu">衆議院</span>
        <canvas id="chartSyu"></canvas>
      </div>
      <div class="chart-cell">
        <span class="chart-label chart-label-san">参議院</span>
        <canvas id="chartSan"></canvas>
      </div>
    </div>
  </div>

  <div class="section-block">
    <div class="section-header">
      <h2 class="section-title">議員名簿</h2>
      <p class="section-subtitle">国会議員一覧</p>
      <div class="section-mark"></div>
    </div>
    <table id="politicianTable" class="display">
      <thead>
        <tr>
          <th>写　真</th>
          <th>院　名</th>
          <th>氏　名</th>
          <th>会　派</th>
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

<footer>
  日本の政治 ― 公式議会記録に基づくデータ
</footer>

<script>
$(document).ready(function() {
  var el = document.getElementById('chart-data');
  var dataAll = JSON.parse(el.dataset.all);
  var dataSyu = JSON.parse(el.dataset.syu);
  var dataSan = JSON.parse(el.dataset.san);
  setupDashboard(dataAll, dataSyu, dataSan);
});
</script>