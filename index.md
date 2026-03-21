---
layout: default
title: 日本の政治
---

<style>
  /* テーブル要素の完全中央寄せ */
  #politicianTable th, 
  #politicianTable td {
    text-align: center !important;
    vertical-align: middle !important;
  }

  /* 収支棒グラフのスタイリング */
  .balance-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    min-width: 140px;
  }
  .balance-bar-container {
    flex: 1;
    max-width: 60px;
    height: 8px;
    background: var(--rule);
    border-radius: 4px;
    overflow: hidden;
  }
  .balance-fill {
    height: 100%;
    transition: width 0.6s ease;
  }
  .balance-fill.positive { background-color: var(--moegi); } /* 緑 */
  .balance-fill.negative { background-color: var(--shu); }   /* 赤 */
  
  .balance-text {
    font-family: var(--sans);
    font-size: 0.82rem;
    font-weight: 600;
    width: 70px;
    text-align: right;
    font-variant-numeric: tabular-nums;
  }
  .text-plus { color: var(--moegi); }
  .text-minus { color: var(--shu); }
</style>

{% assign all = site.data.politicians %}
{% assign syu = all | where: "chamber", "衆議院" %}
{% assign san = all | where: "chamber", "参議院" %}
{% assign g_all = all | group_by: "party" %}
{% assign g_syu = syu | group_by: "party" %}
{% assign g_san = san | group_by: "party" %}

{% include header.html %}

<div class="dashboard-container">

  <div class="section-block">
    <div class="section-header">
      <h2 class="section-title">現在の議席配分</h2>
      <p class="section-subtitle">グラフをクリックして政党を選択</p>
      <div class="section-mark"></div>
    </div>
    <div class="chart-grid">
      <div class="chart-cell">
        <span class="chart-label chart-label-all">国　会</span>
        <canvas id="chartAll"></canvas>
      </div>
      <div class="chart-cell">
        <span class="chart-label chart-label-syu">衆議院</span>
        <canvas id="chartSyu"></canvas>
      </div>
      <div class="chart-cell">
        <span class="chart-label chart-label-san">参議院</span>
        <canvas id="chartSan"></canvas>
      </div>
    </div>
    <div style="text-align:center;margin-top:1.75rem;">
      <button onclick="resetAll()" class="reset-btn">選択をリセット</button>
    </div>
  </div>

  <div class="section-block">
    <div class="section-header">
      <h2 class="section-title">国会議員一覧</h2>
      <div class="section-mark"></div>
    </div>
    <div class="table-controls">
      <button onclick="resetAll()" class="reset-btn">選択をリセット</button>
      <div class="table-length-wrap">
        <select id="tableLengthSelect" class="form-input" style="width:auto;min-height:36px;padding:.3rem .6rem;font-size:.82rem;" onchange="$('#politicianTable').DataTable().page.len(this.value).draw()">
          <option value="25">25件表示</option>
          <option value="50">50件表示</option>
          <option value="100" selected>100件表示</option>
          <option value="-1">全件表示</option>
        </select>
      </div>
      <div class="table-search-wrap">
        <input type="search" id="tableSearch" class="form-input" style="width:180px;min-height:36px;padding:.3rem .7rem;font-size:.82rem;" placeholder="氏名・政党で検索"
          oninput="$('#politicianTable').DataTable().search(this.value).draw()">
      </div>
    </div>
    <table id="politicianTable" class="display">
      <thead>
        <tr>
          <th>写真</th><th>院名</th><th>氏名</th><th>会派</th><th>選挙区</th>
          <th>収入</th><th>支出</th><th>収支</th>
        </tr>
      </thead>
      <tbody>
        {% for p in site.data.politicians %}
        {% assign inc = p.income | default: 0 %}
        {% assign exp = p.expense | default: 0 %}
        {% assign bal = inc | minus: exp %}
        {% comment %} 1,000,000(100万)を100%としてバーの長さを計算 {% endcomment %}
        {% assign bar_width = bal | abs | times: 100 | divided_by: 1000000 | at_most: 100 %}
        <tr>
          <td>{{ p.img_url }}</td>
          <td>{{ p.chamber }}</td>
          <td data-sort="{{ p.yomi }}">{{ p.name }}<br><span class="yomi">{{ p.yomi }}</span></td>
          <td>{{ p.party }}</td>
          <td>{{ p.district }}</td>
          <td data-sort="{{ inc }}">{{ inc | number_with_delimiter }}</td>
          <td data-sort="{{ exp }}">{{ exp | number_with_delimiter }}</td>
          <td data-sort="{{ bal }}">
            <div class="balance-wrapper">
              <div class="balance-bar-container">
                <div class="balance-fill {% if bal >= 0 %}positive{% else %}negative{% endif %}" 
                     style="width: {{ bar_width }}%;"></div>
              </div>
              <span class="balance-text {% if bal >= 0 %}text-plus{% else %}text-minus{% endif %}">
                {% if bal > 0 %}+{% endif %}{{ bal | number_with_delimiter }}
              </span>
            </div>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

</div>

{% include footer.html %}

<script>
(function() {
  var all = {
    {% for i in g_all %}
    {{ i.name | jsonify }}: {{ i.size }}{% unless forloop.last %},{% endunless %}
    {% endfor %}
  };
  var syu = {
    {% for i in g_syu %}
    {{ i.name | jsonify }}: {{ i.size }}{% unless forloop.last %},{% endunless %}
    {% endfor %}
  };
  var san = {
    {% for i in g_san %}
    {{ i.name | jsonify }}: {{ i.size }}{% unless forloop.last %},{% endunless %}
    {% endfor %}
  };

  // DataTableのセットアップをカスタマイズ（setupDashboard内のDataTable呼び出し部分を想定）
  // 注意：外部JS内のsetupDashboardを呼び出しますが、DataTablesのtargets数が増えたため、
  // 外部JS側の targets: [5, 6, 7] 設定が重要になります。

  $(document).ready(function() {
    setupDashboard(all, syu, san);
  });
})();
</script>