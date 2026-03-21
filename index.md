・ｿ---
layout: default
title: 隴鯉ｽ･隴幢ｽｬ邵ｺ・ｮ隰ｾ・ｿ雎撰ｽｻ
---

{% assign all = site.data.politicians %}
{% assign syu = all | where: "chamber", "髯ｦ繝ｻ・ｭ・ｰ鬮ｯ・｢" %}
{% assign san = all | where: "chamber", "陷ｿ繧奇ｽｭ・ｰ鬮ｯ・｢" %}

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
      <h2 class="section-title">霑ｴ・ｾ陜ｨ・ｨ邵ｺ・ｮ髫ｴ・ｰ陝ｶ・ｭ鬩滓ｦ翫・</h2>
      <p class="section-subtitle">郢ｧ・ｰ郢晢ｽｩ郢晁ｼ費ｽ堤ｹｧ・ｯ郢晢ｽｪ郢昴・縺醍ｸｺ蜉ｱ窶ｻ隰ｾ・ｿ陷亥｣ｹ・帝ｩ包ｽｸ隰壹・/p>
      <div class="section-mark"></div>
    </div>
    <div class="chart-grid">
      <div class="chart-cell">
        <span class="chart-label chart-label-all">陜暦ｽｽ邵ｲﾂ闔ｨ繝ｻ/span>
        <canvas id="chartAll"></canvas>
      </div>
      <div class="chart-cell">
        <span class="chart-label chart-label-syu">髯ｦ繝ｻ・ｭ・ｰ鬮ｯ・｢</span>
        <canvas id="chartSyu"></canvas>
      </div>
      <div class="chart-cell">
        <span class="chart-label chart-label-san">陷ｿ繧奇ｽｭ・ｰ鬮ｯ・｢</span>
        <canvas id="chartSan"></canvas>
      </div>
    </div>
    <div style="text-align:center;margin-top:1.75rem;">
      <button id="resetBtn" onclick="resetAll()" class="reset-btn">鬩包ｽｸ隰壽ｧｭ・堤ｹ晢ｽｪ郢ｧ・ｻ郢昴・繝ｨ</button>
    </div>
  </div>

  <div class="section-block">
    <div class="section-header">
      <h2 class="section-title">陜暦ｽｽ闔ｨ螟奇ｽｭ・ｰ陷ｩ・｡闕ｳﾂ髫包ｽｧ</h2>
      <div class="section-mark"></div>
    </div>
    <table id="politicianTable" class="display">
      <thead>
        <tr>
          <th>陷蜥乗ｄ</th>
          <th>鬮ｯ・｢陷ｷ繝ｻ/th>
          <th>雎御ｸ樣倹郢晢ｽｻ邵ｺ・ｵ郢ｧ鄙ｫ窶ｲ邵ｺ・ｪ</th>
          <th>闔ｨ螢ｽ・ｴ・ｾ</th>
          <th>鬩包ｽｸ隰門雀邇・/th>
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