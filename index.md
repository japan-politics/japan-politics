---
layout: default
title: ホーム
---

# 議会勢力図

<div class="chart-grid">
  <div><h3 style="text-align:center">全議員</h3><div class="chart-container"><canvas id="chartAll"></canvas></div></div>
  <div><h3 style="text-align:center">衆議院</h3><div class="chart-container"><canvas id="chartSyu"></canvas></div></div>
  <div><h3 style="text-align:center">参議院</h3><div class="chart-container"><canvas id="chartSan"></canvas></div></div>
</div>

<div style="text-align:center; margin-top: 3rem;">
  <a href="list.html" style="background:#1a365d; color:white; padding:1rem 2rem; border-radius:8px; text-decoration:none; font-weight:bold;">👉 議員名簿（顔写真付）を見る</a>
</div>

{% assign all = site.data.politicians %}
{% assign syu = all | where: "chamber", "衆議院" %}
{% assign san = all | where: "chamber", "参議院" %}

<script>
const rulingParties = ['自民', '公明'];
const partyColors = { '自民': '#1e40af', '公明': '#0ea5e9', '立憲': '#2563eb', '中道': '#2563eb', '維新': '#10b981', '国民': '#f59e0b', '共産': '#ef4444', '無': '#94a3b8' };

function renderPie(id, dataObj) {
    const labels = Object.keys(dataObj);
    const data = Object.values(dataObj);
    const borderColors = labels.map(p => rulingParties.includes(p) ? '#ff0000' : '#ffffff');
    const borderWidths = labels.map(p => rulingParties.includes(p) ? 6 : 1);
    const bgColors = labels.map(p => partyColors[p] || '#cbd5e1');

    new Chart(document.getElementById(id), {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{ data: data, backgroundColor: bgColors, borderColor: borderColors, borderWidth: borderWidths }]
        },
        options: { plugins: { legend: { position: 'bottom' } } }
    });
}

// データの注入
renderPie('chartAll', { {% assign grp = all | group_by: "party" %}{% for g in grp %}'{{ g.name }}':{{ g.size }}{% unless forloop.last %},{% endunless %}{% endfor %} });
renderPie('chartSyu', { {% assign grp = syu | group_by: "party" %}{% for g in grp %}'{{ g.name }}':{{ g.size }}{% unless forloop.last %},{% endunless %}{% endfor %} });
renderPie('chartSan', { {% assign grp = san | group_by: "party" %}{% for g in grp %}'{{ g.name }}':{{ g.size }}{% unless forloop.last %},{% endunless %}{% endfor %} });
</script>