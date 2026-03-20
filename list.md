---
layout: default
title: 議員一覧
---

{% include header.html %}

<div class="dashboard-container">
  <div class="section-block">
    <div class="section-header">
      <h2 class="section-title">議員名簿</h2>
      <p class="section-subtitle">国会議員一覧</p>
      <div class="section-mark"></div>
    </div>
    <table id="politicianTable" class="display">
      <thead>
        <tr>
          <th>写　真</th>
          <th>院　名</th>
          <th>氏　名</th>
          <th>会　派</th>
          <th>選挙区</th>
        </tr>
      </thead>
      <tbody>
        {% for p in site.data.politicians %}
        <tr>
          <td>{{ p.img_url }}</td>
          <td>{{ p.chamber }}</td>
          <td>{{ p.name }}</td>
          <td>{{ p.party }}</td>
          <td>{{ p.district }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>

<footer>
  日本の政治 ― 公式議会記録に基づくデータ
</footer>

<script>
$(document).ready(function() {
  setupTable();
});
</script>