# 小碗 Small Bowl China — 7天中国细节攻略站

面向日本、韩国及欧美首次来华游客的静态网站。免费展示 8 张"细节卡"和 7 天骨架，付费解锁完整攻略。三语（EN / 日本語 / 한국어），按浏览器语言自动切换。

## 目录

```
site/
  index.html       页面骨架，所有文案通过 data-i18n 注入
  style.css        视觉系统（浅色 / 深色自动）
  i18n.js          界面文案（三语）
  content-en.js    英文内容：卡片、7 天、价格档、FAQ
  content-ja.js    日文内容
  content-ko.js    韩文内容
  content-paid.js  付费内容样例（解锁后显示）
  app.js           渲染、语言切换、筛选、解锁码、"指给店员看"放大卡
```

本地预览：直接双击 `site/index.html`，或在 `site/` 下运行 `python -m http.server 8080`。

## 上线（免费）

把 `site/` 整个目录拖到 Netlify Drop、Cloudflare Pages 或 GitHub Pages 即可，无需构建。

## 收款：三处要改的地方（都在 `app.js` 顶部）

1. **PAY_LINKS**：换成你的 Stripe Payment Link / Gumroad / Lemon Squeezy 购买链接。
   - 日韩用户建议 Stripe（支持 JCB、Konbini、Kakao Pay 通过 Alipay+ 不行，但卡支付够用）。
   - Gumroad 最简单：上传 PDF，设价 US$2，复制链接即可。定价只有一档：2 美元（¥300 / ₩2,800）买断。
2. **UNLOCK_CODES**：购买后邮件里发给用户的解锁码。也支持链接直达：`https://你的域名/?code=XIAOWAN2026`。
   - 当前是纯前端校验，只能挡住普通用户。要真正防盗版：
     - 把 `content-paid.js` 从公开目录移走，只在 PDF 里发完整内容；或
     - 用 Gumroad License Key / Lemon Squeezy License API 在 Cloudflare Worker 里校验后再返回付费内容。
3. **MAIL_ENDPOINT**：邮件订阅接口（Buttondown、Formspree、Mailchimp）。留空时邮箱只存本机 localStorage。

演示解锁码：`SMALLBOWL-DEMO`（上线前删掉）。

## 添加内容

- 新卡片：在三个 `content-*.js` 的 `cards` 数组里各加一项，`id` 相同。`locked: true` 的卡片只写 `hook` 和 `teaser`，完整内容放 `content-paid.js`。
- 每张卡必须有 `say`（中文 + 拼音 + 释义），这是"指给店员看"功能的来源。
- 城市筛选按钮在 `index.html` 的 `.filters` 里，`data-filter` 值要和卡片的 `city` 一致。

## 内容核对提醒

签证、支付手续费、票价按 2026 年中情况写的。每季度核对：日韩免签政策、支付宝境外卡手续费（当前 200 元以下免费）、故宫预约规则、高铁票价。
