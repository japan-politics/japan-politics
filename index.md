---
layout: default
title: 日本の政治
---

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
        <div class="chart-canvas-wrap"><canvas id="chartAll"></canvas></div>
      </div>
      <div class="chart-cell">
        <span class="chart-label chart-label-syu">衆議院</span>
        <div class="chart-canvas-wrap"><canvas id="chartSyu"></canvas></div>
      </div>
      <div class="chart-cell">
        <span class="chart-label chart-label-san">参議院</span>
        <div class="chart-canvas-wrap"><canvas id="chartSan"></canvas></div>
      </div>
    </div>
    <div style="text-align:center;margin-top:2.5rem;">
      <button onclick="resetAll()" class="reset-btn">選択をリセット</button>
    </div>
  </div>

  <div class="section-block">
    <div class="section-header">
      <h2 class="section-title">国会議員一覧</h2>
      <div class="section-mark"></div>
    </div>
    
    <table id="politicianTable" class="display">
      <thead>
        <tr>
          <th>写真</th>
          <th>院名</th>
          <th>氏名</th>
          <th>政党</th>
          <th>選挙区</th>
          <th>収入</th>
          <th>支出</th>
          <th>収支</th>
        </tr>
      </thead>
      <tbody>
        {% for p in site.data.politicians %}
          {% comment %} 1. 政党名の正規化ロジック（Liquid版） {% endcomment %}
          {% assign p_raw = p.party | default: "無所属" %}
          {% assign p_clean = p_raw | split: "・" | first | replace: "新緑風会", "" %}
          
          {% if p_clean contains "立憲民主党" or p_clean contains "公明党" %}
            {% assign display_party = "中道改革連合" %}
          {% else %}
            {% assign display_party = p_clean %}
          {% endif %}

          {% comment %} 収支計算 {% endcomment %}
          {% assign inc = p.income | default: 0 %}
          {% assign exp = p.expense | default: 0 %}
          {% assign bal = inc | minus: exp %}
          {% assign bar_width = bal | abs | times: 100 | divided_by: 1000000 | at_most: 100 %}

          <tr>
            <td>{{ p.img_url }}</td>
            <td>{{ p.chamber }}</td>
            <td data-sort="{{ p.yomi }}">
              {{ p.name }}<br><span class="yomi">{{ p.yomi }}</span>
            </td>
            <td>{{ display_party }}</td>
            <td>{{ p.district }}</td>
            <td data-sort="{{ inc }}">{{ inc | number_with_delimiter }}</td>
            <td data-sort="{{ exp }}">{{ exp | number_with_delimiter }}</td>
            <td data-sort="{{ bal }}">
              <div class="balance-wrapper">
                <div class="balance-bar-container">
                  <div class="balance-fill {% if bal >= 0 %}positive{% else %}negative{% endif %}" style="width: {{ bar_width }}%;"></div>
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

<script>
(function() {
  /**
   * JS側：政党名のクリーンアップ関数
   * 1. 「・」以降を削除
   * 2. 立憲・公明を統合
   * 3. 特定の文字列を削除
   */
  function normalizeName(name) {
    if (!name) return "無所属";
    let n = name.split('・')[0].replace("新緑風会", "").trim();
    if (n.includes("立憲民主党") || n.includes("公明党")) {
      return "中道改革連合";
    }
    return n;
  }

  function aggregateData(rawData) {
    let normalized = {};
    for (let party in rawData) {
      let cleanName = normalizeName(party);
      normalized[cleanName] = (normalized[cleanName] || 0) + rawData[party];
    }
    return normalized;
  }

  // Jekyllから渡される生データ
  var rawAll = { {% for i in g_all %}{{ i.name | jsonify }}: {{ i.size }}{% unless forloop.last %},{% endunless %}{% endfor %} };
  var rawSyu = { {% for i in g_syu %}{{ i.name | jsonify }}: {{ i.size }}{% unless forloop.last %},{% endunless %}{% endfor %} };
  var rawSan = { {% for i in g_san %}{{ i.name | jsonify }}: {{ i.size }}{% unless forloop.last %},{% endunless %}{% endfor %} };

  $(document).ready(function() {
    // データをクリーンな名称で集約してからダッシュボードを起動
    setupDashboard(
      aggregateData(rawAll), 
      aggregateData(rawSyu), 
      aggregateData(rawSan)
    );
  });
})();
</script>