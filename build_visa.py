# Generates the visa pages and rewrites sitemap.xml.
#   /visa/                      EN checker + full country table
#   /visa/240-hour-transit.html EN transit explainer
#   /visa/<slug>.html           EN, one page per passport
#   /ja/visa/  /ja/visa/japan.html        /ja/visa/240-hour-transit.html
#   /ko/visa/  /ko/visa/south-korea.html  /ko/visa/240-hour-transit.html
#
# Policy facts live in visa_data.py. When a rule changes: edit visa_data.py, bump CHECKED, run
#   python build_visa.py
# then commit the generated folders together with sitemap.xml.
import html
import io
import json
import os
from datetime import date

import visa_data as D

SITE = "https://chinavisit.org"
ASSET_V = "20260917v"
LANGS = ("en", "ja", "ko")
HOME = {"en": "/", "ja": "/ja.html", "ko": "/ko.html"}
HUB = {"en": "/visa/", "ja": "/ja/visa/", "ko": "/ko/visa/"}
TRANSIT = {"en": "/visa/240-hour-transit.html", "ja": "/ja/visa/240-hour-transit.html", "ko": "/ko/visa/240-hour-transit.html"}
# Country pages that exist in each language besides English.
LOCAL_COUNTRY = {"ja": "japan", "ko": "south-korea"}

FONTS = ("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800"
         "&family=IBM+Plex+Mono:wght@400;600&family=Noto+Sans+JP:wght@400;700&family=Noto+Sans+KR:wght@400;700"
         "&family=Noto+Sans+SC:wght@400;700&family=Zhi+Mang+Xing&display=swap")

e = lambda s: html.escape(str(s), quote=True)
BY_SLUG = {c["slug"]: c for c in D.COUNTRIES}


def country_url(lang, slug):
    if lang != "en" and LOCAL_COUNTRY.get(lang) == slug:
        return "/%s/visa/%s.html" % (lang, slug)
    return "/visa/%s.html" % slug


def fmt_date(iso, lang):
    y, m, d = (int(x) for x in iso.split("-"))
    if lang == "ja":
        return "%d年%d月%d日" % (y, m, d)
    if lang == "ko":
        return "%d년 %d월 %d일" % (y, m, d)
    return date(y, m, d).strftime("%-d %B %Y") if os.name != "nt" else date(y, m, d).strftime("%d %B %Y").lstrip("0")


def name(c, lang):
    return c[lang] if lang != "en" else c["en"]


# ------------------------------------------------------------------ chrome
UI = {
    "en": {"nav": [("Details", "#details"), ("Apps", "#apps"), ("7 days", "#days"), ("Full guide", "#pricing")], "visa": "Visa",
           "home": "Home", "hub": "Visa check", "checked": "Checked {d}", "sources": "Sources",
           "legal": "Visa rules change, sometimes with a week's notice. We check official announcements and update this page, but the border officer and your airline have the final word. Confirm with the Chinese embassy or consulate where you live before you fly.",
           "cta_h": "Visa sorted. Now the small bowl.",
           "cta_p": "The part nobody explains: paying with Alipay, unlocking a shared bike, ordering douzhi without a word of Chinese. Free details, full 7-day guide $2.",
           "cta_btn": "Read the free details", "say_tip": "Show the screen. Point. Smile.", "tap": "Tap to enlarge"},
    "ja": {"nav": [("ディテール", "#details"), ("アプリ", "#apps"), ("7日間", "#days"), ("完全版", "#pricing")], "visa": "ビザ",
           "home": "ホーム", "hub": "ビザ確認", "checked": "{d} 確認", "sources": "出典",
           "legal": "ビザ制度は短い予告で変わることがあります。公式発表を確認して更新していますが、最終判断は入国審査官と航空会社です。出発前に在日中国大使館・総領事館で必ず確認してください。",
           "cta_h": "ビザはOK。次は「小さなコツ」。",
           "cta_p": "Alipayでの支払い、シェア自転車の解錠、中国語ゼロで豆汁を注文する方法。誰も教えてくれない部分をまとめました。無料で読めて、完全版は2ドル。",
           "cta_btn": "無料のコツを読む", "say_tip": "画面を見せて、指さして、笑顔で。", "tap": "タップで拡大"},
    "ko": {"nav": [("디테일", "#details"), ("앱", "#apps"), ("7일", "#days"), ("전체 가이드", "#pricing")], "visa": "비자",
           "home": "홈", "hub": "비자 확인", "checked": "{d} 확인", "sources": "출처",
           "legal": "비자 제도는 짧은 예고로 바뀔 수 있습니다. 공식 발표를 확인해 업데이트하지만 최종 판단은 입국심사관과 항공사가 합니다. 출발 전 주한 중국대사관·총영사관에서 꼭 확인하세요.",
           "cta_h": "비자는 해결. 이제 작은 요령.",
           "cta_p": "알리페이 결제, 공유자전거 잠금 해제, 중국어 한마디 없이 더우즈 주문하기. 아무도 안 알려주는 부분만 모았습니다. 무료로 읽고, 전체 가이드는 2달러.",
           "cta_btn": "무료 요령 읽기", "say_tip": "화면을 보여주고, 가리키고, 웃으세요.", "tap": "탭하면 크게"},
}

BRAND_SVG = ('<svg class="brand-mark" viewBox="0 0 64 64" width="30" height="30" aria-hidden="true"><path d="M8 27h48a24 24 0 0 1-48 0z" fill="#C4331F"/>'
             '<rect x="24" y="51" width="16" height="4" rx="1" fill="#C4331F"/><path d="M16 12l30 26M23 8l30 26" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" fill="none"/></svg>')


def page(lang, path, title, desc, body, alternates, jsonld, crumbs):
    """alternates: {lang: path} for hreflang; the language switch uses it, falling back to that language's hub."""
    u = UI[lang]
    alt_links = "".join('<link rel="alternate" hreflang="%s" href="%s%s">\n' % (l, SITE, p) for l, p in alternates.items())
    if "en" in alternates:
        alt_links += '<link rel="alternate" hreflang="x-default" href="%s%s">\n' % (SITE, alternates["en"])
    switch = "".join('<a href="%s" lang="%s" hreflang="%s"%s>%s</a>' % (
        alternates.get(l, HUB[l]), l, l, ' class="is-on" aria-current="true"' if l == lang else "", lab)
        for l, lab in (("en", "EN"), ("ja", "日本語"), ("ko", "한국어")))
    nav = "".join('<a href="%s%s">%s</a>' % (HOME[lang], h, e(t)) for t, h in u["nav"])
    nav += '<a href="%s" aria-current="page">%s</a>' % (HUB[lang], e(u["visa"]))
    crumb = " / ".join('<a href="%s">%s</a>' % (h, e(t)) for t, h in crumbs[:-1]) + " / " + e(crumbs[-1][0])
    bc = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": t, "item": SITE + h} for i, (t, h) in enumerate(crumbs)]}
    graph = json.dumps({"@context": "https://schema.org", "@graph": [bc] + jsonld}, ensure_ascii=False)
    return """<!DOCTYPE html>
<html lang="{lang}" data-lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}{path}">
{alts}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{fonts}"></noscript>
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}{path}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="China Visit">
<meta property="og:image" content="{site}/images/tiantan.jpg">
<link rel="icon" type="image/svg+xml" href="/images/logo.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32.png">
<link rel="apple-touch-icon" href="/images/apple-touch-icon.png">
<meta name="theme-color" content="#F1F3EE">
<link rel="stylesheet" href="/style.css?v={v}">
<link rel="stylesheet" href="/visa.css?v={v}">
<script type="application/ld+json">{graph}</script>
</head>
<body>
<header class="top">
  <a class="brand" href="{home}">{svg}<span class="brand-zh">小碗</span><span class="brand-en">Small Bowl</span></a>
  <nav class="nav" aria-label="Sections">{nav}</nav>
  <div class="lang" role="group" aria-label="Language">{switch}</div>
</header>
<main class="v-main">
<p class="crumbs">{crumb}</p>
{body}
</main>
<footer class="foot">
  <div class="foot-brand">
    <span class="brand-zh">小碗</span>
    <p class="v-foot"><a href="{home}">{home_t}</a><a href="{hub}">{hub_t}</a><a href="{transit}">240h</a><a href="mailto:86886779@qq.com?subject=China%20Visit%20visa">86886779@qq.com</a></p>
  </div>
  <p class="foot-legal">{legal}</p>
</footer>
<div class="say-overlay" id="sayOverlay" hidden role="dialog" aria-modal="true" aria-label="Show this to staff">
  <button type="button" class="say-close" id="sayClose" aria-label="Close">×</button>
  <p class="say-overlay-zh" id="sayZh"></p>
  <p class="say-overlay-pinyin" id="sayPinyin"></p>
  <p class="say-overlay-tip">{say_tip}</p>
</div>
<script>
(function () {{
  var o = document.getElementById("sayOverlay");
  document.addEventListener("click", function (ev) {{
    var b = ev.target.closest("[data-say]");
    if (!b) return;
    document.getElementById("sayZh").textContent = b.getAttribute("data-say");
    document.getElementById("sayPinyin").textContent = b.getAttribute("data-say-pinyin") || "";
    o.hidden = false; document.getElementById("sayClose").focus();
  }});
  function close() {{ o.hidden = true; }}
  document.getElementById("sayClose").addEventListener("click", close);
  document.addEventListener("keydown", function (ev) {{ if (ev.key === "Escape") close(); }});
}})();
</script>
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "3685ef96a9c6460796e8590ef74cd9d0"}}'></script>
</body>
</html>
""".format(lang=lang, title=e(title), desc=e(desc), site=SITE, path=path, alts=alt_links, fonts=FONTS, v=ASSET_V,
           graph=graph, home=HOME[lang], svg=BRAND_SVG, nav=nav, switch=switch, crumb=crumb, body=body,
           home_t=e(u["home"]), hub=HUB[lang], hub_t=e(u["hub"]), transit=TRANSIT[lang], legal=e(u["legal"]),
           say_tip=e(u["say_tip"]))


def faq_block(lang, items):
    body = "".join('<details><summary>%s</summary><div class="faq-body"><p>%s</p></div></details>' % (e(q), a) for q, a in items)
    ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in items]}
    title = {"en": "Questions people ask", "ja": "よくある質問", "ko": "자주 묻는 질문"}[lang]
    return '<section class="prose v-faq"><h2>%s</h2><div class="faq">%s</div></section>' % (title, body), ld


def strip_tags(s):
    import re
    return re.sub(r"<[^>]+>", "", s)


def say_cards(lang, keys):
    u = UI[lang]
    out = []
    for k in keys:
        zh, py, mean = D.PHRASES[k]["zh"], D.PHRASES[k]["py"], D.PHRASES[k][lang]
        out.append('<button type="button" class="say-card" data-say="%s" data-say-pinyin="%s"><span class="say-zh">%s</span>'
                   '<span class="say-pinyin">%s</span><span class="say-meaning">%s</span><span class="say-hint">%s</span></button>'
                   % (e(zh), e(py), e(zh), e(py), e(mean), e(u["tap"])))
    return '<div class="say-stack">%s</div>' % "".join(out)


def cta(lang):
    u = UI[lang]
    return ('<aside class="v-cta"><div><h2>%s</h2><p>%s</p></div><a class="btn" href="%s#details">%s</a></aside>'
            % (e(u["cta_h"]), e(u["cta_p"]), HOME[lang], e(u["cta_btn"])))


def sources(lang, keys):
    rows = "".join('<span>%s: <a href="%s" rel="noopener" target="_blank">%s</a></span>' % (e(D.SOURCES[k]["title"]), e(D.SOURCES[k]["url"]), e(D.SOURCES[k]["url"])) for k in keys)
    return '<p class="sources"><strong>%s</strong>%s<span>%s</span></p>' % (e(UI[lang]["sources"]), rows, e(UI[lang]["checked"].format(d=fmt_date(D.CHECKED, lang))))


def write(path, text):
    fs = path.lstrip("/")
    if fs.endswith("/"):
        fs += "index.html"
    os.makedirs(os.path.dirname(fs), exist_ok=True)
    io.open(fs, "w", encoding="utf-8", newline="\n").write(text)
    return path


# ------------------------------------------------------------------ pages (copy lives in visa_copy.py)
import visa_copy as C  # noqa: E402


def main():
    written = []  # (path, {lang: path} alternates)

    # hubs
    hub_alts = dict(HUB)
    for lang in LANGS:
        title, desc, body, ld = C.hub(lang, D, BY_SLUG, country_url, fmt_date, say_cards, faq_block, cta, sources, e)
        crumbs = [(UI[lang]["home"], HOME[lang]), (UI[lang]["hub"], HUB[lang])]
        written.append((write(HUB[lang], page(lang, HUB[lang], title, desc, body, hub_alts, ld, crumbs)), hub_alts))

    # transit explainers
    tr_alts = dict(TRANSIT)
    for lang in LANGS:
        title, desc, body, ld = C.transit(lang, D, BY_SLUG, country_url, fmt_date, say_cards, faq_block, cta, sources, e)
        crumbs = [(UI[lang]["home"], HOME[lang]), (UI[lang]["hub"], HUB[lang]), ({"en": "240-hour transit", "ja": "240時間トランジット", "ko": "240시간 경유"}[lang], TRANSIT[lang])]
        written.append((write(TRANSIT[lang], page(lang, TRANSIT[lang], title, desc, body, tr_alts, ld, crumbs)), tr_alts))

    # country pages
    for c in D.COUNTRIES:
        alts = {"en": "/visa/%s.html" % c["slug"]}
        for l, slug in LOCAL_COUNTRY.items():
            if slug == c["slug"]:
                alts[l] = "/%s/visa/%s.html" % (l, slug)
        for lang in alts:
            title, desc, body, ld, short = C.country(lang, c, D, BY_SLUG, country_url, fmt_date, say_cards, faq_block, cta, sources, e)
            crumbs = [(UI[lang]["home"], HOME[lang]), (UI[lang]["hub"], HUB[lang]), (short, alts[lang])]
            written.append((write(alts[lang], page(lang, alts[lang], title, desc, body, alts, ld, crumbs)), alts))

    write_sitemap(written)
    print("wrote %d visa pages + sitemap.xml" % len(written))


def write_sitemap(written):
    import re
    old = io.open("sitemap.xml", encoding="utf-8").read() if os.path.exists("sitemap.xml") else ""
    kept = dict(re.findall(r"<loc>%s([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>" % re.escape(SITE), old))
    home_alts = {"en": "/", "ja": "/ja.html", "ko": "/ko.html"}
    entries = [(p, home_alts) for p in ("/", "/ja.html", "/ko.html")] + written
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for p, alts in entries:
        out.append("  <url>")
        out.append("    <loc>%s%s</loc>" % (SITE, p))
        out.append("    <lastmod>%s</lastmod>" % (kept.get(p) if p in home_alts.values() and p in kept else D.CHECKED))
        if len(alts) > 1:
            for l, ap in alts.items():
                out.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>' % (l, SITE, ap))
            if "en" in alts:
                out.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>' % (SITE, alts["en"]))
        out.append("  </url>")
    out.append("</urlset>")
    io.open("sitemap.xml", "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
