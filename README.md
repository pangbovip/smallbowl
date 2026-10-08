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
| `GROUP_LINK` | 占位符 | **要改**：WhatsApp 建群 → 群资料 → 通过链接邀请 → 复制链接，粘贴到这里。没填之前，付款成功弹窗和"已解锁"行里的入群区块**整块隐藏**；填上真实链接后自动显示"加入群"按钮 |
| `UNLOCK_CODES` | 含演示码 `SMALLBOWL-DEMO` | **删掉演示码**，留给退款补发、朋友、媒体用 |

### 两种校验强度

- **不部署 Worker（现状）**：付款成功后**只在付款的那个浏览器里解锁**（存在 localStorage）。换设备输入解锁码无法校验，所以页面不再显示"已购买？输入解锁码"，改为提示买家"把 PayPal 收据发邮件或 WhatsApp 给我们，我们发完整版 PDF"（`app.js` 里 `CAN_RESTORE` 为 false 时的文案，见 i18n.js 的 `*Local` 和 `pricing.recover`）。
  - 人工补发 PDF 的做法：在 PayPal 后台核对收据 → 用自己的浏览器打开 chinavisit.org，开发者工具 Console 执行 `localStorage.setItem("sb_unlocked","1")` 后刷新 → 完整行程里点"存为 PDF" → 把 PDF 发给买家。
  - 部署 Worker 并填好 `VERIFY_ENDPOINT` 后，`CAN_RESTORE` 自动变 true，页面自动恢复"换设备输码"的文案和输入框，不用改别的。
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

`MAIL_ENDPOINT`：邮件订阅接口（Buttondown、Formspree、Mailchimp）。留空时页脚订阅表单整块隐藏（不收集发不出去的邮箱）；填上后自动显示。

## SEO 与收录

- 三个语言各有独立网址并互相声明 hreflang：`/`、`/ja.html`、`/ko.html`；`sitemap.xml` 列出三者，以及全部攻略页和签证页。
- 免费细节卡另有可被搜索收录的独立文章页，见下文"攻略文章页（/guide/）"。
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

## 签证页面（/visa/）

面向搜索流量的静态页，全部由脚本生成，按国籍接住"Do Americans need a visa for China"一类搜索，每页底部把人导回首页的免费细节和 $2 完整版。

```
visa_data.py    政策数据：每个国家属于哪种制度、天数、起止日期、240 小时过境资格；出典 SOURCES
visa_copy.py    三语文案与页面模板
visa.css        签证页样式（沿用 style.css 的变量）
build_visa.py   生成页面 + 重写 sitemap.xml：python build_visa.py
```

生成结果（110 页）：

- `/visa/` 查询器 + 全部国家表；`/visa/240-hour-transit.html` 过境说明；`/visa/<国家>.html` 102 个国籍页（英文）
- `/ja/visa/`、`/ja/visa/japan.html`、`/ja/visa/240-hour-transit.html`
- `/ko/visa/`、`/ko/visa/south-korea.html`、`/ko/visa/240-hour-transit.html`

**政策变了怎么改：** 改 `visa_data.py`（国家的 `scheme`、`end`、`transit` 等字段），把 `CHECKED` 改成当天日期，运行 `python build_visa.py`，连同生成的 `visa/ ja/visa/ ko/visa/ sitemap.xml` 一起提交。IndexNow 工作流现在直接读 sitemap.xml，新增页面不用再手动加进 urlList。

**必须盯的日期：** 48 国的 30 天免签目前到 **2026-12-31**（俄罗斯到 2027-12-31，布鲁内无期限）。去年的延期通知是 11 月初发的，今年 11 月留意外交部领事司公告，延期后改 `UNILATERAL_END` 重新生成；如果没延期，页面必须在 1 月 1 日前改掉。

**刻意没写的：** 厄瓜多尔、汤加的互免条件（官方表格不完整）；"香港/澳门算第三地"没有找到官方示例，页面里只写"常见做法，订票前问航空公司"。

## 攻略文章页（/guide/）

首页的细节卡是 JS 渲染的，搜索引擎没法把它们当成独立页面收录。`build_guides.py` 用**同一份免费数据**（`content-*.js` 里的免费卡片、`apps`、FAQ，以及 `i18n.js` 的文案）生成静态文章页，卡片和文章页始终同步：

```
build_guides.py   页面清单（GUIDES）、每页的 title / description / H1（META）、生成逻辑
```

生成结果（33 页）：`/guide/`、`/ja/guide/`、`/ko/guide/` 三个索引页，加上每种语言 10 篇文章，例如 `/guide/how-to-use-alipay-as-a-foreigner.html`、`/ja/guide/shared-bikes-china.html`。每页有独立的 title / description / H1、canonical、三语 hreflang、Article + BreadcrumbList 结构化数据、相关攻略和签证页的内链，以及 $2 完整版的入口。

- **只用免费内容**：脚本从不读取 `content-paid-*.js`；`check_no_paid()` 会在生成时比对付费文件，有任何付费句子混进页面就直接报错停下。锁定卡只出现标题（本来就公开）。
- **改了卡片、App、FAQ 或 i18n.js 之后**：运行 `python build_guides.py`。它会重写三种语言的文章页、`index.html` 里的"Step-by-step guides"链接区块（`<!--guides:start-->` 到 `<!--guides:end-->` 之间，别手改）、`ja.html` / `ko.html` 和 `sitemap.xml`。连同 `guide/ ja/guide/ ko/guide/ index.html ja.html ko.html sitemap.xml` 一起提交。
- **加一篇新文章**：在 `GUIDES` 里加一项（`card` 只能是免费卡），在 `META` 里写三种语言的 title / description / H1，在 `i18n.js` 三种语言里加 `guide.<id>` 短标题，然后运行脚本。
- 首页卡片底部的"Read the full page →"链接由 `app.js` 根据上面那块静态链接自动加上，不用另外维护。
- `UPDATED` 是文章页的发布 / 修改日期（页面上显示、结构化数据、sitemap 的 lastmod），改了文案就改这个日期。
- `build_visa.py` 和 `build_guides.py` 共用 `write_sitemap()`，先跑哪个都会得到完整的 sitemap。签证页模板改动后改 `build_visa.py` 里的 `PAGES_UPDATED`；`visa_data.py` 的 `CHECKED` 只在**重新核对过官方政策**后才改。

**签证页的到期提示**：凡是 `visa_data.py` 里结束日期等于 `UNILATERAL_END`（目前 2026-12-31）的 30 天免签国家，国家页顶部会自动显示红色到期提示；签证索引页也有一条总提示；需签证 / 过境国家页会提示指纹豁免和签证费减免同样在这天到期。延期公告出来后改 `UNILATERAL_END` 和 `CHECKED` 再跑 `python build_visa.py`，提示里的日期会自动更新。
