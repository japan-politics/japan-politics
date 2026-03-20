---
layout: default
title: ホーム
---

# 議席占有率（政党別）

<div class="grid-3">
    <div>
        <h3 style="text-align:center">全議員</h3>
        <div class="chart-container"><canvas id="chartAll"></canvas></div>
    </div>
    <div>
        <h3 style="text-align:center">衆議院</h3>
        <div class="chart-container"><canvas id="chartSyu"></canvas></div>
    </div>
    <div>
        <h3 style="text-align:center">参議院</h3>
        <div class="chart-container"><canvas id="chartSan"></canvas></div>
    </div>
</div>

<div style="text-align:center; margin-top: 2rem;">
    [👉 詳細な議員一覧・検索はこちら]({{ '/list.html' | relative_url }}){: .btn }
</div>

{% assign all = site.data.politicians %}
{% comment %} 勢力データ生成 {% endcomment %}
<script>
const rulingParties = ['自民', '公明'];
const partyColors = {
    '自民': '#1e40af', '公明': '#0ea5e9', '立憲': '#2563eb', '中道': '#2563eb',
    '維新': '#10b981', '国民': '#f59e0b', '共産': '#ef4444', 'れいわ': '#ec4899', '無': '#94a3b8'
};

function createChart(id, rawData) {
    const labels = Object.keys(rawData);
    const data = Object.values(rawData);
    const borderColors = labels.map(p => rulingParties.includes(p) ? '#ff0000' : '#ffffff');
    const borderWidths = labels.map(p => rulingParties.includes(p) ? 5 : 1);
    const backgroundColors = labels.map(p => partyColors[p] || '#cbd5e1');

    new Chart(document.getElementById(id), {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: borderWidths
            }]
        },
        options: { plugins: { legend: { position: 'bottom' } } }
    });
}

{% assign syu = all | where: "chamber", "衆議院" %}
{% assign san = all | where: "chamber", "参議院" %}

// データの流し込み
createChart('chartAll', { 
    {% assign groups = all | group_by: "party" %}{% for g in groups %}'{{ g.name }}': {{ g.size }}{% unless forloop.last %},{% endunless %}{% endfor %}
});
createChart('chartSyu', {
    {% assign groups = syu | group_by: "party" %}{% for g in groups %}'{{ g.name }}': {{ g.size }}{% unless forloop.last %},{% endunless %}{% endfor %}
});
createChart('chartSan', {
    {% assign groups = san | group_by: "party" %}{% for g in groups %}'{{ g.name }}': {{ g.size }}{% unless forloop.last %},{% endunless %}{% endfor %}
});
</script>