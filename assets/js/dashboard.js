/* ============================================================
   政党名・グループ定義
   ============================================================ */
const rulingParties = ['自由民主党']; // 短縮名に合わせる

const partyColors = {
  '自由民主党':   '#3a5f8a',
  '中道改革連合': '#7a5c3a', // 立憲・公明を集約
  '日本維新の会': '#4a7c5f',
  '国民民主党':   '#5a5a7a',
  '参政党':       '#4a6a4a',
  'チームみらい': '#3a7a5a',
  '日本共産党':   '#7a3a4a',
  '社会民主党':   '#2a6b6b',
  'れいわ新選組': '#6a3a7a',
  '日本保守党':   '#7a5a3a',
  '沖縄の風':     '#3a7a6a',
  '無所属':       '#888780',
};

const fallbackColors = [
  '#3a5f8a','#4a7c5f','#8a6a2a','#7a5c3a','#5a5a7a',
  '#7a3a4a','#4a6a4a','#2a6b6b','#6a3a7a','#888780'
];

let activeHouse = null;
const chartInstances = {};

/**
 * 政党名の正規化
 * 1. 「・」以降を削除（無所属の会、無所属クラブなど）
 * 2. 「新緑風会」を削除
 * 3. 立憲・公明を「中道改革連合」へ集約
 */
function normalizeName(name) {
  if (!name) return "無所属";
  let n = name.split('・')[0].replace("新緑風会", "").trim();
  if (n.includes("立憲民主党") || n.includes("公明党")) {
    return "中道改革連合";
  }
  return n;
}

/**
 * グラフ描画前のデータ集計
 */
function normalizeData(rawData) {
  let normalized = {};
  for (let party in rawData) {
    let cleanName = normalizeName(party);
    normalized[cleanName] = (normalized[cleanName] || 0) + rawData[party];
  }
  return normalized;
}

function sortPartyData(obj) {
  const entries = Object.entries(obj);
  const ruling    = entries.filter(([l]) =>  rulingParties.includes(l)).sort((a,b) => b[1]-a[1]);
  const nonRuling = entries.filter(([l]) => !rulingParties.includes(l)).sort((a,b) => b[1]-a[1]);
  return [...ruling, ...nonRuling];
}

/* ── 中央文字プラグイン (サイズ強化版) ── */
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
      ctx.font      = `600 2.2rem 'Noto Serif JP', serif`;
      ctx.fillStyle = '#1a1410';
      ctx.fillText(total, cx, cy - 8);
      ctx.font      = `500 0.85rem 'Noto Sans JP', sans-serif`;
      ctx.fillStyle = '#5a5048';
      ctx.fillText('総議席', cx, cy + 22);
    } else {
      ctx.font      = `600 2.0rem 'Noto Serif JP', serif`;
      ctx.fillStyle = '#1a1410';
      ctx.fillText(selSeats, cx, cy - 15);
      ctx.font      = `300 0.6rem 'Noto Sans JP', sans-serif`;
      ctx.fillStyle = '#b0a090';
      ctx.fillText('───────', cx, cy + 2);
      ctx.font      = `500 1.0rem 'Noto Serif JP', serif`;
      ctx.fillStyle = '#3a2e22';
      ctx.fillText(total, cx, cy + 22);
    }
    ctx.restore();
  }
};
Chart.register(centerTextPlugin);

function renderChart(id, obj, houseKey) {
  const canvas = document.getElementById(id);
  if (!canvas || Object.keys(obj).length === 0) return;

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
        // rulingParties(自由民主党)に金枠を適用
        borderColor: labels.map(l => rulingParties.includes(l) ? '#9a6e28' : '#ffffff'),
        borderWidth: labels.map(l => rulingParties.includes(l) ? 4 : 1),
        hoverOffset: 12
      }]
    },
    options: {
      cutout: '68%',
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true }
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

  buildLegend(chart, id, houseKey, labels, values, bg);
}

function buildLegend(chart, canvasId, houseKey, labels, values, bg) {
  const cell = document.getElementById(canvasId).closest('.chart-cell');
  if (!cell) return;

  const existing = cell.querySelector('.chart-legend');
  if (existing) existing.remove();

  const legend = document.createElement('div');
  legend.className = 'chart-legend';

  labels.forEach((label, i) => {
    const item = document.createElement('div');
    item.className = 'chart-legend-item';
    
    const dot = document.createElement('span');
    dot.className = 'chart-legend-dot';
    dot.style.background = bg[i];
    
    if (rulingParties.includes(label)) {
      dot.classList.add('ruling-dot');
    }

    const text = document.createElement('span');
    text.textContent = `${label} ${values[i]}`;

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
  if (sel.has(idx)) {
    sel.delete(idx);
  } else {
    sel.add(idx);
  }
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
    sel.size === 0 || sel.has(i) ? c : c + '33'
  );
  chart.update();

  const canvas = chart.canvas;
  const cell = canvas.closest('.chart-cell');
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
        // テーブル内の生テキストも正規化して比較する
        const normalizedCell = normalizeName(partyCell);
        if (!parties.some(p => normalizedCell === p)) return false;
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
    $('#politicianTable').DataTable().draw();
  }
}

function setupDashboard(dataAll, dataSyu, dataSan) {
  // 描画・集計前にデータを正規化
  const normAll = normalizeData(dataAll);
  const normSyu = normalizeData(dataSyu);
  const normSan = normalizeData(dataSan);

  renderChart('chartAll', normAll, 'all');
  renderChart('chartSyu', normSyu, 'syu');
  renderChart('chartSan', normSan, 'san');

  $('#politicianTable').DataTable({
    language: { url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/ja.json' },
    pageLength: 100,
    dom: 'tip', 
    order: [[7, 'desc']], 
    columnDefs: [
      {
        targets: "_all",
        className: "dt-center" 
      },
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
      },
      { targets: [5, 6, 7], type: "num-fmt" }
    ]
  });
}