---
layout: default
title: 縺雁撫縺・粋繧上○
---

{% include header.html %}

<div class="dashboard-container">
  <div class="section-block">
    <div class="section-header">
      <h2 class="section-title">縺雁撫縺・粋繧上○</h2>
      <div class="section-mark"></div>
    </div>

    <div class="contact-content">
      <p class="contact-lead">繝・・繧ｿ縺ｮ隱､繧翫・縺疲э隕九・縺碑ｦ∵悍縺ｪ縺ｩ縺ｯ莉･荳九・繝輔か繝ｼ繝繧医ｊ縺企√ｊ縺上□縺輔＞縲・/p>

      <form class="contact-form" id="contactForm">
        <input type="hidden" name="access_key" value="142535ed-d4d0-4cc8-b468-b71ee8c58bc8">
        <input type="hidden" name="subject" value="縲先律譛ｬ縺ｮ謾ｿ豐ｻ縲代♀蝠上＞蜷医ｏ縺・>
        <input type="hidden" name="from_name" value="譌･譛ｬ縺ｮ謾ｿ豐ｻ 縺雁撫縺・粋繧上○繝輔か繝ｼ繝">
        <input type="checkbox" name="botcheck" style="display:none">

        <div class="form-group">
          <label class="form-label" for="name">縺雁錐蜑・/label>
          <input class="form-input" type="text" id="name" name="name"
            placeholder="螻ｱ逕ｰ 螟ｪ驛・ required>
        </div>

        <div class="form-group">
          <label class="form-label" for="email">繝｡繝ｼ繝ｫ繧｢繝峨Ξ繧ｹ</label>
          <input class="form-input" type="email" id="email" name="email"
            placeholder="example@example.com" required>
        </div>

        <div class="form-group">
          <label class="form-label" for="category">莉ｶ蜷・/label>
          <select class="form-input" id="category" name="category" required>
            <option value="" disabled selected>驕ｸ謚槭＠縺ｦ縺上□縺輔＞</option>
            <option value="繝・・繧ｿ縺ｮ隱､繧翫↓縺､縺・※">繝・・繧ｿ縺ｮ隱､繧翫↓縺､縺・※</option>
            <option value="讖溯・縺ｮ隕∵悍">讖溯・縺ｮ隕∵悍</option>
            <option value="縺昴・莉・>縺昴・莉・/option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label" for="message">縺雁撫縺・粋繧上○蜀・ｮｹ</label>
          <textarea class="form-input form-textarea" id="message" name="message"
            rows="6" placeholder="縺雁撫縺・粋繧上○蜀・ｮｹ繧偵＃險伜・縺上□縺輔＞" required></textarea>
        </div>

        <div class="form-submit">
          <button type="submit" class="submit-btn" id="submitBtn">騾∽ｿ｡縺吶ｋ</button>
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
  btn.textContent = '騾∽ｿ｡荳ｭ...';
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
      result.textContent = '縺雁撫縺・粋繧上○繧貞女縺台ｻ倥￠縺ｾ縺励◆縲ゅ≠繧翫′縺ｨ縺・＃縺悶＞縺ｾ縺吶・;
      result.style.display = 'block';
      this.reset();
    } else {
      throw new Error(json.message);
    }
  } catch(err) {
    result.className = 'form-result form-result--err';
    result.textContent = '騾∽ｿ｡縺ｫ螟ｱ謨励＠縺ｾ縺励◆縲ゅ＠縺ｰ繧峨￥邨後▲縺ｦ縺九ｉ蜀榊ｺｦ縺願ｩｦ縺励￥縺縺輔＞縲・;
    result.style.display = 'block';
  } finally {
    btn.disabled = false;
    btn.textContent = '騾∽ｿ｡縺吶ｋ';
  }
});
</script>