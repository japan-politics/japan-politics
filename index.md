---
layout: default
title: ホーム
---

# 議会勢力ダッシュボード

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-top: 2rem;">
  <div class="card" style="text-align:center;">
    <h3>全議員 合計</h3>
    <canvas id="chartAll" style="max-height: 250px;"></canvas>
  </div>
  <div class="card" style="text-align:center;">
    <h3>衆議院</h3>
    <canvas id="chartSyu" style="max-height: 250px;"></canvas>
  </div>
  <div class="card" style="text-align:center;">
    <h3>参議院</h3>
    <canvas id="chartSan" style="max-height: 250px;"></canvas>
  </div>
</div>

<div style="text-align:center; margin-top: 3rem;">
  <a href="list.html" class="btn-primary">👉 詳細な議員一覧（顔写真付）を表示</a>
</div>

{% assign all = site.data.politicians %}
{% assign syu = all | where: "chamber", "衆議院" %}
{% assign san = all | where: "chamber", "参議院" %}

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const rulingParties = ['自民', '公明'];
const partyColors = { 
    '自民': '#1a365d', '公明': '#3182ce', '立憲': '#2b6cb0', 
    '維新': '#38a169', '国民': '#d69e2e', '共産': '#e53e3e', '無': '#a0aec0' 
};

function renderPie(id, dataObj) {
    const labels = Object.keys(dataObj);
    const data = Object.values(dataObj);
    if (data.length === 0) return;

    new Chart(document.getElementById(id), {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: labels.map(l => partyColors[l] || '#cbd5e1'),
                borderColor: labels.map(l => rulingParties.includes(l) ? '#ff0000' : '#ffffff'),
                borderWidth: labels.map(l => rulingParties.includes(l) ? 5 : 1)
            }]
        },
        options: { plugins: { legend: { position: 'bottom' } } }
    });
}

{% assign g_all = all | group_by: "party" %}
{% assign g_syu = syu | group_by: "party" %}
{% assign g_san = san | group_by: "party" %}

renderPie('chartAll', { {% for i in g_all %}'{{ i.name }}':{{ i.size }}{% unless forloop.last %},{% endunless %}{% endfor %} });
renderPie('chartSyu', { {% for i in g_syu %}'{{ i.name }}':{{ i.size }}{% unless forloop.last %},{% endunless %}{% endfor %} });
renderPie('chartSan', { {% for i in g_san %}'{{ i.name }}':{{ i.size }}{% unless forloop.last %},{% endunless %}{% endfor %} });
</script>