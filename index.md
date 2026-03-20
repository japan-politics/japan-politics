---
layout: default
title: ホーム
---

# 日本国会議員データベース（衆議院）

GitHub Actionsで毎日自動更新される政治家情報サイトです。

## 政党別・議席サマリ
{% assign all = site.data.politicians %}
{% assign ldp = all | where: "party", "自由民主党" %}
{% assign cdp = all | where: "party", "立憲民主党" %}
{% assign ishin = all | where: "party", "日本維新の会" %}

* **自由民主党**: {{ ldp.size }} 名
* **立憲民主党**: {{ cdp.size }} 名
* **日本維新の会**: {{ ishin.size }} 名
* **全体合計**: {{ all.size }} 名

[議員一覧を見る](list.html)