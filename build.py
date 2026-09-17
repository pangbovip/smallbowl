# Generates ja.html and ko.html from index.html using the strings in i18n.js.
# Run after editing index.html or i18n.js:  python build.py
import io, json, re, html

SITE = "https://chinavisit.org/"
META = {
    "ja": {
        "title": "China Visit｜はじめての中国7日間ガイド：豆汁の飲み方・小籠包の食べ方・シェア自転車の乗り方",
        "description": "日本人向けの中国7日間旅行ガイド。北京の豆汁の飲み方、上海の小籠包の食べ方、シェア自転車、QR決済、地下鉄、トイレまで、誰も教えてくれない小さなコツだけを集めました。完全版は2ドル買い切り。",
        "og_title": "China Visit｜はじめての中国7日間ガイド",
    },
    "ko": {
        "title": "China Visit | 처음 가는 중국 7일 가이드: 더우즈 마시는 법, 샤오롱바오 먹는 법, 공유자전거 타는 법",
        "description": "한국인을 위한 중국 7일 여행 가이드. 베이징 더우즈, 상하이 샤오롱바오, 공유자전거, QR 결제, 지하철, 화장실까지 아무도 안 알려주는 작은 요령만 모았습니다. 전체 가이드는 2달러 1회 결제.",
        "og_title": "China Visit | 처음 가는 중국 7일 가이드",
    },
}

def load_i18n():
    src = io.open("i18n.js", encoding="utf-8").read()
    body = src[src.index("{"): src.rindex("}") + 1]
    body = re.sub(r"^\s*//[^\n]*", "", body, flags=re.M)              # comment lines
    body = re.sub(r"^(\s*)(en|ja|ko):", r'\1"\2":', body, flags=re.M)  # top-level language keys
    body = re.sub(r",(\s*[}\]])", r"\1", body)                         # trailing commas
    return json.loads(body)

def build(lang, i18n):
    page = io.open("index.html", encoding="utf-8").read()
    strings = i18n[lang]
    m = META[lang]
    page = page.replace('<html lang="en">', '<html lang="%s" data-lang="%s">' % (lang, lang), 1)
    page = re.sub(r"<title>.*?</title>", "<title>%s</title>" % html.escape(m["title"]), page, count=1, flags=re.S)
    page = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % html.escape(m["description"], quote=True), page, count=1)
    page = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % html.escape(m["og_title"], quote=True), page, count=1)
    page = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % html.escape(m["description"], quote=True), page, count=1)
    page = page.replace('<meta property="og:url" content="%s">' % SITE, '<meta property="og:url" content="%s%s.html">' % (SITE, lang), 1)
    page = page.replace('<link rel="canonical" href="%s">' % SITE, '<link rel="canonical" href="%s%s.html">' % (SITE, lang), 1)

    def text_repl(mo):
        key = mo.group(2)
        val = strings.get(key)
        if val is None:
            return mo.group(0)
        return mo.group(1) + html.escape(val, quote=False) + mo.group(4)
    page = page.replace('href="visa/" data-i18n="nav.visa"', 'href="%s/visa/" data-i18n="nav.visa"' % lang, 1)
    page = re.sub(r'(data-i18n="([^"]+)"[^>]*>)(.*?)(</)', text_repl, page, flags=re.S)

    def ph_repl(mo):
        key = mo.group(1)
        val = strings.get(key)
        if val is None:
            return mo.group(0)
        return 'data-i18n-placeholder="%s" placeholder="%s"' % (key, html.escape(val, quote=True))
    page = re.sub(r'data-i18n-placeholder="([^"]+)" placeholder="[^"]*"', ph_repl, page)
    return page

if __name__ == "__main__":
    i18n = load_i18n()
    for lang in ("ja", "ko"):
        out = build(lang, i18n)
        io.open("%s.html" % lang, "w", encoding="utf-8", newline="\n").write(out)
        print("wrote %s.html (%d bytes)" % (lang, len(out.encode("utf-8"))))
