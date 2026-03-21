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

      <form class="contact-form" id="contactForm">
        <input type="hidden" name="access_key" value="142535ed-d4d0-4cc8-b468-b71ee8c58bc8">
        <input type="hidden" name="subject" value="【日本の政治】お問い合わせ">
        <input type="hidden" name="from_name" value="日本の政治 お問い合わせフォーム">
        <input type="checkbox" name="botcheck" style="display:none">

        <div class="form-group">
          <label class="form-label" for="name">お名前</label>
          <input class="form-input" type="text" id="name" name="name"
            placeholder="山田 太郎" required>
        </div>

        <div class="form-group">
          <label class="form-label" for="email">メールアドレス</label>
          <input class="form-input" type="email" id="email" name="email"
            placeholder="example@example.com" required>
        </div>

        <div class="form-group">
          <label class="form-label" for="category">件名</label>
          <select class="form-input" id="category" name="category" required>
            <option value="" disabled selected>選択してください</option>
            <option value="データの誤りについて">データの誤りについて</option>
            <option value="機能の要望">機能の要望</option>
            <option value="その他">その他</option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label" for="message">お問い合わせ内容</label>
          <textarea class="form-input form-textarea" id="message" name="message"
            rows="6" placeholder="お問い合わせ内容をご記入ください" required></textarea>
        </div>

        <div class="form-submit">
          <button type="submit" class="submit-btn" id="submitBtn">送信する</button>
        </div>

        <div id="formResult" class="form-result" style="display:none"></div>
      </form>
    </div>
  </div>
</div>

{% include footer.html %}

<script>
document.getElementById('contactForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  var btn = document.getElementById('submitBtn');
  var result = document.getElementById('formResult');
  btn.disabled = true;
  btn.textContent = '送信中...';
  result.style.display = 'none';

  var data = new FormData(this);
  try {
    var res = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      body: data
    });
    var json = await res.json();
    if (json.success) {
      result.className = 'form-result form-result--ok';
      result.textContent = 'お問い合わせを受け付けました。ありがとうございます。';
      result.style.display = 'block';
      this.reset();
    } else {
      throw new Error(json.message);
    }
  } catch(err) {
    result.className = 'form-result form-result--err';
    result.textContent = '送信に失敗しました。しばらく経ってから再度お試しください。';
    result.style.display = 'block';
  } finally {
    btn.disabled = false;
    btn.textContent = '送信する';
  }
});
</script>