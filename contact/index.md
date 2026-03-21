・ｿ---
layout: default
title: 邵ｺ髮∵牒邵ｺ繝ｻ邊狗ｹｧ荳岩雷
---

{% include header.html %}

<div class="dashboard-container">
  <div class="section-block">
    <div class="section-header">
      <h2 class="section-title">邵ｺ髮∵牒邵ｺ繝ｻ邊狗ｹｧ荳岩雷</h2>
      <div class="section-mark"></div>
    </div>

    <div class="contact-content">
      <p class="contact-lead">郢昴・繝ｻ郢ｧ・ｿ邵ｺ・ｮ髫ｱ・､郢ｧ鄙ｫ繝ｻ邵ｺ逍ｲﾑ埼囎荵昴・邵ｺ遒托ｽｦ竏ｵ謔咲ｸｺ・ｪ邵ｺ・ｩ邵ｺ・ｯ闔会ｽ･闕ｳ荵昴・郢晁ｼ斐°郢晢ｽｼ郢晢｣ｰ郢ｧ蛹ｻ・顔ｸｺ莨・竏夲ｽ顔ｸｺ荳岩味邵ｺ霈費ｼ樒ｸｲ繝ｻ/p>

      <form class="contact-form" id="contactForm">
        <input type="hidden" name="access_key" value="142535ed-d4d0-4cc8-b468-b71ee8c58bc8">
        <input type="hidden" name="subject" value="邵ｲ蜈亥ｾ玖ｭ幢ｽｬ邵ｺ・ｮ隰ｾ・ｿ雎撰ｽｻ邵ｲ莉｣笙陜荳奇ｼ櫁惺蛹ｻ・冗ｸｺ繝ｻ>
        <input type="hidden" name="from_name" value="隴鯉ｽ･隴幢ｽｬ邵ｺ・ｮ隰ｾ・ｿ雎撰ｽｻ 邵ｺ髮∵牒邵ｺ繝ｻ邊狗ｹｧ荳岩雷郢晁ｼ斐°郢晢ｽｼ郢晢｣ｰ">
        <input type="checkbox" name="botcheck" style="display:none">

        <div class="form-group">
          <label class="form-label" for="name">邵ｺ髮・倹陷代・/label>
          <input class="form-input" type="text" id="name" name="name"
            placeholder="陞ｻ・ｱ騾包ｽｰ 陞滂ｽｪ鬩帙・ required>
        </div>

        <div class="form-group">
          <label class="form-label" for="email">郢晢ｽ｡郢晢ｽｼ郢晢ｽｫ郢ｧ・｢郢晏ｳｨﾎ樒ｹｧ・ｹ</label>
          <input class="form-input" type="email" id="email" name="email"
            placeholder="example@example.com" required>
        </div>

        <div class="form-group">
          <label class="form-label" for="category">闔会ｽｶ陷ｷ繝ｻ/label>
          <select class="form-input" id="category" name="category" required>
            <option value="" disabled selected>鬩包ｽｸ隰壽ｧｭ・邵ｺ・ｦ邵ｺ荳岩味邵ｺ霈費ｼ・/option>
            <option value="郢昴・繝ｻ郢ｧ・ｿ邵ｺ・ｮ髫ｱ・､郢ｧ鄙ｫ竊鍋ｸｺ・､邵ｺ繝ｻ窶ｻ">郢昴・繝ｻ郢ｧ・ｿ邵ｺ・ｮ髫ｱ・､郢ｧ鄙ｫ竊鍋ｸｺ・､邵ｺ繝ｻ窶ｻ</option>
            <option value="隶匁ｺｯ繝ｻ邵ｺ・ｮ髫補扱謔・>隶匁ｺｯ繝ｻ邵ｺ・ｮ髫補扱謔・/option>
            <option value="邵ｺ譏ｴ繝ｻ闔峨・>邵ｺ譏ｴ繝ｻ闔峨・/option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label" for="message">邵ｺ髮∵牒邵ｺ繝ｻ邊狗ｹｧ荳岩雷陷繝ｻ・ｮ・ｹ</label>
          <textarea class="form-input form-textarea" id="message" name="message"
            rows="6" placeholder="邵ｺ髮∵牒邵ｺ繝ｻ邊狗ｹｧ荳岩雷陷繝ｻ・ｮ・ｹ郢ｧ蛛ｵ・・坎莨懊・邵ｺ荳岩味邵ｺ霈費ｼ・ required></textarea>
        </div>

        <div class="form-submit">
          <button type="submit" class="submit-btn" id="submitBtn">鬨ｾ竏ｽ・ｿ・｡邵ｺ蜷ｶ・・/button>
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
  btn.textContent = '鬨ｾ竏ｽ・ｿ・｡闕ｳ・ｭ...';
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
      result.textContent = '邵ｺ髮∵牒邵ｺ繝ｻ邊狗ｹｧ荳岩雷郢ｧ雋槫･ｳ邵ｺ蜿ｰ・ｻ蛟･・邵ｺ・ｾ邵ｺ蜉ｱ笳・ｸｲ繧・旺郢ｧ鄙ｫ窶ｲ邵ｺ・ｨ邵ｺ繝ｻ・・ｸｺ謔ｶ・樒ｸｺ・ｾ邵ｺ蜷ｶﾂ繝ｻ;
      result.style.display = 'block';
      this.reset();
    } else {
      throw new Error(json.message);
    }
  } catch(err) {
    result.className = 'form-result form-result--err';
    result.textContent = '鬨ｾ竏ｽ・ｿ・｡邵ｺ・ｫ陞滂ｽｱ隰ｨ蜉ｱ・邵ｺ・ｾ邵ｺ蜉ｱ笳・ｸｲ繧・ｼ邵ｺ・ｰ郢ｧ蟲ｨ・･驍ｨ蠕娯夢邵ｺ・ｦ邵ｺ荵晢ｽ芽怙讎奇ｽｺ・ｦ邵ｺ鬘假ｽｩ・ｦ邵ｺ蜉ｱ・･邵ｺ・ｰ邵ｺ霈費ｼ樒ｸｲ繝ｻ;
    result.style.display = 'block';
  } finally {
    btn.disabled = false;
    btn.textContent = '鬨ｾ竏ｽ・ｿ・｡邵ｺ蜷ｶ・・;
  }
});
</script>