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
  app.js           渲染、语言切换、筛选、PayPal 弹窗、解锁码、"指给店员看"放大卡
worker/            可选：Cloudflare Worker，用 PayPal API 校验交易并存解锁码
```

本地预览：直接双击 `site/index.html`，或在 `site/` 下运行 `python -m http.server 8080`。

## 上线（免费）

仓库 https://github.com/pangbovip/smallbowl ，GitHub Pages 从 main 分支根目录发布，自定义域名 https://chinavisit.org （CNAME 文件），域名和 DNS 都在 Cloudflare，与问古堂同一套。

## 收款：PayPal 弹窗，付完当场解锁

流程（已实现，和问古堂同一个 PayPal 商家账号）：

1. 访客点任意"解锁"或"购买 · $2"按钮 → 页面内弹出 PayPal 按钮（PayPal 余额或任意信用卡，不需要 PayPal 账号）。
2. 付款成功 → 本机立即解锁全部锁定卡和 7 天付费内容 → 弹窗显示解锁码 `SB-<PayPal 交易号>`，可一键复制。
3. 换设备：在定价区"已购买？"输入解锁码即可。买家丢了码也没关系，PayPal 收据邮件里的 Transaction ID 就是它。

`app.js` 顶部四个配置：

| 变量 | 现状 | 上线前 |
|---|---|---|
| `PAYPAL_CLIENT_ID` | 已填问古堂的客户端 ID | 不用改（客户端 ID 本来就是公开的） |
| `PRICE_USD` | `2.00` | 改价只改这里 |
| `VERIFY_ENDPOINT` | 空 | 可选：填 Worker 地址后解锁码走服务端校验（见下） |
| `UNLOCK_CODES` | 含演示码 `SMALLBOWL-DEMO` | **删掉演示码**，留给退款补发、朋友、媒体用 |

### 两种校验强度

- **不部署 Worker（现状）**：解锁码在浏览器里只校验格式（`SB-` + 12~20 位字母数字）。挡得住普通用户，挡不住看源码的人。2 美元的产品，这个强度通常够用。
- **部署 Worker（推荐，20 分钟）**：付款后页面把交易号发给 Worker，Worker 用 PayPal API 核实"已完成、≥2 美元"才发码并存入 KV；换设备输码时也查 KV。步骤：

```bash
cd worker
npx wrangler login
npx wrangler kv namespace create CODES
```

把打印出的 id 填进 `wrangler.toml`，然后：

```bash
npx wrangler secret put PAYPAL_CLIENT_ID
npx wrangler secret put PAYPAL_SECRET
npx wrangler deploy
```

PayPal Secret 在 https://developer.paypal.com/dashboard/applications/live 里，点问古堂那个应用就能看到（和客户端 ID 配对）。部署完把 Worker 地址（形如 `https://smallbowl-unlock.<你的子域>.workers.dev`）填进 `app.js` 的 `VERIFY_ENDPOINT`，推送即可。

### 付费内容本身

定价卡承诺了"7 天逐小时、60 张指给店员看的卡、每日雨天方案、离线 PDF"。目前 `content-paid.js` 只有烤鸭卡和第 1 天的样例。**开始收款前要把这些写完**，否则买家付 2 美元看到的和免费版几乎一样，会退款和差评。PDF 可以用浏览器"打印为 PDF"从解锁后的页面导出，或者我来单独生成。

`MAIL_ENDPOINT`：邮件订阅接口（Buttondown、Formspree、Mailchimp）。留空时邮箱只存本机 localStorage。

## 添加内容

- 新卡片：在三个 `content-*.js` 的 `cards` 数组里各加一项，`id` 相同。`locked: true` 的卡片只写 `hook` 和 `teaser`，完整内容放 `content-paid.js`。
- 每张卡必须有 `say`（中文 + 拼音 + 释义），这是"指给店员看"功能的来源。
- 城市筛选按钮在 `index.html` 的 `.filters` 里，`data-filter` 值要和卡片的 `city` 一致。

## 内容核对提醒

签证、支付手续费、票价按 2026 年中情况写的。每季度核对：日韩免签政策、支付宝境外卡手续费（当前 200 元以下免费）、故宫预约规则、高铁票价。
