function externalTooltip(context) {
  const { chart, tooltip } = context;
  const cell = chart.canvas.closest('.chart-cell');
  if (!cell) return;

  let tip = cell.querySelector('.chart-tooltip-ext');
  if (!tip) {
    tip = document.createElement('div');
    tip.className = 'chart-tooltip-ext';
    cell.style.position = 'relative';
    cell.appendChild(tip);
  }

  if (tooltip.opacity === 0) {
    tip.style.opacity = '0';
    return;
  }

  const dataIndex = tooltip.dataPoints[0].dataIndex;
  const label     = tooltip.dataPoints[0].label;
  const value     = tooltip.dataPoints[0].parsed;
  const color     = chart.data.datasets[0].backgroundColor[dataIndex];

  tip.innerHTML = `<span style="display:inline-block;width:8px;height:8px;border-radius:1px;background:${color};margin-right:5px;vertical-align:middle;"></span>${label}：${value} 議席`;
  tip.style.opacity = '1';
}

const rulingParties = ['自由民主党', '日本維新の会'];

const partyColors = {
  '自由民主党':   '#2e5c96',
  '日本維新の会': '#2e7a52',
  '中道改革連合': '#8c5a28',
  '立憲民主党':   '#6b3a28',
  '国民民主党':   '#4a4a7a',
  '参政党':       '#3a6a4a',
  'チームみらい': '#1e6b7a',
  '日本共産党':   '#7a2a3a',
  'れいわ新選組': '#5a2a7a',
  '社会民主党':   '#2a5a5a',
  '日本保守党':   '#6a4a2a',
  '沖縄の風':     '#2a6a5a',
  '無所属':       '#7a7870',
};

const fallbackColors = [
  '#3a5f8a','#4a7c5f','#8a6a2a','#7a5c3a','#5a5a7a',
  '#7a3a4a','#4a6a4a','#2a6b6b','#6a3a7a','#888780'
];

let activeHouse = null;
const chartInstances = {};

function sortPartyData(obj) {
  const rulingOrder = ['自由民主党', '日本維新の会'];
  const ruling = rulingOrder
    .filter(p => obj[p] !== undefined)
    .map(p => [p, obj[p]]);
  const nonRuling = Object.entries(obj)
    .filter(([l]) => !rulingParties.includes(l))
    .sort((a, b) => b[1] - a[1]);
  return [...ruling, ...nonRuling];
}

const centerTextPlugin = {
  id: 'centerText',
  afterDraw(chart) {
    const { ctx, chartArea: { top, bottom, left, right } } = chart;
    const cx = (left + right) / 2;
    const cy = (top + bottom) / 2;
    const r  = Math.min(right - left, bottom - top) / 2;
    const selected = chart._selectedIndices || new Set();
    const values   = chart.data.datasets[0].data;
    const total    = values.reduce((s, v) => s + v, 0);
    let selSeats   = 0;
    selected.forEach(i => { selSeats += values[i] || 0; });

    const fs  = Math.max(13, Math.round(r * 0.26));
    const sub = Math.max(10, Math.round(r * 0.12));

    ctx.save();
    ctx.textAlign    = 'center';
    ctx.textBaseline = 'middle';

    if (selected.size === 0) {
      ctx.font      = `700 ${fs}px 'Noto Serif JP', serif`;
      ctx.fillStyle = '#1a1410';
      ctx.fillText(total, cx, cy - sub * 0.5);
      ctx.font      = `400 ${sub}px 'Noto Sans JP', sans-serif`;
      ctx.fillStyle = '#5a5048';
      ctx.fillText('総議席', cx, cy + sub * 1.5);
    } else {
      ctx.font      = `700 ${Math.round(fs * 0.9)}px 'Noto Serif JP', serif`;
      ctx.fillStyle = '#1a1410';
      ctx.fillText(selSeats, cx, cy - sub * 1.2);
      ctx.font      = `300 ${Math.round(sub * 0.85)}px 'Noto Sans JP', sans-serif`;
      ctx.fillStyle = '#c0b0a0';
      ctx.fillText('──────', cx, cy + sub * 0.2);
      ctx.font      = `500 ${sub}px 'Noto Serif JP', serif`;
      ctx.fillStyle = '#3a2e22';
      ctx.fillText(total, cx, cy + sub * 1.8);
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
  const values = sorted.map(([, v]) => v);
  const bg = labels.map((l, i) => partyColors[l] || fallbackColors[i % fallbackColors.length]);

  // canvasサイズをHTML属性で固定（CSS上書きによる座標ズレを防ぐ）
  canvas.width  = 260;
  canvas.height = 260;
  canvas.style.width  = '260px';
  canvas.style.height = '260px';

  const chart = new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: [...bg],
        borderColor:  labels.map(l => rulingParties.includes(l) ? '#f0a830' : 'rgba(248,244,238,0.6)'),
        borderWidth:  labels.map(l => rulingParties.includes(l) ? 7 : 1),
        hoverOffset:  0,
        hoverBorderWidth: 2,
        hoverBorderColor: '#d8d0c4',
      }]
    },
    options: {
      responsive: false,
      cutout: '60%',
      plugins: {
        legend: { display: false },
        tooltip: {
          enabled: false,
          external: externalTooltip,
        }
      },
      onClick(e, elements) {
        if (elements && elements.length > 0) {
          toggleSlice(this, elements[0].index, houseKey);
        }
      },
      onHover(e, elements) {
        e.native.target.style.cursor = (elements && elements.length > 0) ? 'pointer' : 'default';
      },
    }
  });

  chart._selectedIndices = new Set();
  chart._origBg = [...bg];
  chartInstances[houseKey] = chart;

  buildLegend(chart, id, houseKey, labels, values, bg);
}

function buildLegend(chart, canvasId, houseKey, labels, values, bg) {
  const cell = document.getElementById(canvasId).closest('.chart-cell');
  if (!cell) return;

  // 既存の凡例ラッパーを全て削除してから再生成
  cell.querySelectorAll('.chart-legend-wrap').forEach(el => el.remove());

  const wrap = document.createElement('div');
  wrap.className = 'chart-legend-wrap';

  const legend = document.createElement('div');
  legend.className = 'chart-legend';
  wrap.appendChild(legend);

  labels.forEach((label, i) => {
    const ruling = rulingParties.includes(label);
    const item   = document.createElement('div');
    item.className = 'chart-legend-item';
    item.style.cursor = 'pointer';
    if (ruling) {
      item.style.background    = 'rgba(181,132,58,.10)';
      item.style.borderRadius  = '2px';
      item.style.padding       = '1px 3px';
      item.style.margin        = '-1px -3px';
    }

    const dot = document.createElement('span');
    dot.className = 'chart-legend-dot';
    dot.style.background = bg[i];
    if (ruling) {
      dot.style.outline       = '2px solid #9a6e28';
      dot.style.outlineOffset = '1px';
    }

    const name = document.createElement('span');
    name.className   = 'chart-legend-name';
    name.textContent = label;

    const count = document.createElement('span');
    count.className   = 'chart-legend-count';
    count.textContent = values[i];

    item.appendChild(dot);
    item.appendChild(name);
    item.appendChild(count);
    item.addEventListener('click', () => toggleSlice(chart, i, houseKey));
    legend.appendChild(item);
  });

  cell.appendChild(wrap);
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

  const canvas = chart.canvas;
  if (!canvas) return;
  const cell = canvas.closest('.chart-cell');
  if (!cell) return;
  cell.querySelectorAll('.chart-legend-item').forEach((item, i) => {
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
  if ($.fn.DataTable.isDataTable('#politicianTable')) {
    $.fn.dataTable.ext.search = [];
    $('#politicianTable').DataTable().search('').draw();
  }
  // 検索窓をクリア
  const searchInput = document.querySelector('input[type="search"]');
  if (searchInput) searchInput.value = '';
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
    dom: 'tip',
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