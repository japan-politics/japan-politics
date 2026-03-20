// 与党リスト（赤枠で強調）
const rulingParties = ['自民', '維新'];

// 和のカラーパレット
const partyColors = {
  '自民': '#9e2a1c',
  '公明': '#b5843a',
  '立憲': '#2d5c8a',
  '維新': '#3d6b4f',
  '国民': '#7a4f2d',
  '共産': '#6b3a5e',
  '参政': '#5a7a3a',
  '社民': '#2a6b6b',
  '無所属': '#888780',
  '無':   '#888780',
};
const fallbackColors = [
  '#9e2a1c','#3d6b4f','#b5843a','#2d5c8a','#7a4f2d',
  '#6b3a5e','#5a7a3a','#2a6b6b','#888780','#b0a090'
];

// データを「与党を先頭に、残りは議席数降順」に並び替える
function sortPartyData(obj) {
  const entries = Object.entries(obj);

  const ruling    = entries.filter(([l]) =>  rulingParties.includes(l))
                           .sort((a, b) => b[1] - a[1]);
  const nonRuling = entries.filter(([l]) => !rulingParties.includes(l))
                           .sort((a, b) => b[1] - a[1]);

  const sorted = [...ruling, ...nonRuling];
  return {
    labels: sorted.map(([l]) => l),
    values: sorted.map(([, v]) => v),
  };
}

function setupDashboard(dataAll, dataSyu, dataSan) {
  const renderChart = (id, obj) => {
    const canvas = document.getElementById(id);
    if (!canvas) return;
    if (Object.keys(obj).length === 0) return;

    const { labels, values } = sortPartyData(obj);
    const bgColors = labels.map((l, i) =>
      partyColors[l] || fallbackColors[i % fallbackColors.length]
    );

    new Chart(canvas, {
      type: 'doughnut',
      data: {
        labels,
        datasets: [{
          data: values,
          backgroundColor: bgColors,
          // 与党セグメントは赤枠、それ以外は背景色と同じ（境界を消す）
          borderColor: labels.map(l =>
            rulingParties.includes(l) ? '#c0392b' : '#f8f4ee'
          ),
          borderWidth: labels.map(l =>
            rulingParties.includes(l) ? 4 : 1
          ),
        }]
      },
      options: {
        cutout: '70%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              font: { family: "'Noto Sans JP', sans-serif", size: 10 },
              color: '#4a3f30',
              boxWidth: 10,
              padding: 8,
              pointStyle: 'rect',
              usePointStyle: true,
              // 凡例も与党を先頭にした並び順のまま表示される
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
          ? `<img src="${d}" class="giin-photo" loading="lazy" onerror="this.src='https://placehold.jp/24/d8d0c4/7a6e5f/48x62.png?text=写真'">`
          : `<div style="width:48px;height:62px;background:#e8e2d8;display:flex;align-items:center;justify-content:center;font-size:10px;color:#7a6e5f;font-family:'Noto Sans JP',sans-serif">写真</div>`
      },
      {
        targets: 1,
        render: d => `<span class="badge ${d === '衆議院' ? 'badge-shugiin' : 'badge-sangiin'}">${d}</span>`
      }
    ]
  });
}


function setupTable() {
  $('#politicianTable').DataTable({
    language: { url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/ja.json' },
    pageLength: 50,
    columnDefs: [
      {
        targets: 0,
        render: d => d
          ? `<img src="${d}" class="giin-photo" loading="lazy" onerror="this.src='https://placehold.jp/24/d8d0c4/7a6e5f/48x62.png?text=写真'">`
          : `<div style="width:48px;height:62px;background:#e8e2d8;display:flex;align-items:center;justify-content:center;font-size:10px;color:#7a6e5f;font-family:'Noto Sans JP',sans-serif">写真</div>`
      },
      {
        targets: 1,
        render: d => `<span class="badge ${d === '衆議院' ? 'badge-shugiin' : 'badge-sangiin'}">${d}</span>`
      }
    ]
  });
}