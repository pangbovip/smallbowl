# 小碗 Small Bowl China — 7天中国细节攻略站

面向日本、韩国及欧美首次来华游客的静态网站。免费展示 8 张"细节卡"和 7 天骨架，付费解锁完整攻略。三语（EN / 日本語 / 한국어），按浏览器语言自动切换。

## 目录

```
site/
  index.html       页面骨架（英文，x-default），所有文案通过 data-i18n 注入
  ja.html / ko.html  由 build.py 从 index.html + i18n.js 生成的日/韩版（独立网址，供 Google 收录）
  build.py         改过 index.html 或 i18n.js 后运行一次：python build.py

改了 style.css 或任何 .js 后，把 index.html 里 `?v=` 的版本号改一下再运行 build.py，否则老访客的浏览器会用缓存的旧文件。
  style.css        视觉系统（浅色 / 深色自动）
  i18n.js          界面文案（三语）
  content-en.js    英文内容：卡片、7 天、价格档、FAQ
  content-ja.js    日文内容
  content-ko.js    韩文内容
  content-paid-en.js / -ja.js / -ko.js  付费内容：6 张卡完整正文、7 天逐小时行程（含雨天方案、每天 6 句）、12 句通用短语
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
| `GROUP_LINK` | 占位符 | **要改**：WhatsApp 建群 → 群资料 → 通过链接邀请 → 复制链接，粘贴到这里。没填之前，按钮自动变成"发消息请求入群"，点击是给你发一条预填的 WhatsApp 私信，你手动拉人；填上链接后按钮自动变回"加入群" |
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

### 付费内容

解锁后页面多出两个区块："完整行程（逐小时）"和"短语本"。每天一张表（时刻 / 给司机看的中文 / 做什么）、雨天方案、6 句当日短语；6 张锁定卡显示完整步骤。短语总数：免费 8 + 卡片 6 + 每日 42 + 通用 12 = 68 张。

"存为 PDF"按钮调用浏览器打印，`style.css` 末尾的 `@media print` 只输出解锁内容，买家自己存离线版。付费内容文件仍是公开的静态 JS，看源码能读到；2 美元的产品接受这个取舍，介意就按上面 Worker 方案把这三个文件改成解锁后再从 Worker 拉取。

`MAIL_ENDPOINT`：邮件订阅接口（Buttondown、Formspree、Mailchimp）。留空时邮箱只存本机 localStorage。

## SEO 与收录

- 三个语言各有独立网址并互相声明 hreflang：`/`、`/ja.html`、`/ko.html`；`sitemap.xml` 列出三者。
- `index.html` 头部有 JSON-LD（WebSite、Product $2、FAQPage）。
- Google Search Console：用"网域"属性添加 `chinavisit.org`，在 Cloudflare DNS 加 Google 给的 TXT 记录验证，然后在"站点地图"提交 `https://chinavisit.org/sitemap.xml`。
- 韩国用户主要用 Naver：在 Naver Search Advisor 添加站点并提交同一个 sitemap。日本用户用 Google，Yahoo Japan 也走 Google 索引。
- 与问古堂互链：本站页脚"姊妹站"区块指向 wenguhall.com（日文页指向 /ja.html）；问古堂页脚已回链 chinavisit.org。

## 数据与推广

- **访问统计**：Cloudflare Web Analytics，代码在 `index.html` 的 `</body>` 前，`build.py` 会带到日韩页。看数据：Cloudflare 后台 → Analytics & Logs → Web Analytics → chinavisit.org。能看访问量、来源网站、国家、设备、热门页面。
- **IndexNow**：`.github/workflows/indexnow.yml` 在每次改动页面并推送后，等 90 秒通知 Bing、Naver 等搜索引擎重新抓取；密钥文件是根目录的 `00869675f174f36b12e5b37f660fc249.txt`，不要删。
- **推送前先 `git fetch` 再变基**：仓库在 GitHub 网页上也会有人加文件。
- **推广素材**：`推广素材/`（不进网站仓库）。`发帖文案.md` 是各平台文案和两周发布节奏；`make_share_images.py` 生成 1080×1350 分享图，改了卡片内容后重新运行即可。

## 添加内容

- 新卡片：在三个 `content-*.js` 的 `cards` 数组里各加一项，`id` 相同。`locked: true` 的卡片只写 `hook` 和 `teaser`，完整内容放 `content-paid-*.js` 的 `cards[id]`。
- 行程：`content-paid-*.js` 的 `days[i]` 有 `plan`（时刻/中文/说明）、`rain`、`say` 三部分，第 i 天对应 `content-*.js` 里 `days[i]` 的城市和标题。
- 每张卡必须有 `say`（中文 + 拼音 + 释义），这是"指给店员看"功能的来源。
- 免费板块"出发前必装的 App"在三个 `content-*.js` 的 `apps` 数组里，字段：`mark`（标志上的汉字）、`tag`、`what`、`why`（替代了什么）、`setup`（在家要做完的事）、`site`。
- 每张卡对应一张原图 `images/<id>.jpg`（3:2）。换成自己拍的照片：覆盖同名文件，把 `images/credits.js` 里对应条目删掉，然后运行 `python make_responsive_images.py`。页面实际加载的是它生成的 `<id>-400.avif`、`<id>-800.avif` 和 `<id>-800.jpg`，不重新生成就还是旧图。
- 首页天坛图同理：原图 `images/tiantan.jpg`，页面用的是生成的 `tiantan-*.avif`（电脑竖图）和 `tiantan-wide-*.avif`（手机 3:2 横图）。
- 城市筛选按钮在 `index.html` 的 `.filters` 里，`data-filter` 值要和卡片的 `city` 一致。

## 内容核对提醒

签证、支付手续费、票价按 2026 年中情况写的。每季度核对：日韩免签政策、支付宝/微信境外卡是否收手续费（目前不收）、故宫预约规则、高铁票价。
