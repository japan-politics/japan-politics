/* assets/js/dashboard.js */
function setupDashboard() {
    $('#politicianTable').DataTable({
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.13.6/i18n/ja.json"
        },
        "pageLength": 50,
        "columnDefs": [
            {
                "targets": 0,
                "render": function(data) {
                    const fallback = 'https://placehold.jp/24/cccccc/ffffff/50x70.png?text=NoImage';
                    const src = (data && data.includes('http')) ? data : fallback;
                    return `<img src="${src}" class="giin-photo" loading="lazy" onerror="this.src='${fallback}'">`;
                }
            },
            {
                "targets": 1,
                "render": function(data) {
                    const cls = (data === '衆議院') ? 'badge-shugiin' : 'badge-sangiin';
                    return `<span class="badge ${cls}">${data}</span>`;
                }
            }
        ]
    });
}