const rulingParties = ['自民', '維新'];

const partyColors = {
  '自民':   '#3a5f8a',  // 与党: 藍青
  '維新':   '#4a7c5f',  // 与党: 萌葱
  '立憲':   '#7a5c3a',  // 栗茶
  '公明':   '#8a6a2a',  // 金茶
  '国民':   '#5a5a7a',  // 青鼠
  '共産':   '#7a3a4a',  // 葡萄
  '参政':   '#4a6a4a',  // 苔色
  '社民':   '#2a6b6b',  // 青緑
  '無所属': '#888780',
  '無':     '#888780',
};
const fallbackColors = [
  '#3a5f8a','#4a7c5f','#8a6a2a','#7a5c3a','#5a5a7a',
  '#7a3a4a','#4a6a4a','#2a6b6b','#888780','#b0a090'
];

function sortPartyData(obj) {
  const entries = Object.entries(obj);
  const ruling    = entries.filter(([l]) =>  rulingParties.includes(l)).sort((a,b) => b[1]-a[1]);
  const nonRuling = entries.filter(([l]) => !rulingParties.includes(l)).sort((a,b) => b[1]-a[1]);
  const sorted = [...ruling, ...nonRuling];
  return { labels: sorted.map(([l]) => l), values: sorted.map(([,v]) => v) };
}

// 円の中心テキストを描画するカスタムプラグイン
const centerTextPlugin = {
  id: 'centerText',
  afterDraw(chart) {
    const { ctx, chartArea: { top, bottom, left, right } } = chart;
    const cx = (left + right) / 2;
    const cy = (top + bottom) / 2;

    const selected = chart._selectedIndices || new Set();
    const labels   = chart.data.labels;
    const values   = chart.data.datasets[0].data;
    const total    = values.reduce((s, v) => s + v, 0);

    let selSeats = 0;
    selected.forEach(i => { selSeats += values[i] || 0; });

    ctx.save();
    ctx.textAlign    = 'center';
    ctx.textBaseline = 'middle';

    if (selected.size === 0) {
      // 未選択: 総議席のみ
      ctx.font         = `500 1.45rem 'Noto Serif JP', serif`;
      ctx.fillStyle    = '#2d2416';
      ctx.fillText(total, cx, cy - 6);
      ctx.font         = `300 0.62rem 'Noto Sans JP', sans-serif`;
      ctx.fillStyle    = '#7a6e5f';
      ctx.fillText('総議席', cx, cy + 14);
    } else {
      // 選択中: 選択議席 / 総議席
      ctx.font         = `500 1.35rem 'Noto Serif JP', serif`;
      ctx.fillStyle    = '#2d2416';
      ctx.fillText(selSeats, cx, cy - 14);
      ctx.font         = `300 0.58rem 'Noto Sans JP', sans-serif`;
      ctx.fillStyle    = '#7a6e5f';
      ctx.fillText('─────', cx, cy + 1);
      ctx.font         = `400 0.78rem 'Noto Serif JP', serif`;
      ctx.fillStyle    = '#4a3f30';
      ctx.fillText(total, cx, cy + 16);
    }
    ctx.restore();
  }
};

Chart.register(centerTextPlugin);

function setupDashboard(dataAll, dataSyu, dataSan) {
  const renderChart = (id, obj) => {
    const canvas = document.getElementById(id);
    if (!canvas) return;
    if (Object.keys(obj).length === 0) return;

    const { labels, values } = sortPartyData(obj);
    const bgColors = labels.map((l, i) =>
      partyColors[l] || fallbackColors[i % fallbackColors.length]
    );
    const dimColors = bgColors.map(c => c + '55'); // 非選択時の薄い色

    const chart = new Chart(canvas, {
      type: 'doughnut',
      data: {
        labels,
        datasets: [{
          data: values,
          backgroundColor: bgColors,
          borderColor: labels.map(l =>
            rulingParties.includes(l) ? '#b5843a' : '#f8f4ee'
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
              boxWidth: 10, padding: 8,
              pointStyle: 'rect', usePointStyle: true,
            },
            onClick(e, legendItem, legend) {
              const idx     = legendItem.index;
              const chart   = legend.chart;
              const selected = chart._selectedIndices || (chart._selectedIndices = new Set());
              const ds       = chart.data.datasets[0];
              const bg       = chart._origBgColors;

              if (selected.has(idx)) {
                selected.delete(idx);
              } else {
                selected.add(idx);
              }

              // 選択状態に応じて色を更新
              ds.backgroundColor = bg.map((c, i) =>
                selected.size === 0 || selected.has(i) ? c : c + '44'
              );
              chart.update('none');
            }
          }
        },
        onClick(e, elements) {
          if (!elements.length) return;
          const idx      = elements[0].index;
          const chart    = this;
          const selected  = chart._selectedIndices || (chart._selectedIndices = new Set());
          const ds        = chart.data.datasets[0];
          const bg        = chart._origBgColors;

          if (selected.has(idx)) {
            selected.delete(idx);
          } else {
            selected.add(idx);
          }

          ds.backgroundColor = bg.map((c, i) =>
            selected.size === 0 || selected.has(i) ? c : c + '44'
          );
          chart.update('none');
        }
      }
    });

    // 元の色を保存
    chart._selectedIndices = new Set();
    chart._origBgColors    = [...bgColors];
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