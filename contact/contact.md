---
layout: default
title: お問い合わせ
---

{% include header.html %}

<div class="dashboard-container">
  <div class="section-block">
    <div class="section-header">
      <h2 class="section-title">お問い合わせ</h2>
      <div class="section-mark"></div>
    </div>

    <div class="contact-content">
      <p class="contact-lead">データの誤り・ご意見・ご要望などは以下のフォームよりお送りください。</p>

      <form class="contact-form" action="https://formsubmit.co/workaddress330@gmail.com" method="POST">
        <!-- FormSubmit の設定 -->
        <input type="hidden" name="_subject" value="【日本の政治】お問い合わせ">
        <input type="hidden" name="_language" value="ja">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_next" value="{{ '/' | absolute_url }}contact/thanks/">

        <div class="form-group">
          <label class="form-label" for="name">お名前</label>
          <input class="form-input" type="text" id="name" name="name" placeholder="山田 太郎" required>
        </div>

        <div class="form-group">
          <label class="form-label" for="email">メールアドレス</label>
          <input class="form-input" type="email" id="email" name="email" placeholder="example@example.com" required>
        </div>

        <div class="form-group">
          <label class="form-label" for="subject">件名</label>
          <select class="form-input" id="subject" name="subject" required>
            <option value="" disabled selected>選択してください</option>
            <option value="データの誤りについて">データの誤りについて</option>
            <option value="機能の要望">機能の要望</option>
            <option value="その他">その他</option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label" for="message">お問い合わせ内容</label>
          <textarea class="form-input form-textarea" id="message" name="message" rows="6" placeholder="お問い合わせ内容をご記入ください" required></textarea>
        </div>

        <div class="form-submit">
          <button type="submit" class="submit-btn">送信する</button>
        </div>
      </form>
    </div>
  </div>
</div>

{% include footer.html %}