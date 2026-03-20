---
layout: default
title: 勢力図
---

<div class="card">
    <h2>議会勢力分析</h2>
    <p style="color: var(--text-sub); margin-bottom: 2rem;">各議院における政党別議席占有率のリアルタイム解析結果です。赤色の外枠は与党（自民・公明）を示します。</p>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 3rem;">
        <div style="text-align:center;">
            <strong style="display:block; margin-bottom:1rem;">全議員合計</strong>
            <canvas id="chartAll" style="max-width:280px; margin:0 auto;"></canvas>
        </div>
        <div style="text-align:center;">
            <strong style="display:block; margin-bottom:1rem;">衆議院</strong>
            <canvas id="chartSyu" style="max-width:280px; margin:0 auto;"></canvas>
        </div>
        <div style="text-align:center;">
            <strong style="display:block; margin-bottom:1rem;">参議院</strong>
            <canvas id="chartSan" style="max-width:280px; margin:0 auto;"></canvas>
        </div>
    </div>

    <div style="text-align:center; margin-top: 4rem;">
        <a href="list.html" class="btn-primary">詳細な議員名簿を確認する</a>
    </div>
</div>

{% assign all = site.data.politicians %}
{% assign syu = all | where: "chamber", "衆議院" %}
{% assign san = all | where: "chamber", "参議院" %}

<script>
const rulingParties = ['自民', '公明'];
const partyColors = { 
    '自民': '#1a365d', '公明': '#3182ce', '立憲': '#2b6cb0', 
    '維新': '#38a169', '国民': '#d69e2e', '共産': '#e53e3e', 
    'れいわ': '#d53f8c', '社民': '#e53e3e', '無': '#a0aec0' 
};

function initChart(id, dataObj) {
    const labels = Object.keys(dataObj);
    const data = Object.values(dataObj);
    
    new Chart(document.getElementById(id), {
        type: 'doughnut', // モダンな「ドーナツ型」を採用
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: labels.map(l => partyColors[l] || '#cbd5e1'),
                borderColor: labels.map(l => rulingParties.includes(l) ? '#ff0000' : '#ffffff'),
                borderWidth: labels.map(l => rulingParties.includes(l) ? 5 : 1),
                hoverOffset: 10
            }]
        },
        options: {
            cutout: '65%', // ドーナツの穴の大きさ
            plugins: {
                legend: { position: 'bottom', labels: { usePointStyle: true, padding: 20 } }
            }
        }
    });
}

{% assign g_all = all | group_by: "party" %}
{% assign g_syu = syu | group_by: "party" %}
{% assign g_san = san | group_by: "party" %}

initChart('chartAll', { {% for i in g_all %}'{{ i.name }}':{{ i.size }}{% unless forloop.last %},{% endunless %}{% endfor %} });
initChart('chartSyu', { {% for i in g_syu %}'{{ i.name }}':{{ i.size }}{% unless forloop.last %},{% endunless %}{% endfor %} });
initChart('chartSan', { {% for i in g_san %}'{{ i.name }}':{{ i.size }}{% unless forloop.last %},{% endunless %}{% endfor %} });
</script>