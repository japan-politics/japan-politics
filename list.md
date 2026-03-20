---
layout: default
title: 衆議院議員一覧
---

# 衆議院議員一覧

CSVから自動生成された名簿です。

| 氏名 | 政党 | 選挙区 |
| :--- | :--- | :--- |
{% for p in site.data.politicians %}
| {{ p.name }} | {{ p.party }} | {{ p.district }} |
{% endfor %}

[トップへ戻る](index.html)