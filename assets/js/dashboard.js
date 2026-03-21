const rulingParties = ['自由民主党・無所属の会'];

const partyColors = {
  '自由民主党・無所属の会':  '#3a5f8a',
  '中道改革連合':            '#7a5c3a',
  '日本維新の会':            '#4a7c5f',
  '国民民主党・無所属クラブ':'#5a5a7a',
  '国民民主党・新緑風会':    '#5a5a7a',
  '参政党':                  '#4a6a4a',
  'チームみらい':            '#3a7a5a',
  '日本共産党':              '#7a3a4a',
  '社会民主党':              '#2a6b6b',
  'れいわ新選組':            '#6a3a7a',
  '日本保守党':              '#7a5a3a',
  '沖縄の風':                '#3a7a6a',
  '無所属':                  '#888780',
};
const fallbackColors = [
  '#3a5f8a','#4a7c5f','#8a6a2a','#7a5c3a','#5a5a7a',
  '#7a3a4a','#4a6a4a','#2a6b6b','#6a3a7a','#888780'
];

let activeHouse = null;
const chartInstances = {};

function sortPartyData(obj) {
  const entries = Object.entries(obj);
  const ruling    = entries.filter(([l]) =>  rulingParties.includes(l)).sort((a,b) => b[1]-a[1]);
  const nonRuling = entries.filter(([l]) => !rulingParties.includes(l)).sort((a,b) => b[1]-a[1]);
  return [...ruling, ...nonRuling];
}

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
      ctx.font      = `700 2rem 'Noto Serif JP', serif`;
      ctx.fillStyle = '#1a1410';
      ctx.fillText(total, cx, cy - 10);
      ctx.font      = `400 0.75rem 'Noto Sans JP', sans-serif`;
      ctx.fillStyle = '#5a5048';
      ctx.fillText('総議席', cx, cy + 16);
    } else {
      ctx.font      = `700 1.8rem 'Noto Serif JP', serif`;
      ctx.fillStyle = '#1a1410';
      ctx.fillText(selSeats, cx, cy - 18);
      ctx.font      = `300 0.62rem 'Noto Sans JP', sans-serif`;
      ctx.fillStyle = '#b0a090';
      ctx.fillText('───────', cx, cy + 2);
      ctx.font      = `500 0.9rem 'Noto Serif JP', serif`;
      ctx.fillStyle = '#3a2e22';
      ctx.fillText(total, cx, cy + 20);
    }
    ctx.restore();
  }
};
Chart.register(centerTextPlugin);

function renderChart(id, obj, houseKey) {
  const canvas = document.getElementById(id);
  if (!canvas) return;
  if (Object.keys(obj).length === 0) return;

  const sorted = sortPartyData(obj);
  const labels = sorted.map(([l]) => l);
  const values = sorted.map(([,v]) => v);
  const bg = labels.map((l, i) => partyColors[l] || fallbackColors[i % fallbackColors.length]);

  const chart = new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: [...bg],
        borderColor: labels.map(l => rulingParties.includes(l) ? '#9a6e28' : '#f8f4ee'),
        borderWidth: labels.map(l => rulingParties.includes(l) ? 4 : 1),
      }]
    },
    options: {
      cutout: '68%',
      plugins: {
        legend: { display: false }  // 組み込み凡例を非表示、カスタム凡例を使用
      },
      onClick(e, elements) {
        if (elements && elements.length > 0) {
          toggleSlice(this, elements[0].index, houseKey);
        }
      },
    }
  });

  chart._selectedIndices = new Set();
  chart._origBg = [...bg];
  chartInstances[houseKey] = chart;

  // カスタム2列凡例を描画
  buildLegend(chart, id, houseKey, labels, values, bg);
}

function buildLegend(chart, canvasId, houseKey, labels, values, bg) {
  // canvas の親の .chart-cell に凡例を追加
  const cell = document.getElementById(canvasId).closest('.chart-cell');
  if (!cell) return;

  // 既存の凡例を削除
  const existing = cell.querySelector('.chart-legend');
  if (existing) existing.remove();

  const legend = document.createElement('div');
  legend.className = 'chart-legend';

  labels.forEach((label, i) => {
    const item = document.createElement('div');
    item.className = 'chart-legend-item';
    item.style.cursor = 'pointer';

    const dot = document.createElement('span');
    dot.className = 'chart-legend-dot';
    dot.style.background = bg[i];
    if (rulingParties.includes(label)) {
      dot.style.outline = '2px solid #9a6e28';
      dot.style.outlineOffset = '1px';
    }

    const text = document.createElement('span');
    text.textContent = `${label}  ${values[i]}`;
    text.style.overflow = 'hidden';
    text.style.textOverflow = 'ellipsis';

    item.appendChild(dot);
    item.appendChild(text);
    item.addEventListener('click', () => toggleSlice(chart, i, houseKey));
    legend.appendChild(item);
  });

  cell.appendChild(legend);
}

function toggleSlice(chart, idx, houseKey) {
  if (activeHouse !== null && activeHouse !== houseKey) {
    resetChart(activeHouse);
  }
  activeHouse = houseKey;

  const sel = chart._selectedIndices;
  sel.has(idx) ? sel.delete(idx) : sel.add(idx);
  updateChartColors(chart);

  const selectedParties = sel.size > 0 ? [...sel].map(i => chart.data.labels[i]) : null;
  filterTable(houseKey, selectedParties);

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

  // カスタム凡例の透明度も更新
  const canvas = chart.canvas;
  if (!canvas) return;
  const cell = canvas.closest('.chart-cell');
  if (!cell) return;
  const items = cell.querySelectorAll('.chart-legend-item');
  items.forEach((item, i) => {
    item.style.opacity = sel.size === 0 || sel.has(i) ? '1' : '0.3';
  });
}

function resetChart(houseKey) {
  const chart = chartInstances[houseKey];
  if (!chart) return;
  chart._selectedIndices = new Set();
  updateChartColors(chart);
}

function filterTable(houseKey, parties) {
  if (!$.fn.DataTable.isDataTable('#politicianTable')) return;
  $.fn.dataTable.ext.search = [];
  if (houseKey || parties) {
    $.fn.dataTable.ext.search.push(function(settings, data) {
      const chamberCell = data[1] || '';
      const partyCell   = data[3] || '';
      if (houseKey === 'syu' && !chamberCell.includes('衆議院')) return false;
      if (houseKey === 'san' && !chamberCell.includes('参議院')) return false;
      if (parties && parties.length > 0) {
        if (!parties.some(p => partyCell.includes(p))) return false;
      }
      return true;
    });
  }
  $('#politicianTable').DataTable().draw();
}

function resetAll() {
  Object.keys(chartInstances).forEach(k => {
    chartInstances[k]._selectedIndices = new Set();
    updateChartColors(chartInstances[k]);
  });
  activeHouse = null;

  // DataTablesのカスタムフィルタを解除して再描画
  if ($.fn.DataTable.isDataTable('#politicianTable')) {
    $.fn.dataTable.ext.search = [];
    $('#politicianTable').DataTable().draw();
  }

  // 凡例の透明度を全てリセット
  document.querySelectorAll('.chart-legend-item').forEach(item => {
    item.style.opacity = '1';
  });
}

function setupDashboard(dataAll, dataSyu, dataSan) {
  renderChart('chartAll', dataAll, 'all');
  renderChart('chartSyu', dataSyu, 'syu');
  renderChart('chartSan', dataSan, 'san');

  $('#politicianTable').DataTable({
    language: { url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/ja.json' },
    pageLength: 100,
    dom: 'tip',  // デフォルトのlength・search・infoを非表示（カスタムに置き換え）
    columnDefs: [
      {
        targets: 0,
        orderable: false,
        render: d => d
          ? `<img src="${d}" class="giin-photo" loading="lazy" onerror="this.src='https://placehold.jp/24/d8d0c4/7a6e5f/52x68.png?text=写真'">`
          : `<div class="photo-placeholder">写真</div>`
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