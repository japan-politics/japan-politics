---
layout: default
title: ホーム
---

# 日本国会議員データベース

GitHub Actionsにより毎日自動更新される、衆議院・参議院の議員情報サイトです。

{% assign all = site.data.politicians %}
{% assign shugiin = all | where: "chamber", "衆議院" %}
{% assign sangiin = all | where: "chamber", "参議院" %}

## 議席数サマリ
* **全議員数**: {{ all.size }} 名
* **衆議院**: {{ shugiin.size }} 名
* **参議院**: {{ sangiin.size }} 名

## 衆議院：政党別人数
{% assign ldp_s = shugiin | where: "party", "自民" %}
{% assign cdp_s = shugiin | where: "party", "中道" %}
{% assign ishin_s = shugiin | where: "party", "維新" %}
* **自民**: {{ ldp_s.size }} 名
* **立憲（中道）**: {{ cdp_s.size }} 名
* **維新**: {{ ishin_s.size }} 名

## 参議院：政党別人数
{% assign ldp_c = sangiin | where: "party", "自民" %}
{% assign cdp_c = sangiin | where: "party", "立憲" %}
{% assign ishin_c = sangiin | where: "party", "維新" %}
* **自民**: {{ ldp_c.size }} 名
* **立憲**: {{ cdp_c.size }} 名
* **維新**: {{ ishin_c.size }} 名

[👉 全議員名簿を見る](list.html)