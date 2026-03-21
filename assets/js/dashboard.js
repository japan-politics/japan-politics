const rulingParties = ['閾ｪ逕ｱ豌台ｸｻ蜈・, '譌･譛ｬ邯ｭ譁ｰ縺ｮ莨・];

const partyColors = {
  '閾ｪ逕ｱ豌台ｸｻ蜈・:       '#3a5f8a',
  '譌･譛ｬ邯ｭ譁ｰ縺ｮ莨・:     '#4a7c5f',
  '遶区・豌台ｸｻ蜈・:       '#7a5c3a',
  '遶区・豌台ｸｻ繝ｻ辟｡謇螻・: '#8a7050',
  '蜈ｬ譏主・':           '#8a6a2a',
  '蝗ｽ豌第ｰ台ｸｻ蜈・:       '#5a5a7a',
  '譌･譛ｬ蜈ｱ逕｣蜈・:       '#7a3a4a',
  '蜿よ帆蜈・:           '#4a6a4a',
  '遉ｾ莨壽ｰ台ｸｻ蜈・:       '#2a6b6b',
  '繧後＞繧乗眠驕ｸ邨・:     '#6a3a7a',
  '譛牙ｿ励・莨・:         '#5a6a3a',
  '縺ｿ繧峨＞縺ｮ鬚ｨ':       '#3a6a7a',
  '譌･譛ｬ菫晏ｮ亥・':       '#7a5a3a',
  '豐也ｸ・・鬚ｨ':         '#3a7a6a',
  '辟｡謇螻・:           '#888780',
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

// 蜃｡萓九ｂ隴ｰ蟶ｭ謨ｰ髯埼・↓荳ｦ縺ｹ繧九き繧ｹ繧ｿ繝繝励Λ繧ｰ繧､繝ｳ
// Chart.js縺ｮ蜃｡萓九・data鬆・↑縺ｮ縺ｧ縲《ortPartyData縺ｮ鬆・ｺ上′縺昴・縺ｾ縺ｾ蜿肴丐縺輔ｌ繧・

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
      ctx.font      = `600 1.4rem 'Noto Serif JP', serif`;
      ctx.fillStyle = '#1a1410';
      ctx.fillText(total, cx, cy - 8);
      ctx.font      = `400 0.68rem 'Noto Sans JP', sans-serif`;
      ctx.fillStyle = '#5a5048';
      ctx.fillText('邱剰ｭｰ蟶ｭ', cx, cy + 14);
    } else {
      ctx.font      = `600 1.3rem 'Noto Serif JP', serif`;
      ctx.fillStyle = '#1a1410';
      ctx.fillText(selSeats, cx, cy - 15);
      ctx.font      = `300 0.58rem 'Noto Sans JP', sans-serif`;
      ctx.fillStyle = '#b0a090';
      ctx.fillText('笏笏笏笏笏笏笏', cx, cy + 1);
      ctx.font      = `400 0.8rem 'Noto Serif JP', serif`;
      ctx.fillStyle = '#3a2e22';
      ctx.fillText(total, cx, cy + 17);
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
        legend: {
          position: 'bottom',
          align: 'start',        // 蟾ｦ謠・∴縺ｧ謨ｴ蛻・
          labels: {
            font: { family: "'Noto Sans JP', sans-serif", size: 11 },
            color: '#3a2e22',
            boxWidth: 12,
            boxHeight: 12,
            padding: 10,
            pointStyle: 'rect',
            usePointStyle: true,
            // 2蛻苓｡ｨ遉ｺ縺ｮ縺溘ａ譛螟ｧ蟷・ｒ蛻ｶ髯・
            generateLabels(chart) {
              const data = chart.data;
              return data.labels.map((label, i) => ({
                text: `${label}  ${data.datasets[0].data[i]}`,
                fillStyle: data.datasets[0].backgroundColor[i],
                strokeStyle: data.datasets[0].borderColor[i],
                lineWidth: data.datasets[0].borderWidth[i],
                index: i,
                hidden: false,
              }));
            }
          },
          onClick(e, item, legend) {
            toggleSlice(legend.chart, item.index, houseKey);
          }
        }
      },
      onClick(e, elements) {
        if (!elements.length) return;
        toggleSlice(this, elements[0].index, houseKey);
      },
      layout: { padding: { bottom: 8 } }
    }
  });

  chart._selectedIndices = new Set();
  chart._origBg = [...bg];
  chartInstances[houseKey] = chart;
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
      if (houseKey === 'syu' && !chamberCell.includes('陦・ｭｰ髯｢')) return false;
      if (houseKey === 'san' && !chamberCell.includes('蜿りｭｰ髯｢')) return false;
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
        orderable: false,
        render: d => d
          ? `<img src="${d}" class="giin-photo" loading="lazy" onerror="this.src='https://placehold.jp/24/d8d0c4/7a6e5f/52x68.png?text=蜀咏悄'">`
          : `<div class="photo-placeholder">蜀咏悄</div>`
      },
      {
        targets: 1,
        render: d => d
          ? `<span class="badge ${d === '陦・ｭｰ髯｢' ? 'badge-shugiin' : 'badge-sangiin'}">${d}</span>`
          : ''
      }
    ]
  });
},
    pageLength: 100,
    columnDefs: [
      {
        targets: 0,
        orderable: false,
        render: d => d
          ? `<img src="${d}" class="giin-photo" loading="lazy" onerror="this.src='https://placehold.jp/24/d8d0c4/7a6e5f/52x68.png?text=蜀咏悄'">`
          : `<div class="photo-placeholder">蜀咏悄</div>`
      },
      {
        targets: 1,
        render: d => d
          ? `<span class="badge ${d === '陦・ｭｰ髯｢' ? 'badge-shugiin' : 'badge-sangiin'}">${d}</span>`
          : ''
      }
    ]
  });
}