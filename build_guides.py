# Generates the standalone guide pages from the same data the homepage cards use, so cards and pages stay in sync.
#   /guide/            EN index         /guide/<slug>.html     EN article
#   /ja/guide/         JA index         /ja/guide/<slug>.html  JA article
#   /ko/guide/         KO index         /ko/guide/<slug>.html  KO article
# It also refreshes the "Step-by-step guides" link block in index.html, ja.html / ko.html (via build.py)
# and sitemap.xml (via build_visa.write_sitemap).
#
# Content comes ONLY from the free files: content-en/ja/ko.js (free cards, apps, FAQ, tiers, locked-card teasers)
# and i18n.js (labels). The paid files (content-paid-*.js) are never read; check_no_paid() fails the build if any
# paid sentence ends up in a page.
#
# After editing a card, an app, i18n.js or the copy below:
#   python build_guides.py
# then commit guide/ ja/guide/ ko/guide/ index.html ja.html ko.html sitemap.xml together.
import io
import json
import os
import re

import build as B          # load_i18n, and ja/ko homepage generation
import build_visa as V     # site chrome shared with the visa pages
import visa_data as D

SITE = V.SITE
LANGS = ("en", "ja", "ko")
UPDATED = "2026-10-08"     # datePublished / dateModified / sitemap lastmod; bump when the guide copy changes
HUB = V.GUIDE_HUB
HOME = V.HOME
e = V.e

# ------------------------------------------------------------------ which pages exist
# card: id of a free card in content-*.js (steps, where, mistake, phrase). setup: app ids shown as "do this at home".
# also: app ids shown after the steps. faq: indexes into content faq. related: other guide ids.
GUIDES = [
    dict(id="alipay", slug="how-to-use-alipay-as-a-foreigner", card="pay", home=["pay", "alipay"], mark="支付宝", setup=["alipay"], also=["wechat"], faq=[2],
         related=["apps", "bike", "metro", "esim"]),
    dict(id="apps", slug="apps-to-download-before-china", card=None, mark="App", app_list=True, faq=[],
         related=["alipay", "esim", "metro", "bike"]),
    dict(id="esim", slug="china-esim-internet-guide", card=None, mark="网", main_app="esim", also=["translate"], faq=[1],
         related=["apps", "alipay", "metro"]),
    dict(id="metro", slug="how-to-ride-the-metro-in-china", card="metro", mark="地铁", setup=["alipay", "amap"], faq=[],
         related=["bike", "alipay", "apps"]),
    dict(id="bike", slug="shared-bikes-china", card="bike", mark="单车", setup=["alipay"], faq=[],
         related=["metro", "alipay", "apps"]),
    dict(id="xlb", slug="how-to-eat-xiaolongbao", card="xlb", mark="小笼包", faq=[3],
         related=["douzhi", "hotpot", "water", "alipay"]),
    dict(id="douzhi", slug="how-to-drink-douzhi", card="douzhi", mark="豆汁", faq=[3],
         related=["xlb", "hotpot", "alipay"]),
    dict(id="hotpot", slug="sichuan-hotpot-dipping-sauce", card="hotpot", mark="火锅", faq=[3],
         related=["xlb", "douzhi", "water"]),
    dict(id="water", slug="hot-water-in-china", card="water", mark="热水", faq=[],
         related=["toilet", "xlb", "metro"]),
    dict(id="toilet", slug="public-toilets-in-china", card="toilet", mark="厕所", faq=[],
         related=["water", "metro", "apps"]),
]
BY_ID = {g["id"]: g for g in GUIDES}
GROUPS = [("money", ["alipay", "apps", "esim"]), ("move", ["metro", "bike"]), ("food", ["xlb", "douzhi", "hotpot"]), ("daily", ["water", "toilet"])]
STARTERS = [BY_ID[i] for i in ("alipay", "apps", "esim")]   # linked from every visa page

# Search-facing copy: title / meta description / H1. Every fact here is already in content-*.js.
META = {
    "en": {
        "alipay": ("How to Use Alipay in China as a Foreigner (2026 Setup + QR Pay)",
                   "Set up Alipay with a Visa, Mastercard or JCB before you fly, then pay by scanning a QR code or showing your barcode. Alipay adds no fees on foreign cards. Steps, the one mistake, a phrase to show.",
                   "How to use Alipay in China as a foreigner"),
        "apps": ("Apps to Download Before Traveling to China (2026 Checklist)",
                 "Alipay, WeChat, Amap, Trip.com, Google Translate's offline pack and a roaming eSIM: what each one replaces and what to set up at home, before you are on a Chinese network.",
                 "6 apps to download before you travel to China"),
        "esim": ("Internet in China for Tourists: Roaming eSIM, No VPN Needed",
                 "Google, LINE and KakaoTalk are blocked on local Chinese networks. A roaming eSIM routes your data through your home country, so they work without a VPN. What to buy, when to activate, the hotel Wi-Fi catch.",
                 "Internet in China: use a roaming eSIM, skip the VPN"),
        "metro": ("How to Ride the Metro in China: Alipay QR, Security Check, Last Trains",
                  "Beijing and Shanghai metro for first-timers: the bag X-ray at every entrance, riding with an Alipay transport QR code, single tickets, escalator etiquette and the 23:00 last-train trap. 3–7 RMB a ride.",
                  "How to ride the metro in China"),
        "bike": ("How to Ride a Shared Bike in China with Alipay (Meituan, HelloBike)",
                 "Unlock Meituan, HelloBike or Qingju bikes inside Alipay, no extra app. Scan, ride, park in the zone, lock. About 1.5 RMB per 15 minutes, and the parking mistake that costs 2–5 RMB.",
                 "How to ride a shared bike in China"),
        "xlb": ("How to Eat Xiaolongbao (Soup Dumplings) Without Burning Your Mouth",
                "Lift it onto the spoon, bite a small hole, sip the soup, then dip in black vinegar with ginger. The four steps, where to eat them in Shanghai, and the one mistake that burns your lip.",
                "How to eat xiaolongbao, Shanghai's soup dumplings"),
        "douzhi": ("How to Drink Douzhi in Beijing (Fermented Mung Bean Drink)",
                   "Douzhi smells sour and tastes like old Beijing. Order a small bowl with jiaoquan and pickles, drink it hot, and know where to go: the Temple of Heaven north gate. 3–5 RMB a bowl.",
                   "How to drink douzhi, Beijing's fermented mung bean drink"),
        "hotpot": ("Sichuan Hotpot Dipping Sauce: How Locals Make the Oil Dish",
                   "In Chengdu hotpot you mix your own dip: sesame oil, garlic, coriander, a few drops of oyster sauce. Plus how to order half-and-half mild and how long to cook tripe. 100–150 RMB per person.",
                   "How to make a Sichuan hotpot dipping sauce like a local"),
        "water": ("Hot Water in China: Why You Get It, and Can You Drink Tap Water?",
                  "Ask for water in China and it arrives hot. How to ask for room-temperature water, where to refill free on trains and in stations, and why you should not drink the tap water.",
                  "Why everyone in China hands you hot water"),
        "toilet": ("Public Toilets in China: Squat Toilets, Tissues and Paper Bins",
                   "Public toilets in China are free and everywhere, but half have no paper and some are squat toilets. Carry tissues, know which toilets are best, and where the used paper goes.",
                   "Public toilets in China: the rules nobody writes down"),
    },
    "ja": {
        "alipay": ("外国人のAlipay（アリペイ）の使い方｜中国旅行の設定とQR決済（2026年）",
                   "出発前にAlipayにVisa・Mastercard・JCBを登録してパスポート認証。現地ではQRを読み取るか、バーコードを見せるだけ。海外カードでもAlipayの手数料はなし。手順・NG・見せるフレーズ付き。",
                   "外国人のためのAlipay（アリペイ）の使い方"),
        "apps": ("中国旅行前に入れておくアプリ6選（2026年）｜Alipay・WeChat・地図・翻訳",
                 "Alipay、WeChat、Amap（高徳地図）、Trip.com、Google翻訳のオフラインパック、ローミングeSIM。それぞれ何の代わりになり、出発前に自宅で何を済ませるか。",
                 "中国旅行の前に入れておくアプリ6つ"),
        "esim": ("中国のネット事情｜ローミングeSIMならVPNなしでGoogle・LINEが使える",
                 "中国の現地回線ではGoogleやLINEが遮断されます。自国経由のローミングeSIMならVPNなしでそのまま使えます。買う場所、有効化のタイミング、ホテルWi-Fiの落とし穴。",
                 "中国のネットは、ローミングeSIMでVPN不要"),
        "metro": ("中国の地下鉄の乗り方｜AlipayのQR乗車・手荷物検査・終電",
                  "北京・上海の地下鉄を初めて使う人へ。駅入口のX線検査、Alipayの乗車QRコード、1回券の買い方、エスカレーターのマナー、23時ごろの終電。1回3〜7元。",
                  "中国の地下鉄の乗り方"),
        "bike": ("中国のシェア自転車の乗り方｜Alipayで解錠（美団・ハロー・青桔）",
                 "美団・ハロー・青桔の自転車はAlipayの中から解錠でき、別アプリは不要。スキャン、乗車、エリア内に駐輪、施錠。15分約1.5元。2〜5元の罰金になるNGも。",
                 "中国のシェア自転車の乗り方"),
        "xlb": ("小籠包の食べ方｜上海でやけどしない4ステップ",
                "そっと持ち上げてレンゲへ、横に小さな穴、スープを吸ってから黒酢と生姜で。4つの手順、上海で食べる店、唇をやけどする典型的なNG。",
                "上海の小籠包の食べ方"),
        "douzhi": ("北京・豆汁（ドウジー）の飲み方｜焦圈と漬物で、熱いうちに",
                   "においは酸っぱい、味は北京そのもの。小碗に焦圈と漬物を添えて、熱いうちに一口。天壇公園北門の店ほか、1杯3〜5元。",
                   "北京の豆汁（ドウジー）の飲み方"),
        "hotpot": ("四川火鍋のつけダレの作り方｜地元流の油碟（ごま油ダレ）",
                   "成都の火鍋はタレを自分で作る。ごま油、にんにく、パクチー、オイスターソース数滴。鴛鴦鍋を微辣で頼む方法、毛肚を煮る秒数も。1人100〜150元。",
                   "四川火鍋のつけダレ、地元流の作り方"),
        "water": ("中国で熱いお湯が出てくる理由｜常温の頼み方と水道水",
                  "中国で水を頼むと熱湯が来る。常温の水の頼み方、列車や駅の無料の給湯器、そして水道水は飲めないこと。",
                  "なぜ中国では熱いお湯が出てくるのか"),
        "toilet": ("中国の公衆トイレ事情｜しゃがみ式・ティッシュ・紙はゴミ箱へ",
                   "中国の公衆トイレは無料でどこにでもあるが、半分は紙がなく、しゃがみ式も。ティッシュの携帯、きれいなトイレの探し方、使った紙の捨て方。",
                   "中国の公衆トイレ、誰も書かないルール"),
    },
    "ko": {
        "alipay": ("외국인 알리페이 사용법｜중국 여행 설정과 QR 결제 (2026)",
                   "출발 전 알리페이에 비자·마스터카드를 등록하고 여권 인증. 현지에서는 QR을 스캔하거나 바코드를 보여주면 끝. 해외 카드도 알리페이 수수료 없음. 순서, 금지 사항, 보여줄 문장까지.",
                   "외국인을 위한 알리페이 사용법"),
        "apps": ("중국 여행 전 필수 앱 6가지 (2026)｜알리페이·위챗·지도·번역",
                 "알리페이, 위챗, 아맵(가오더지도), 트립닷컴, 구글 번역 오프라인 팩, 로밍 eSIM. 각각 무엇을 대신하고, 출발 전에 집에서 무엇을 끝내야 하는지.",
                 "중국 여행 전에 깔아둘 앱 6가지"),
        "esim": ("중국 인터넷｜로밍 eSIM이면 VPN 없이 구글·카카오톡",
                 "중국 현지 망에서는 구글과 카카오톡이 차단됩니다. 본국을 거치는 로밍 eSIM이면 VPN 없이 그대로 됩니다. 어디서 사고 언제 켜는지, 호텔 와이파이의 함정까지.",
                 "중국 인터넷, 로밍 eSIM이면 VPN 필요 없음"),
        "metro": ("중국 지하철 타는 법｜알리페이 QR 승차·보안 검색·막차",
                  "베이징·상하이 지하철이 처음이라면. 역 입구 X선 검사, 알리페이 승차 QR, 1회권 사는 법, 에스컬레이터 매너, 밤 11시 무렵 막차. 1회 3~7위안.",
                  "중국 지하철 타는 법"),
        "bike": ("중국 공유자전거 타는 법｜알리페이로 잠금 해제 (메이퇀·헬로바이크)",
                 "메이퇀, 헬로바이크, 칭쥐 자전거는 알리페이 안에서 잠금 해제, 별도 앱 필요 없음. 스캔, 주행, 구역 안 주차, 잠금. 15분 약 1.5위안. 2~5위안 벌금이 붙는 실수까지.",
                 "중국 공유자전거 타는 법"),
        "xlb": ("샤오롱바오 먹는 법｜상하이에서 입 안 데는 4단계",
                "살짝 들어 숟가락에, 옆에 작은 구멍, 국물 먼저 마시고 흑초와 생강채에 찍어서. 네 단계, 상하이에서 먹을 곳, 입술 데는 대표적인 실수.",
                "상하이 샤오롱바오 먹는 법"),
        "douzhi": ("베이징 더우즈(豆汁) 마시는 법｜자오취안·절임과 뜨거울 때",
                   "냄새는 시큼, 맛은 베이징 그 자체. 작은 그릇에 자오취안과 절임을 곁들여 뜨거울 때 한 모금. 천단공원 북문 가게 등, 한 그릇 3~5위안.",
                   "베이징 더우즈 마시는 법"),
        "hotpot": ("쓰촨 훠궈 소스 만드는 법｜현지인의 참기름 소스(油碟)",
                   "청두 훠궈는 소스를 직접 만든다. 참기름, 다진 마늘, 고수, 굴소스 몇 방울. 반반 냄비를 웨이라로 주문하는 법, 천엽 익히는 시간까지. 1인 100~150위안.",
                   "쓰촨 훠궈 소스, 현지인처럼 만드는 법"),
        "water": ("중국에서 뜨거운 물을 주는 이유｜상온 물 주문법과 수돗물",
                  "중국에서 물을 달라고 하면 뜨거운 물이 나온다. 상온 물 달라는 법, 기차와 역의 무료 온수기, 그리고 수돗물은 마시지 않는다는 것.",
                  "중국에서는 왜 다들 뜨거운 물을 줄까"),
        "toilet": ("중국 공중화장실 이용법｜쪼그려 앉는 변기·휴지·휴지통",
                   "중국 공중화장실은 무료이고 어디에나 있지만 절반은 휴지가 없고 쪼그려 앉는 변기도 있다. 휴지 챙기기, 좋은 화장실 찾기, 쓴 휴지 버리는 곳.",
                   "중국 공중화장실, 아무도 안 적어둔 규칙"),
    },
}

HUB_META = {
    "en": ("China Travel Guide for First-Timers: {n} Practical How-Tos (2026)",
           "Practical China how-tos for first-time visitors: using Alipay as a foreigner, apps to download, eSIM internet, the metro, shared bikes, xiaolongbao, douzhi, hotpot sauce, hot water and public toilets.",
           "China how-to guides for first-timers",
           "The small things nobody explains, one page each. Free to read. The steps, where to go, the one mistake, and a Chinese phrase to show."),
    "ja": ("はじめての中国旅行ガイド：Alipay・アプリ・地下鉄・小籠包まで{n}テーマ（2026年）",
           "はじめての中国旅行の実用ガイド。外国人のAlipayの使い方、入れておくアプリ、eSIMとネット、地下鉄、シェア自転車、小籠包、豆汁、火鍋のタレ、お湯、公衆トイレ。",
           "はじめての中国、テーマ別ガイド",
           "誰も教えてくれない小さなことを、1テーマ1ページで。無料で読めます。手順、場所、NG、見せる中国語フレーズ。"),
    "ko": ("처음 가는 중국 여행 가이드: 알리페이·앱·지하철·샤오롱바오까지 {n}가지 (2026)",
           "처음 가는 중국 여행 실용 가이드. 외국인 알리페이 사용법, 깔아둘 앱, eSIM과 인터넷, 지하철, 공유자전거, 샤오롱바오, 더우즈, 훠궈 소스, 뜨거운 물, 공중화장실.",
           "처음 가는 중국, 주제별 가이드",
           "아무도 안 알려주는 작은 것들을 주제마다 한 페이지로. 무료로 읽을 수 있습니다. 순서, 장소, 금지 사항, 보여줄 중국어 문장."),
}

UI = {
    "en": dict(guides="Guides", steps="Step by step", where="Where to go", mistake="The one mistake", say="Show this to staff",
               setup="Set this up at home first", also="Also useful", before="Before you fly", related="Related guides",
               visa_h="Do you need a visa?", visa_p="Check your passport against China's official lists.",
               visa_all="All passports", visa_tr="240-hour transit", price="Price", city="City", zh="In Chinese",
               published="Published {d}", photo="Photo:", site="Official site", ask="Questions people ask",
               groups={"money": "Money, apps and internet", "move": "Getting around", "food": "Food", "daily": "Everyday"},
               cta_h="Want every hour planned? The full guide is US$2.",
               cta_p="Everything on this page is free. The full 7-day guide adds:",
               cta_locked="Also unlocks these cards: {titles}", cta_btn="See the full guide · US$2",
               apps_intro="Six apps, all free. Each one replaces something you would use at home."),
    "ja": dict(guides="ガイド", steps="手順", where="どこで", mistake="やってはいけない1つ", say="店員さんに見せるフレーズ",
               setup="先に自宅で設定しておくもの", also="あわせて使うもの", before="出発前に", related="関連ガイド",
               visa_h="中国のビザは必要？", visa_p="中国の公式リストでパスポートごとに確認できます。",
               visa_all="すべての国", visa_tr="240時間トランジット", price="値段", city="都市", zh="中国語",
               published="{d}公開", photo="写真：", site="公式サイト", ask="よくある質問",
               groups={"money": "お金・アプリ・ネット", "move": "移動", "food": "食べる", "daily": "日常"},
               cta_h="1時間単位の完全版は2ドル。",
               cta_p="このページの内容は無料です。7日間の完全版には：",
               cta_locked="さらに解除されるカード：{titles}", cta_btn="完全版を見る · 2ドル",
               apps_intro="6つとも無料。それぞれ、普段使っている何かの代わりになります。"),
    "ko": dict(guides="가이드", steps="순서", where="어디서", mistake="하지 말아야 할 한 가지", say="직원에게 보여줄 문장",
               setup="먼저 집에서 설정해 둘 것", also="함께 쓰면 좋은 것", before="출발 전에", related="관련 가이드",
               visa_h="중국 비자, 필요할까?", visa_p="중국 공식 목록으로 여권별로 확인할 수 있습니다.",
               visa_all="전체 국가", visa_tr="240시간 경유", price="가격", city="도시", zh="중국어",
               published="{d} 게시", photo="사진:", site="공식 사이트", ask="자주 묻는 질문",
               groups={"money": "돈·앱·인터넷", "move": "이동", "food": "먹기", "daily": "일상"},
               cta_h="시간 단위 전체 가이드는 2달러.",
               cta_p="이 페이지 내용은 무료입니다. 7일 전체 가이드에는:",
               cta_locked="추가로 열리는 카드: {titles}", cta_btn="전체 가이드 보기 · 2달러",
               apps_intro="6개 모두 무료. 각각 평소 쓰던 무언가를 대신합니다."),
}
# Visa pages linked from every guide. EN: the biggest markets plus Italy (already ranks); JA/KO: their own page.
VISA_LINKS = {"en": ["united-states", "united-kingdom", "canada", "australia", "germany", "italy", "japan", "south-korea"],
              "ja": ["japan"], "ko": ["south-korea"]}


# ------------------------------------------------------------------ data
def js_literal_to_json(src):
    """Turn a JS object/array literal (unquoted keys, comments, trailing commas) into JSON text. String-aware."""
    out, i, n = [], 0, len(src)
    while i < n:
        ch = src[i]
        if ch in "\"'":
            j, buf = i + 1, []
            while src[j] != ch:
                if src[j] == "\\":
                    buf.append(src[j:j + 2]); j += 2; continue
                buf.append(src[j]); j += 1
            body = "".join(buf)
            if ch == "'":
                body = body.replace("\\'", "'").replace('"', '\\"')
            out.append('"%s"' % body); i = j + 1; continue
        if src.startswith("//", i):
            i = src.index("\n", i); continue
        if src.startswith("/*", i):
            i = src.index("*/", i) + 2; continue
        m = re.match(r"[A-Za-z_$][\w$]*", src[i:i + 80])
        if m:
            word, k = m.group(0), i + len(m.group(0))
            while k < n and src[k] in " \t\r\n":
                k += 1
            out.append('"%s"' % word if k < n and src[k] == ":" else word)
            i += len(word); continue
        if ch in "}]":
            k = len(out) - 1
            while k >= 0 and out[k].isspace():
                k -= 1
            if k >= 0 and out[k] == ",":
                out[k] = ""
        out.append(ch); i += 1
    return "".join(out)


def load_js(path, marker):
    src = io.open(path, encoding="utf-8").read()
    start = src.index(marker) + len(marker)
    body = src[start:].strip().rstrip(";")
    return json.loads(js_literal_to_json(body))


CONTENT = {l: load_js("content-%s.js" % l, "window.CONTENT.%s =" % l) for l in LANGS}
CREDITS = {c["id"]: c for c in load_js("images/credits.js", "window.PHOTO_CREDITS =")}
I18N = B.load_i18n()


def card(lang, cid):
    c = next(x for x in CONTENT[lang]["cards"] if x["id"] == cid)
    assert not c.get("locked"), "guide pages may only use free cards: %s" % cid
    return c


def app(lang, aid):
    return next(x for x in CONTENT[lang]["apps"] if x["id"] == aid)


def label(lang, gid):
    return I18N[lang]["guides.all" if gid == "all" else "guide." + gid]


def guide_path(lang, slug):
    return HUB[lang] + slug + ".html"


def alts_for(g):
    return {l: guide_path(l, g["slug"]) for l in LANGS}


def entries():
    """Every guide page as (path, {lang: path}), for the sitemap."""
    out = [(HUB[l], dict(HUB)) for l in LANGS]
    for g in GUIDES:
        out += [(guide_path(l, g["slug"]), alts_for(g)) for l in LANGS]
    return out


# ------------------------------------------------------------------ html pieces
def say_card(say, lang):
    tap = V.UI[lang]["tap"]
    return ('<div class="say-stack"><button type="button" class="say-card" data-say="%s" data-say-pinyin="%s"><span class="say-zh">%s</span>'
            '<span class="say-pinyin">%s</span><span class="say-meaning">%s</span><span class="say-hint">%s</span></button></div>'
            % (e(say["zh"]), e(say["py"]), e(say["zh"]), e(say["py"]), e(say["en"]), e(tap)))


def app_box(lang, a, heading_level="h3"):
    t = I18N[lang]
    return ('<article class="app" id="app-%s"><span class="app-mark" aria-hidden="true">%s</span>'
            '<div class="app-head"><%s class="app-name">%s</%s><span class="app-zh">%s</span><span class="app-tag">%s</span></div>'
            '<p class="app-what">%s</p><dl class="app-rows"><div class="app-row"><dt>%s</dt><dd class="app-setup">%s</dd></div>'
            '<div class="app-row"><dt>%s</dt><dd>%s</dd></div></dl>'
            '<a class="app-site" href="%s" target="_blank" rel="noopener">%s</a></article>'
            % (e(a["id"]), e(a["mark"]), heading_level, e(a["name"]), heading_level, e(a["zh"]), e(a["tag"]), e(a["what"]),
               e(t["apps.doNow"]), e(a["setup"]), e(t["apps.why"]), e(a["why"]), e(a["site"]), e(t["apps.open"])))


def picture(cid, alt, eager=True):
    return ('<picture><source type="image/avif" srcset="/images/{i}-400.avif 400w, /images/{i}-800.avif 800w" sizes="(max-width: 720px) calc(100vw - 32px), 760px">'
            '<img src="/images/{i}-800.jpg" alt="{a}" width="1200" height="800"{l}></picture>').format(
        i=e(cid), a=e(alt), l=' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"')


def credit_html(lang, cid):
    c = CREDITS.get(cid)
    if not c:
        return ""
    return '<figcaption>%s <a href="%s" target="_blank" rel="noopener license">%s</a>, %s</figcaption>' % (
        e(UI[lang]["photo"]), e(c["page"]), e(c["author"]), e(c["license"]))


def related_html(lang, g):
    items = []
    for rid in g["related"]:
        r = BY_ID[rid]
        items.append('<a href="%s">%s</a>' % (guide_path(lang, r["slug"]), e(label(lang, rid))))
    items.append('<a href="%s">%s →</a>' % (HUB[lang], e(label(lang, "all"))))
    return '<section class="prose"><h2>%s</h2><div class="chips-links">%s</div></section>' % (e(UI[lang]["related"]), "".join(items))


def visa_html(lang):
    u = UI[lang]
    by = {c["slug"]: c for c in D.COUNTRIES}
    links = []
    for slug in VISA_LINKS[lang]:
        c = by[slug]
        links.append('<a href="%s">%s</a>' % (V.country_url(lang, slug), e(c["en"] if lang == "en" else c[lang])))
    links.append('<a href="%s">%s</a>' % (V.TRANSIT[lang], e(u["visa_tr"])))
    links.append('<a href="%s">%s →</a>' % (V.HUB[lang], e(u["visa_all"])))
    return '<section class="prose"><h2>%s</h2><p>%s</p><div class="chips-links">%s</div></section>' % (
        e(u["visa_h"]), e(u["visa_p"]), "".join(links))


def cta_html(lang):
    u, c = UI[lang], CONTENT[lang]
    paid_tier = next(t for t in c["tiers"] if t.get("cta") == "buy")
    items = [x for x in paid_tier["items"] if "WhatsApp" not in x][:5]   # the group is hidden until a real link exists
    locked = [x["title"] for x in c["cards"] if x.get("locked")]
    return ('<aside class="v-cta"><div><h2>%s</h2><p>%s</p><ul class="v-cta-list">%s</ul><p class="v-cta-locked">%s</p></div>'
            '<a class="btn" href="%s#pricing">%s</a></aside>'
            % (e(u["cta_h"]), e(u["cta_p"]), "".join("<li>%s</li>" % e(x) for x in items),
               e(u["cta_locked"].format(titles=" · ".join(locked))), HOME[lang], e(u["cta_btn"])))


def faq_html(lang, idxs):
    if not idxs:
        return ""
    faq = CONTENT[lang]["faq"]
    body = "".join('<details open><summary>%s</summary><div class="faq-body"><p>%s</p></div></details>' % (e(faq[i]["q"]), e(faq[i]["a"])) for i in idxs)
    return '<section class="prose v-faq"><h2>%s</h2><div class="faq">%s</div></section>' % (e(UI[lang]["before"]), body)


# ------------------------------------------------------------------ page shell
def shell(lang, path, title, desc, body, alternates, graph, crumbs, og_image):
    crumb = " / ".join('<a href="%s">%s</a>' % (h, e(t)) for t, h in crumbs[:-1]) + " / " + e(crumbs[-1][0])
    t = I18N[lang]
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
{fonts}
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}{path}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="China Visit">
<meta property="og:image" content="{site}{og_image}">
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
<main class="v-main g-main">
<p class="crumbs">{crumb}</p>
{body}
</main>
<footer class="foot">
  <div class="foot-brand">
    <span class="brand-zh">小碗</span>
    <p class="v-foot"><a href="{home}">{home_t}</a><a href="{hub}">{hub_t}</a><a href="{visa}">{visa_t}</a><a href="mailto:86886779@qq.com?subject=China%20Visit">86886779@qq.com</a></p>
  </div>
  <p class="foot-legal">{legal}</p>
</footer>
{overlay}
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "3685ef96a9c6460796e8590ef74cd9d0"}}'></script>
</body>
</html>
""".format(lang=lang, title=e(title), desc=e(desc), site=SITE, path=path, alts=V.alt_links_html(alternates), fonts=V.font_links(lang),
           og_image=og_image, v=V.ASSET_V, graph=json.dumps(graph, ensure_ascii=False).replace("</", "<\\/"), home=HOME[lang], svg=V.BRAND_SVG,
           nav=V.nav_html(lang, "guide"), switch=V.switch_html(lang, alternates, HUB), crumb=crumb, body=body,
           home_t=e(V.UI[lang]["home"]), hub=HUB[lang], hub_t=e(UI[lang]["guides"]), visa=V.HUB[lang], visa_t=e(V.UI[lang]["hub"]),
           legal=e(t["foot.legal"]), overlay=V.say_overlay_html(lang))


def breadcrumbs_ld(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": t, "item": SITE + h} for i, (t, h) in enumerate(crumbs)]}


PUBLISHER = {"@type": "Organization", "name": "China Visit", "url": SITE + "/",
             "logo": {"@type": "ImageObject", "url": SITE + "/images/logo-512.png", "width": 512, "height": 512}}


# ------------------------------------------------------------------ pages
def article(lang, g):
    u, t = UI[lang], I18N[lang]
    title, desc, h1 = META[lang][g["id"]]
    path = guide_path(lang, g["slug"])
    c = card(lang, g["card"]) if g.get("card") else None
    main_app = app(lang, g["main_app"]) if g.get("main_app") else None
    date = V.fmt_date(UPDATED, lang)

    if c:
        lede = c["hook"]
    elif main_app:
        lede = main_app["what"]
    else:
        lede = t["apps.sub"]
    head = ['<header class="v-head"><p class="g-kicker"><span class="g-mark">%s</span>%s</p><h1>%s</h1><p class="lede">%s</p>'
            '<p class="checked"><time datetime="%s">%s</time></p></header>' % (
                e(g["mark"]), e(CONTENT[lang]["cityNames"][c["city"]]) if c else e(u["guides"]), e(h1), e(lede), UPDATED,
                e(u["published"].format(d=date)))]
    parts = []
    if c:
        parts.append('<section class="verdict g-facts"><div class="facts" style="border-top:0;margin-top:0">'
                     '<div class="fact"><b>%s</b><span>%s</span></div><div class="fact"><b>%s</b><span>%s</span></div>'
                     '<div class="fact"><b lang="zh">%s</b><span>%s</span></div></div></section>' % (
                         e(c["price"]), e(u["price"]), e(CONTENT[lang]["cityNames"][c["city"]]), e(u["city"]), e(c["zh"]), e(u["zh"])))
        parts.append('<figure class="g-photo">%s%s</figure>' % (picture(c["id"], c["title"]), credit_html(lang, c["id"])))
    prose = []
    if g.get("setup"):
        prose.append('<h2>%s</h2><div class="apps g-apps">%s</div>' % (e(u["setup"]), "".join(app_box(lang, app(lang, a)) for a in g["setup"])))
    if c:
        prose.append('<h2>%s</h2><ol class="steps g-steps">%s</ol>' % (e(u["steps"]), "".join("<li>%s</li>" % e(s) for s in c["steps"])))
        prose.append('<h2>%s</h2><p>%s</p>' % (e(u["where"]), e(c["where"])))
        prose.append('<h2>%s</h2><p class="note g-mistake">%s</p>' % (e(u["mistake"]), e(c["mistake"])))
        prose.append('<h2>%s</h2>%s' % (e(u["say"]), say_card(c["say"], lang)))
    if main_app:
        prose.append('<h2>%s</h2><p>%s</p>' % (e(t["apps.doNow"]), e(main_app["setup"])))
        prose.append('<h2>%s</h2><p>%s</p>' % (e(t["apps.why"]), e(main_app["why"])))
        prose.append('<p><a href="%s" target="_blank" rel="noopener">%s: %s</a></p>' % (e(main_app["site"]), e(main_app["name"]), e(main_app["site"])))
    if g.get("app_list"):
        prose.append('<p>%s</p>' % e(u["apps_intro"]))
        prose.append('<div class="apps g-apps g-apps-list">%s</div>' % "".join(app_box(lang, a, "h2") for a in CONTENT[lang]["apps"]))
        prose.append('<p class="note">%s</p>' % e(t["apps.note"]))
    if g.get("also"):
        prose.append('<h2>%s</h2><div class="apps g-apps">%s</div>' % (e(u["also"]), "".join(app_box(lang, app(lang, a)) for a in g["also"])))
    parts.append('<section class="prose">%s</section>' % "".join(prose))
    parts.append(faq_html(lang, g["faq"]))
    parts.append(cta_html(lang))
    parts.append(related_html(lang, g))
    parts.append(visa_html(lang))
    body = '<article class="g-article">%s%s</article>' % ("".join(head), "\n".join(p for p in parts if p))

    crumbs = [(V.UI[lang]["home"], HOME[lang]), (u["guides"], HUB[lang]), (label(lang, g["id"]), path)]
    img = SITE + ("/images/%s.jpg" % c["id"] if c else "/images/tiantan.jpg")
    art = {"@type": "Article", "@id": SITE + path + "#article", "headline": h1, "description": desc, "inLanguage": lang,
           "image": [img], "datePublished": UPDATED, "dateModified": UPDATED, "author": {"@type": "Organization", "name": "China Visit", "url": SITE + "/"},
           "publisher": PUBLISHER, "mainEntityOfPage": {"@type": "WebPage", "@id": SITE + path},
           "isPartOf": {"@type": "WebSite", "name": "China Visit", "url": SITE + "/"}}
    graph = {"@context": "https://schema.org", "@graph": [art, breadcrumbs_ld(crumbs)]}
    return path, shell(lang, path, title, desc, body, alts_for(g), graph, crumbs, img[len(SITE):])


def index(lang):
    u = UI[lang]
    title, desc, h1, lede = HUB_META[lang]
    title = title.format(n=len(GUIDES))
    path = HUB[lang]
    parts = ['<header class="v-head"><h1>%s</h1><p class="lede">%s</p></header>' % (e(h1), e(lede))]
    for gkey, ids in GROUPS:
        tiles = []
        for gid in ids:
            g = BY_ID[gid]
            if g.get("card"):
                c = card(lang, g["card"])
                thumb, blurb = picture(c["id"], c["title"], eager=False), c["hook"]
            else:
                a = app(lang, g["main_app"]) if g.get("main_app") else None
                thumb = '<span class="g-tile-mark" aria-hidden="true">%s</span>' % e(g["mark"])
                blurb = a["what"] if a else I18N[lang]["apps.sub"]
            tiles.append('<a class="g-tile" href="%s">%s<span class="g-tile-text"><b>%s</b><span>%s</span></span></a>' % (
                guide_path(lang, g["slug"]), thumb, e(label(lang, gid)), e(blurb)))
        parts.append('<section class="g-group"><h2>%s</h2><div class="g-tiles">%s</div></section>' % (e(u["groups"][gkey]), "".join(tiles)))
    parts.append(cta_html(lang))
    parts.append(visa_html(lang))
    crumbs = [(V.UI[lang]["home"], HOME[lang]), (u["guides"], path)]
    items = [{"@type": "ListItem", "position": i + 1, "url": SITE + guide_path(lang, BY_ID[gid]["slug"]), "name": label(lang, gid)}
             for i, gid in enumerate(gid for _, ids in GROUPS for gid in ids)]
    coll = {"@type": "CollectionPage", "@id": SITE + path, "url": SITE + path, "name": title, "description": desc, "inLanguage": lang,
            "isPartOf": {"@type": "WebSite", "name": "China Visit", "url": SITE + "/"}, "publisher": PUBLISHER, "dateModified": UPDATED,
            "mainEntity": {"@type": "ItemList", "itemListElement": items}}
    graph = {"@context": "https://schema.org", "@graph": [coll, breadcrumbs_ld(crumbs)]}
    return path, shell(lang, path, title, desc, "\n".join(parts), dict(HUB), graph, crumbs, "/images/tiantan.jpg")


# ------------------------------------------------------------------ homepage link block (index.html; build.py localises it)
HOME_START, HOME_END = "<!--guides:start (generated by build_guides.py, do not edit by hand)-->", "<!--guides:end-->"


def home_block():
    t = I18N["en"]
    links = "".join(
        '<li><a href="guide/{p}" data-guide="{c}" data-guide-path="{p}"><span class="guide-zh" lang="zh">{m}</span>'
        '<span data-i18n="guide.{i}">{l}</span></a></li>'.format(
            p=g["slug"] + ".html", c=" ".join(g.get("home") or [g.get("card") or g.get("main_app") or g["id"]]), m=e(g["mark"]), i=g["id"], l=e(label("en", g["id"])))
        for g in (BY_ID[i] for _, ids in GROUPS for i in ids))
    return ('%s\n  <section class="section guides-sec" id="guides">\n    <div class="section-head">\n'
            '      <h2 data-i18n="guides.title">%s</h2>\n      <p data-i18n="guides.sub">%s</p>\n    </div>\n'
            '    <ul class="guide-links">%s</ul>\n'
            '    <p class="guides-all"><a class="btn btn-ghost btn-small" href="guide/" data-guide-path="" data-i18n="guides.all">%s</a></p>\n'
            '  </section>\n  %s' % (HOME_START, e(t["guides.title"]), e(t["guides.sub"]), links, e(t["guides.all"]), HOME_END))


def update_home():
    src = io.open("index.html", encoding="utf-8").read()
    a, b = src.index(HOME_START), src.index(HOME_END) + len(HOME_END)
    out = src[:a] + home_block() + src[b:]
    if out != src:
        io.open("index.html", "w", encoding="utf-8", newline="\n").write(out)


# ------------------------------------------------------------------ guard: nothing from the paid files
def check_no_paid(pages):
    paid_text = io.open("content-paid-en.js", encoding="utf-8").read() + io.open("content-paid-ja.js", encoding="utf-8").read() + \
        io.open("content-paid-ko.js", encoding="utf-8").read()
    free_text = "".join(io.open("content-%s.js" % l, encoding="utf-8").read() for l in LANGS)
    # every quoted sentence of 25+ chars in the paid files that is not also in the free files
    paid = set(s for s in re.findall(r'"([^"\\]{25,})"', paid_text) if s not in free_text)
    assert paid, "could not read the paid files"
    for path, text in pages:
        plain = text.replace("&#x27;", "'").replace("&quot;", '"').replace("&amp;", "&")
        hits = [s for s in paid if s in plain]
        assert not hits, "%s contains paid content: %r" % (path, hits[:2])


def write(path, text):
    fs = path.lstrip("/")
    if fs.endswith("/"):
        fs += "index.html"
    os.makedirs(os.path.dirname(fs), exist_ok=True)
    io.open(fs, "w", encoding="utf-8", newline="\n").write(text)


def main():
    pages = [index(l) for l in LANGS] + [article(l, g) for g in GUIDES for l in LANGS]
    assert [p for p, _ in pages] == [p for p, _ in (entries()[:3] + [(x, 0) for x, _ in entries()[3:]])]
    check_no_paid(pages)
    for path, text in pages:
        write(path, text)
    update_home()
    V.write_sitemap()
    i18n = B.load_i18n()
    for lang in ("ja", "ko"):
        io.open("%s.html" % lang, "w", encoding="utf-8", newline="\n").write(B.build(lang, i18n))
    print("wrote %d guide pages, index.html guide block, ja.html, ko.html, sitemap.xml" % len(pages))


if __name__ == "__main__":
    main()
