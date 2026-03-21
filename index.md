---
layout: default
title: 日本の政治
---

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
      <h2 class="section-title">現在の議席配分</h2>
      <p class="section-subtitle">グラフをクリックして政党を選択 ― 一覧に反映されます</p>
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
    <div style="text-align:center;margin-top:1.75rem;">
      <button id="resetBtn" onclick="resetAll()" class="reset-btn">選択をリセット</button>
    </div>
  </div>

  <div class="section-block">
    <div class="section-header">
      <h2 class="section-title">国会議員一覧</h2>
      <p class="section-subtitle">衆議院・参議院 全議員</p>
      <div class="section-mark"></div>
    </div>
    <table id="politicianTable" class="display">
      <thead>
        <tr>
          <th>写真</th>
          <th>院名</th>
          <th>氏名・ふりがな</th>
          <th>会派</th>
          <th>選挙区</th>
        </tr>
      </thead>
      <tbody>
        {% for p in site.data.politicians %}
        <tr>
          <td>{{ p.img_url }}</td>
          <td>{{ p.chamber }}</td>
          <td data-sort="{{ p.yomi }}">{{ p.name }}<br><span class="yomi">{{ p.yomi }}</span></td>
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