---
layout: default
title: 譌･譛ｬ縺ｮ謾ｿ豐ｻ
---

{% assign all = site.data.politicians %}
{% assign syu = all | where: "chamber", "陦・ｭｰ髯｢" %}
{% assign san = all | where: "chamber", "蜿りｭｰ髯｢" %}

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
      <h2 class="section-title">迴ｾ蝨ｨ縺ｮ隴ｰ蟶ｭ驟榊・</h2>
      <p class="section-subtitle">繧ｰ繝ｩ繝輔ｒ繧ｯ繝ｪ繝・け縺励※謾ｿ蜈壹ｒ驕ｸ謚・/p>
      <div class="section-mark"></div>
    </div>
    <div class="chart-grid">
      <div class="chart-cell">
        <span class="chart-label chart-label-all">蝗ｽ縲莨・/span>
        <canvas id="chartAll"></canvas>
      </div>
      <div class="chart-cell">
        <span class="chart-label chart-label-syu">陦・ｭｰ髯｢</span>
        <canvas id="chartSyu"></canvas>
      </div>
      <div class="chart-cell">
        <span class="chart-label chart-label-san">蜿りｭｰ髯｢</span>
        <canvas id="chartSan"></canvas>
      </div>
    </div>
    <div style="text-align:center;margin-top:1.75rem;">
      <button id="resetBtn" onclick="resetAll()" class="reset-btn">驕ｸ謚槭ｒ繝ｪ繧ｻ繝・ヨ</button>
    </div>
  </div>

  <div class="section-block">
    <div class="section-header">
      <h2 class="section-title">蝗ｽ莨夊ｭｰ蜩｡荳隕ｧ</h2>
      <div class="section-mark"></div>
    </div>
    <table id="politicianTable" class="display">
      <thead>
        <tr>
          <th>蜀咏悄</th>
          <th>髯｢蜷・/th>
          <th>豌丞錐繝ｻ縺ｵ繧翫′縺ｪ</th>
          <th>莨壽ｴｾ</th>
          <th>驕ｸ謖吝玄</th>
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

{% include footer.html %}

<script>
$(document).ready(function() {
  var el = document.getElementById('chart-data');
  var dataAll = JSON.parse(el.dataset.all);
  var dataSyu = JSON.parse(el.dataset.syu);
  var dataSan = JSON.parse(el.dataset.san);
  setupDashboard(dataAll, dataSyu, dataSan);
});
</script>