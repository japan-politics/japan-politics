const rulingParties = ['自由民主党', '日本維新の会'];

const partyColors = {
  '自由民主党':     '#3a5f8a',
  '日本維新の会':   '#4a7c5f',
  '立憲民主党':     '#7a5c3a',
  '立憲民主・無所属': '#8a7050',
  '公明党':         '#8a6a2a',
  '国民民主党':     '#5a5a7a',
  '日本共産党':     '#7a3a4a',
  '参政党':         '#4a6a4a',
  '社会民主党':     '#2a6b6b',
  'れいわ新選組':   '#6a3a7a',
  '有志の会':       '#5a6a3a',
  'みらいの風':     '#3a6a7a',
  '日本保守党':     '#7a5a3a',
  '沖縄の風':       '#3a7a6a',
  '無所属':         '#888780',
};
const fallbackColors = [
  '#3a5f8a','#4a7c5f','#8a6a2a','#7a5c3a','#5a5a7a',
  '#7a3a4a','#4a6a4a','#2a6b6b','#6a3a7a','#888780'
];

// 選択中の院（null=全体, 'syu'=衆議院, 'san'=参議院）
let activeHouse = null;
// 選択中の政党インデックス（チャートインスタンスごと）
const chartInstances = {};

function sortPartyData(obj) {
  const entries = Object.entries(obj);
  const ruling    = entries.filter(([l]) =>  rulingParties.includes(l)).sort((a,b) => b[1]-a[1]);
  const nonRuling = entries.filter(([l]) => !rulingParties.includes(l)).sort((a,b) => b[1]-a[1]);
  const sorted = [...ruling, ...nonRuling];
  return { labels: sorted.map(([l]) => l), values: sorted.map(([,v]) => v) };
}

// 円の中心テキストプラグイン
const centerTextPlugin = {
  id: 'centerText',
  afterDraw(chart) {
    const { ctx, chartArea: { top, bottom, left, right } } = chart;
    const cx = (left + right) / 2;
    const cy = (top + bottom) / 2;
    const selected = chart._selectedIndices || new Set();
    const values   = chart.data.datasets[0].data;
    const total    = values.reduce((s, v) => s + v, 0);
    let selSeats   = 0;
    selected.forEach(i => { selSeats += values[i] || 0; });

    ctx.save();
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    if (selected.size === 0) {
      ctx.font      = `500 1.35rem 'Noto Serif JP', serif`;
      ctx.fillStyle = '#2d2416';
      ctx.fillText(total, cx, cy - 7);
      ctx.font      = `300 0.6rem 'Noto Sans JP', sans-serif`;
      ctx.fillStyle = '#7a6e5f';
      ctx.fillText('総議席', cx, cy + 13);
    } else {
      ctx.font      = `500 1.25rem 'Noto Serif JP', serif`;
      ctx.fillStyle = '#2d2416';
      ctx.fillText(selSeats, cx, cy - 14);
      ctx.font      = `300 0.55rem 'Noto Sans JP', sans-serif`;
      ctx.fillStyle = '#b0a090';
      ctx.fillText('───────', cx, cy);
      ctx.font      = `400 0.75rem 'Noto Serif JP', serif`;
      ctx.fillStyle = '#4a3f30';
      ctx.fillText(total, cx, cy + 15);
    }
    ctx.restore();
  }
};
Chart.register(centerTextPlugin);

function renderChart(id, obj, houseKey) {
  const canvas = document.getElementById(id);
  if (!canvas) return;
  if (Object.keys(obj).length === 0) return;

  const { labels, values } = sortPartyData(obj);
  const bg = labels.map((l, i) => partyColors[l] || fallbackColors[i % fallbackColors.length]);

  const chart = new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: [...bg],
        borderColor: labels.map(l => rulingParties.includes(l) ? '#b5843a' : '#f8f4ee'),
        borderWidth: labels.map(l => rulingParties.includes(l) ? 4 : 1),
      }]
    },
    options: {
      cutout: '70%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            font: { family: "'Noto Sans JP', sans-serif", size: 10 },
            color: '#4a3f30', boxWidth: 10, padding: 8,
            pointStyle: 'rect', usePointStyle: true,
          },
          onClick(e, item, legend) {
            toggleSlice(legend.chart, item.index, houseKey);
          }
        }
      },
      onClick(e, elements) {
        if (!elements.length) return;
        toggleSlice(this, elements[0].index, houseKey);
      }
    }
  });

  chart._selectedIndices = new Set();
  chart._origBg = [...bg];
  chartInstances[houseKey] = chart;
}

function toggleSlice(chart, idx, houseKey) {
  // 院の切り替え（別の院のチャートをリセット）
  if (activeHouse !== null && activeHouse !== houseKey) {
    resetChart(activeHouse);
  }
  activeHouse = houseKey;

  const sel = chart._selectedIndices;
  sel.has(idx) ? sel.delete(idx) : sel.add(idx);
  updateChartColors(chart);

  // 選択された政党でテーブルを絞り込み
  const selectedParties = sel.size > 0
    ? [...sel].map(i => chart.data.labels[i])
    : null;
  filterTable(houseKey, selectedParties);

  // 選択が空になったらリセット
  if (sel.size === 0) {
    activeHouse = null;
    filterTable(null, null);
  }
}

function updateChartColors(chart) {
  const sel = chart._selectedIndices;
  const bg  = chart._origBg;
  chart.data.datasets[0].backgroundColor = bg.map((c, i) =>
    sel.size === 0 || sel.has(i) ? c : c + '44'
  );
  chart.update('none');
}

function resetChart(houseKey) {
  const chart = chartInstances[houseKey];
  if (!chart) return;
  chart._selectedIndices = new Set();
  updateChartColors(chart);
}

function filterTable(houseKey, parties) {
  if (!$.fn.DataTable.isDataTable('#politicianTable')) return;
  const table = $('#politicianTable').DataTable();

  // カスタム検索フィルタ（院名・政党）
  $.fn.dataTable.ext.search = [];
  if (houseKey || parties) {
    $.fn.dataTable.ext.search.push(function(settings, data) {
      const chamberCell = data[1] || ''; // 院名列（badge内のテキスト）
      const partyCell   = data[3] || ''; // 会派列

      // 院名フィルタ
      if (houseKey === 'syu' && !chamberCell.includes('衆議院')) return false;
      if (houseKey === 'san' && !chamberCell.includes('参議院')) return false;

      // 政党フィルタ
      if (parties && parties.length > 0) {
        if (!parties.some(p => partyCell.includes(p))) return false;
      }
      return true;
    });
  }
  table.draw();
}

// リセットボタン
function resetAll() {
  if (activeHouse) {
    resetChart(activeHouse);
    activeHouse = null;
  }
  // 全チャートリセット
  Object.keys(chartInstances).forEach(k => {
    chartInstances[k]._selectedIndices = new Set();
    updateChartColors(chartInstances[k]);
  });
  filterTable(null, null);
}

function setupDashboard(dataAll, dataSyu, dataSan) {
  renderChart('chartAll', dataAll, 'all');
  renderChart('chartSyu', dataSyu, 'syu');
  renderChart('chartSan', dataSan, 'san');

  $('#politicianTable').DataTable({
    language: { url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/ja.json' },
    pageLength: 100,
    columnDefs: [
      {
        targets: 0,
        render: d => d
          ? `<img src="${d}" class="giin-photo" loading="lazy" onerror="this.src='https://placehold.jp/24/d8d0c4/7a6e5f/48x62.png?text=写真'">`
          : `<div style="width:48px;height:62px;background:#e8e2d8;display:flex;align-items:center;justify-content:center;font-size:10px;color:#7a6e5f;font-family:'Noto Sans JP',sans-serif">写真</div>`
      },
      {
        targets: 1,
        render: d => d
          ? `<span class="badge ${d === '衆議院' ? 'badge-shugiin' : 'badge-sangiin'}">${d}</span>`
          : ''
      }
    ]
  });
}

function setupTable() {
  $('#politicianTable').DataTable({
    language: { url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/ja.json' },
    pageLength: 100,
    columnDefs: [
      {
        targets: 0,
        render: d => d
          ? `<img src="${d}" class="giin-photo" loading="lazy" onerror="this.src='https://placehold.jp/24/d8d0c4/7a6e5f/48x62.png?text=写真'">`
          : `<div style="width:48px;height:62px;background:#e8e2d8;display:flex;align-items:center;justify-content:center;font-size:10px;color:#7a6e5f;font-family:'Noto Sans JP',sans-serif">写真</div>`
      },
      {
        targets: 1,
        render: d => d
          ? `<span class="badge ${d === '衆議院' ? 'badge-shugiin' : 'badge-sangiin'}">${d}</span>`
          : ''
      }
    ]
  });
}