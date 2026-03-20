const rulingParties = ['自民', '公明'];
const partyColors = {
    '自民': '#1a365d', '公明': '#3182ce', '立憲': '#2b6cb0',
    '維新': '#38a169', '国民': '#d69e2e', '共産': '#e53e3e', '無': '#a0aec0'
};

function setupDashboard(dataAll, dataSyu, dataSan) {
    const renderChart = (id, obj) => {
        const canvas = document.getElementById(id);
        // 修正1: canvasが存在しない or データが空なら何もしない
        if (!canvas) return;
        const labels = Object.keys(obj);
        if (labels.length === 0) return;

        // 修正2: borderWidth に配列を渡すとChart.jsのバージョンによって
        //         無視されることがある → 与党のみ太枠にするため
        //         segment単位ではなくdataset全体の設定 + segment overrideで対応
        new Chart(canvas, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: Object.values(obj),
                    backgroundColor: labels.map(l => partyColors[l] || '#cbd5e1'),
                    // 修正2: borderColor/borderWidthは単一値にして、
                    //         与党のみ強調したい場合は segment で上書き
                    borderColor: '#fff',
                    borderWidth: 1,
                }]
            },
            options: {
                cutout: '75%',
                plugins: {
                    legend: { position: 'bottom' }
                },
                // 修正2: segment ごとに上書き（Chart.js v3.x以降で動作）
                elements: {
                    arc: {
                        borderColor: (ctx) => {
                            const label = ctx.chart.data.labels[ctx.dataIndex];
                            return rulingParties.includes(label) ? '#ff0000' : '#fff';
                        },
                        borderWidth: (ctx) => {
                            const label = ctx.chart.data.labels[ctx.dataIndex];
                            return rulingParties.includes(label) ? 5 : 1;
                        }
                    }
                }
            }
        });
    };

    renderChart('chartAll', dataAll);
    renderChart('chartSyu', dataSyu);
    renderChart('chartSan', dataSan);

    $('#politicianTable').DataTable({
        language: { url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/ja.json' },
        pageLength: 25,
        columnDefs: [
            {
                targets: 0,
                render: d => d
                    ? `<img src="${d}" class="giin-photo" loading="lazy" onerror="this.src='https://placehold.jp/24/ccc/fff/50x70.png?text=NoImage'">`
                    : 'なし'
            },
            {
                targets: 1,
                render: d => `<span class="badge ${d === '衆議院' ? 'badge-shugiin' : 'badge-sangiin'}">${d}</span>`
            }
        ]
    });
}