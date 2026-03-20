const rulingParties = ['自民', '公明'];
const partyColors = { '自民': '#1a365d', '公明': '#3182ce', '立憲': '#2b6cb0', '維新': '#38a169', '国民': '#d69e2e', '共産': '#e53e3e', '無': '#a0aec0' };

function setupDashboard(dataAll, dataSyu, dataSan) {
    const renderChart = (id, obj) => {
        const labels = Object.keys(obj);
        if (labels.length === 0) return;
        new Chart(document.getElementById(id), {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: Object.values(obj),
                    backgroundColor: labels.map(l => partyColors[l] || '#cbd5e1'),
                    borderColor: labels.map(l => rulingParties.includes(l) ? '#ff0000' : '#fff'),
                    borderWidth: labels.map(l => rulingParties.includes(l) ? 5 : 1)
                }]
            },
            options: { cutout: '75%', plugins: { legend: { position: 'bottom' } } }
        });
    };

    renderChart('chartAll', dataAll);
    renderChart('chartSyu', dataSyu);
    renderChart('chartSan', dataSan);

    $('#politicianTable').DataTable({
        "language": { "url": "https://cdn.datatables.net/plug-ins/1.13.6/i18n/ja.json" },
        "pageLength": 25,
        "columnDefs": [
            { "targets": 0, "render": d => d ? `<img src="${d}" class="giin-photo" loading="lazy" onerror="this.src='https://placehold.jp/24/ccc/fff/50x70.png?text=NoImage'">` : 'なし' },
            { "targets": 1, "render": d => `<span class="badge ${d==='衆議院'?'badge-shugiin':'badge-sangiin'}">${d}</span>` }
        ]
    });
}