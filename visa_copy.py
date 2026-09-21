# Page copy for build_visa.py. English covers every passport; Japanese and Korean cover the hub,
# the transit explainer and the home-country page (Japan / South Korea, both on the 30-day list).
import json

REGION_ORDER = ("eu", "as", "am", "oc", "me", "af")
STAY = {
    "en": {"30": "30 days", "30_90in180": "30 days per stay, 90 in any 180", "90in180": "90 days in any 180",
           "30_90peryear": "30 days per stay, 90 per year", "60": "60 days", "3m": "3 months"},
    "ja": {"30": "30日", "30_90in180": "1回30日・180日間で計90日", "90in180": "180日間で計90日",
           "30_90peryear": "1回30日・年間計90日", "60": "60日", "3m": "3か月"},
    "ko": {"30": "30일", "30_90in180": "1회 30일·180일 중 90일", "90in180": "180일 중 90일",
           "30_90peryear": "1회 30일·연간 90일", "60": "60일", "3m": "3개월"},
}
STAY_DAYS = {"30": "30", "30_90in180": "30", "90in180": "90", "30_90peryear": "30", "60": "60", "3m": "90"}
STAMP = {"unilateral": "免", "mutual": "免", "transit": "过", "visa": "签"}
VCLASS = {"unilateral": "is-free", "mutual": "is-free", "transit": "is-transit", "visa": "is-visa"}


def end_of(c, D):
    return c["end"] or D.UNILATERAL_END


def sorted_by(countries, lang):
    return sorted(countries, key=lambda c: c[lang] if lang != "en" else c["en"])


def verdict_html(cls, stamp, kicker, answer, detail, facts, e):
    fx = "".join('<div class="fact"><b>%s</b><span>%s</span></div>' % (e(a), e(b)) for a, b in facts)
    return ('<section class="verdict %s"><span class="verdict-stamp" aria-hidden="true">%s</span><p class="verdict-kicker">%s</p>'
            '<p class="verdict-answer">%s</p><p class="verdict-detail">%s</p>%s</section>'
            % (cls, stamp, e(kicker), e(answer), detail, '<div class="facts">%s</div>' % fx if facts else ""))


# =====================================================================================  COUNTRY
def country(lang, c, D, BY, country_url, fmt_date, say_cards, faq_block, cta, sources, e):
    if lang == "en":
        return _country_en(c, D, BY, country_url, fmt_date, say_cards, faq_block, cta, sources, e)
    return _country_local(lang, c, D, fmt_date, say_cards, faq_block, cta, sources, e)


def _related(c, D, country_url, e, lang="en"):
    same = [x for x in D.COUNTRIES if x["region"] == c["region"] and x["slug"] != c["slug"]][:10]
    links = "".join('<a href="%s">%s</a>' % (country_url(lang, x["slug"]), e(x["en"] if lang == "en" else x[lang])) for x in same)
    return links


def _country_en(c, D, BY, country_url, fmt_date, say_cards, faq_block, cta, sources, e):
    n, dem, s = c["en"], c["dem"], c["scheme"]
    checked = fmt_date(D.CHECKED, "en")
    body, faqs, srcs = [], [], []

    if s == "unilateral":
        end = end_of(c, D)
        end_txt = "It has no set end date." if end == "none" else "The policy currently runs until %s." % fmt_date(end, "en")
        title = "Do %s need a visa for China? No: 30 days visa-free (2026)" % dem
        desc = ("%s can enter China visa-free for up to 30 days for tourism, business, family visits or transit. "
                "Rules, end date, what to show at the border. Checked %s." % (dem, checked))
        short = "%s passport" % n
        body.append(verdict_html("is-free", "免", "%s passport · ordinary" % n, "No visa needed for stays up to 30 days.",
            "Under China's visa-free policy, %s passport holders can come for tourism, business, visiting family or friends, "
            "exchange visits or transit, for up to 30 days each time. %s" % (e(n), e(end_txt)),
            [("30 days", "per entry"), ("No end" if end == "none" else fmt_date(end, "en"), "policy end date"),
             ("No cap", "on number of entries"), ("Any port", "air, land or sea")], e))
        body.append("""<section class="prose">
<h2>How the 30 days are counted</h2>
<p>The clock starts at 00:00 on the day after you arrive. Land in Shanghai at 23:00 on 1 March and your 30 days run from 2 March to the end of 31 March. Leave on or before that date.</p>
<h2>What to have ready at the border</h2>
<ul>
<li><strong>An ordinary passport</strong> valid for your whole stay. Emergency and temporary travel documents do not qualify. Your airline may apply stricter validity checks, so ask them.</li>
<li><strong>Proof that matches your purpose.</strong> Officials recommend carrying a return or onward flight and your hotel bookings; for business, an invitation letter.</li>
<li><strong>The arrival card.</strong> Since November 2025 you can fill it in online before you land, instead of on paper in the hall.</li>
<li>You do not need to register with an embassy beforehand, and you can use any open airport, land crossing or seaport.</li>
</ul>
<h2>What visa-free entry does not cover</h2>
<ul>
<li><strong>Work, study and journalism</strong> need the right visa before you travel.</li>
<li><strong>Staying longer than 30 days:</strong> get a visa before you fly, or, with good reason, apply for an extension at the local public security exit-entry office once you are here.</li>
<li><strong>Repeat trips are fine.</strong> There is currently no limit on how many times you use it or on total days per year, as long as each trip matches an allowed purpose.</li>
</ul>
<h2>Show this at the counter</h2>
<p>Border officers at big airports speak English, but staff at smaller crossings and hotel desks may not. Tap a card to enlarge it.</p>
%s
</section>""" % say_cards("en", ["tourist", "visafree", "hotel", "return"]))
        faqs = [
            ("Can %s stay in China longer than 30 days without a visa?" % dem,
             "Not on one entry. You can leave and come back, since there is currently no cap on entries, or apply for an extension at a local exit-entry office if you have good reason. For a planned long stay, get a visa before you fly."),
            ("Is visa-free entry for %s permanent?" % dem,
             ("It has no set end date for now." if end == "none" else
              "No. It currently runs until %s. China has extended its visa-free list several times since 2023, but check again closer to that date." % fmt_date(end, "en"))),
            ("Can I work or study in China on visa-free entry?", "No. Visa-free entry covers tourism, business, visiting family or friends, exchange visits and transit. Work, study and journalism need a visa."),
            ("Do children with %s passports need a visa?" % n, "No. The same rules apply to children travelling on their own passport."),
        ]
        srcs = ["nia_unilateral", "embassy_faq"] + (["mfa_uk_ca"] if c["slug"] in ("united-kingdom", "canada") else []) + \
               (["mfa_russia"] if c["slug"] == "russia" else []) + ["arrival_card"]

    elif s == "mutual":
        days = STAY_DAYS[c["stay"]]
        since = (" in force since %s" % fmt_date(c["since"], "en")) if c["since"] else ""
        title = "Do %s need a visa for China? No: %s days visa-free (2026)" % (dem, days if c["stay"] != "3m" else "90")
        if c["stay"] == "3m":
            title = "Do %s need a visa for China? No: up to 3 months visa-free (2026)" % dem
        desc = "%s can visit China without a visa under a mutual exemption agreement: %s. Rules, limits and what to show at the border. Checked %s." % (dem, STAY["en"][c["stay"]], checked)
        short = "%s passport" % n
        body.append(verdict_html("is-free", "免", "%s passport · ordinary" % n, "No visa needed: %s." % STAY["en"][c["stay"]],
            "China and %s have a mutual visa exemption agreement for ordinary passports%s. Unlike China's one-sided visa-free list, "
            "an agreement has no end date, though either side can suspend it." % (e(n), e(since)),
            [{"3m": ("3 months", "max stay"), "90in180": ("90 days", "in any 180")}.get(c["stay"], (STAY_DAYS[c["stay"]] + " days", "per stay")), ("Agreement", "no end date"),
             ("240h" if c["transit"] else "—", "transit also available" if c["transit"] else "not on transit list")], e))
        body.append("""<section class="prose">
<h2>What to have ready at the border</h2>
<ul>
<li><strong>An ordinary passport</strong> valid for your whole stay. Your airline may apply stricter validity checks.</li>
<li><strong>A return or onward ticket and your hotel bookings.</strong> You may be asked about your plans.</li>
<li><strong>The arrival card.</strong> Since November 2025 you can fill it in online before you land.</li>
</ul>
<h2>What it does not cover</h2>
<ul>
<li>Mutual exemption agreements are for short visits. <strong>Work, study and journalism</strong> need a visa.</li>
<li>If you plan to stay longer than the limit above, apply for a visa before you travel.</li>
</ul>
<h2>Show this at the counter</h2>
%s
</section>""" % say_cards("en", ["tourist", "visafree", "hotel", "return"]))
        faqs = [
            ("How long can %s stay in China without a visa?" % dem, "%s, under the mutual visa exemption agreement between China and %s." % (STAY["en"][c["stay"]].capitalize(), n)),
            ("Does the agreement expire?", "Mutual agreements have no end date, unlike China's one-sided visa-free list. Either country can suspend one, so check before long trips."),
            ("Can I work in China under the agreement?", "No. It covers short visits such as tourism, business and family visits. Work, study and journalism need a visa."),
        ]
        srcs = ["mfa_mutual", "nia_mutual", "arrival_card"]

    elif s == "transit":
        title = "Do %s need a visa for China? Yes, unless you use 240-hour transit (2026)" % dem
        desc = ("%s need a visa for China, but can stay up to 10 days visa-free on 240-hour transit to a third country. "
                "Routes that work, 24 provinces, rules. Checked %s." % (dem, checked))
        short = "%s passport" % n
        added = " %s was added to the list on %s." % (n, fmt_date(c["since"], "en")) if c["since"] else ""
        body.append(verdict_html("is-transit", "过", "%s passport · ordinary" % n, "You need a visa, unless you're flying on.",
            "%s is not on China's 30-day visa-free list. But %s passports qualify for <strong>240-hour visa-free transit</strong>: "
            "if you continue to a third country or region, you can spend up to 10 days in China without a visa.%s" % (e(n), e(n), e(added)),
            [("240 h", "max stay, transit only"), (str(D.TRANSIT_PORTS), "ports of entry"), (str(D.TRANSIT_PROVINCES), "provinces open"), ("3 months", "passport validity")], e))
        body.append("""<section class="prose">
<h2>How 240-hour transit works</h2>
<ol>
<li><strong>Arrive from one country, leave to a different one.</strong> The place you fly in from and the place you fly on to must be different countries or regions.</li>
<li><strong>Hold a confirmed onward ticket</strong> with a date and seat, leaving within 240 hours.</li>
<li><strong>Passport:</strong> an ordinary passport valid for at least 3 more months.</li>
<li><strong>Enter and leave through any of the %d designated ports</strong> (most big international airports, plus some rail, land and sea ports).</li>
<li><strong>Stay within the permitted areas of %d provinces.</strong> You can travel between them, for example Beijing to Shanghai by train.</li>
<li><strong>The clock starts at 00:00 the day after you arrive.</strong></li>
</ol>
<h2>Routes that work, and routes that don't</h2>
<div class="ctable-wrap"><table class="ctable">
<thead><tr><th>Route</th><th>Visa-free?</th></tr></thead>
<tbody>
<tr><td>%s → Shanghai → Tokyo</td><td><span class="pill free">Yes</span></td></tr>
<tr><td>Seoul → Beijing → %s</td><td><span class="pill free">Yes</span> (flying home counts, if you came from elsewhere)</td></tr>
<tr><td>%s → Shanghai → %s</td><td><span class="pill visa">No</span> round trip, same country both ways</td></tr>
<tr><td>%s → Beijing, stay 12 days → Tokyo</td><td><span class="pill visa">No</span> over 240 hours</td></tr>
</tbody></table></div>
<p class="note">Many travellers use a flight to Hong Kong or Macau as the onward leg. The official rule says "third country or region"; confirm with your airline before you book, because it checks your eligibility at check-in.</p>
<h2>Staying longer, or flying round-trip?</h2>
<p>Apply for a tourist (L) visa at a Chinese embassy, consulate or visa application service center before you fly. For single and double-entry visas of up to 180 days, fingerprints are currently waived and fees are reduced until 31 December 2026.</p>
%s
<h2>Show this at the counter</h2>
%s
<p>Full rules, the list of %d provinces and all 57 eligible passports: <a href="/visa/240-hour-transit.html">240-hour visa-free transit, explained</a>.</p>
</section>""" % (D.TRANSIT_PORTS, D.TRANSIT_PROVINCES, e(n), e(n), e(n), e(n), e(n),
                 _asean_note_en(c), say_cards("en", ["transit", "hotel"]), D.TRANSIT_PROVINCES))
        faqs = [
            ("Can %s visit China visa-free on a round-trip ticket?" % dem, "No. For 240-hour transit the onward flight must go to a different country or region from the one you arrived from. A return flight home works only if you arrived from somewhere else."),
            ("When does the 240-hour clock start?", "At 00:00 on the day after you arrive. You then have up to 240 hours, and your onward ticket must fall inside that window."),
            ("Can I travel around China on 240-hour transit?", "Yes, within the permitted areas of %d provinces and municipalities, including Beijing, Shanghai, Guangdong, Sichuan and Yunnan. You can move between them." % D.TRANSIT_PROVINCES),
            ("What passport validity do %s need?" % dem, "At least 3 months for 240-hour transit."),
        ]
        srcs = ["nia_transit", "transit_faq", "transit_areas", "arrival_card"] + (["asean_xsbn", "nia_regional"] if c["asean"] or c["slug"] in ("vietnam", "kyrgyzstan") else [])

    else:  # visa
        title = "Do %s need a visa for China? Yes: your options in 2026" % dem
        desc = ("%s need a visa for China: not on the visa-free, mutual exemption or 240-hour transit lists. "
                "How to apply, 24-hour transit and group-tour exceptions. Checked %s." % (dem, checked))
        short = "%s passport" % n
        body.append(verdict_html("is-visa", "签", "%s passport · ordinary" % n, "Yes. Apply for a visa before you fly.",
            "As of %s, %s is not on China's 30-day visa-free list, has no mutual exemption agreement for ordinary passports, "
            "and is not among the 57 countries eligible for 240-hour transit." % (e(checked), e(n)),
            [("L visa", "for tourism"), ("24 h", "airside transit only"), ("57", "transit countries (not incl. %s)" % n)], e))
        body.append("""<section class="prose">
<h2>Your options</h2>
<ul>
<li><strong>Tourist (L) visa.</strong> Apply at a Chinese embassy, consulate or Chinese visa application service center in your country. For single and double-entry visas of up to 180 days, fingerprints are currently waived and fees reduced until 31 December 2026.</li>
<li><strong>24-hour direct transit.</strong> Any nationality can transit through a Chinese airport within 24 hours without a visa, but must stay in the port area.</li>
%s
</ul>
<p class="note">Lists change. %s could be added to a visa-free or transit list; this page is checked against official announcements and was last checked on %s.</p>
</section>""" % (_asean_li_en(c), e(n), e(checked)))
        faqs = [
            ("Can %s use China's 240-hour visa-free transit?" % dem, "No. As of %s, %s is not among the 57 eligible countries." % (checked, n)),
            ("Is there any visa-free way for %s to enter China?" % dem,
             "Only 24-hour direct transit, staying in the airport or port area%s." % (", or an organised ASEAN tour group to Guilin or Xishuangbanna" if c["asean"] else "")),
            ("Where do %s apply for a China visa?" % dem, "At a Chinese embassy or consulate, or a Chinese visa application service center, in the country where you live."),
        ]
        srcs = ["nia_unilateral", "nia_transit", "mfa_mutual", "arrival_card"] + (["asean_xsbn", "nia_regional"] if c["asean"] else [])

    faq_html, faq_ld = faq_block("en", faqs)
    body.append(faq_html)
    body.append(cta("en"))
    body.append('<section class="prose"><h2>Other passports nearby</h2><div class="chips-links">%s<a href="/visa/">All passports</a><a href="/visa/240-hour-transit.html">240-hour transit</a></div></section>'
                % _related(c, D, country_url, e))
    body.append(sources("en", srcs))
    head = '<header class="v-head"><h1>%s</h1><p class="checked">Checked %s against official Chinese sources</p></header>' % (e(title.split("?")[0] + "?"), e(checked))
    return title, desc, head + "\n".join(body), [faq_ld], short


def _asean_li_en(c):
    if not c["asean"]:
        return ""
    return ('<li><strong>ASEAN tour groups.</strong> Groups of two or more from ASEAN countries, organised by a travel agency, can visit '
            'Guilin (via Guilin airport) or Xishuangbanna visa-free for up to 6 days.</li>')


def _asean_note_en(c):
    notes = []
    if c["asean"]:
        notes.append("Travelling in an organised group? ASEAN tour groups can also visit Guilin or Xishuangbanna visa-free for up to 6 days.")
    if c["slug"] in ("vietnam", "kyrgyzstan"):
        notes.append("Going only to Hainan? Since 20 August 2026 %s passports also qualify for Hainan's own 30-day visa-free entry." % c["en"])
    return "".join('<p class="note">%s</p>' % n for n in notes)


def _country_local(lang, c, D, fmt_date, say_cards, faq_block, cta, sources, e):
    assert c["scheme"] == "unilateral", "local country pages are written for the 30-day list only"
    end = fmt_date(end_of(c, D), lang)
    checked = fmt_date(D.CHECKED, lang)
    since = fmt_date(c["since"], lang)
    cards = say_cards(lang, ["tourist", "visafree", "hotel", "return"])
    if lang == "ja":
        title = "日本人は中国ビザ不要？30日以内ならビザ免除（2026年最新）"
        desc = "日本のパスポートは観光・商用・親族訪問・交流・トランジットで中国に30日までビザなし入国できます。数え方、入国審査で見せるもの、期限（%s）まで。%s確認。" % (end, checked)
        short = "日本のパスポート"
        verdict = verdict_html("is-free", "免", "日本国パスポート（一般旅券）", "30日以内の滞在ならビザ不要。",
            "中国のビザ免除政策により、日本の一般旅券で観光、商用、親族・友人訪問、交流訪問、トランジットの目的なら、1回30日まで入国できます（%sから）。現在の期限は%sです。" % (e(since), e(end)),
            [("30日", "1回の入国につき"), (end, "政策の期限"), ("回数制限なし", "入国回数"), ("全開放港", "空路・陸路・海路")], e)
        prose = """<section class="prose">
<h2>30日はこう数える</h2>
<p>入国した日の翌日0時から数えます。3月1日23時に上海に着いたら、3月2日から3月31日までの30日間。その日までに出国します。</p>
<h2>入国審査で準備しておくもの</h2>
<ul>
<li><strong>一般旅券</strong>。滞在期間中ずっと有効であること。緊急旅券などは対象外。航空会社がより厳しく残存期間を確認する場合があるので、事前に確認を。</li>
<li><strong>目的に合った書類</strong>。帰りの航空券やホテルの予約、商用なら招へい状の携帯が推奨されています。</li>
<li><strong>入国カード</strong>。2025年11月からは、着陸前にオンラインで記入できるようになりました。</li>
<li>大使館への事前届け出は不要。開放されている空港・陸路・港ならどこからでも入国できます。</li>
</ul>
<h2>ビザ免除でできないこと</h2>
<ul>
<li><strong>就労・留学・取材</strong>は、事前に該当するビザが必要です。</li>
<li><strong>30日を超える滞在</strong>は、出発前にビザを取るか、正当な理由があれば現地の公安局出入境管理部門で延長を申請します。</li>
<li><strong>何度でも利用可能</strong>。現在、回数や年間の合計日数の制限はありません（目的が合っていること）。</li>
</ul>
<h2>入国審査・ホテルで見せるカード</h2>
<p>大きな空港の審査官は英語が通じますが、地方の窓口やホテルのフロントでは通じないことも。タップで拡大します。</p>
%s
<p>乗り継ぎで中国に立ち寄るだけなら、<a href="/ja/visa/240-hour-transit.html">240時間トランジットビザ免除</a>という別の制度もあります。</p>
</section>""" % cards
        faqs = [("日本人は中国に30日を超えてビザなしで滞在できますか？", "1回の入国では30日までです。いったん出国して再入国することは可能で（現在、回数制限なし）、正当な理由があれば現地で延長申請もできます。長期滞在の予定ならビザを取得してください。"),
                ("日本人のビザ免除はいつまでですか？", "現在の期限は%sです。2023年以降、何度も延長されてきましたが、期限が近づいたら改めて確認してください。" % end),
                ("ビザ免除で中国で働いたり留学したりできますか？", "できません。対象は観光、商用、親族・友人訪問、交流訪問、トランジットです。"),
                ("子どももビザは不要ですか？", "はい。自分のパスポートで渡航する子どもにも同じルールが適用されます。")]
    else:
        title = "한국인 중국 무비자, 30일까지 비자 필요 없음 (2026년 최신)"
        desc = "한국 여권은 관광·비즈니스·친지 방문·교류·경유 목적으로 중국에 30일까지 무비자 입국할 수 있습니다. 날짜 계산법, 입국심사 준비물, 시행 기한(%s)까지. %s 확인." % (end, checked)
        short = "한국 여권"
        verdict = verdict_html("is-free", "免", "대한민국 여권 (일반여권)", "30일 이내 체류는 비자 필요 없음.",
            "중국의 무비자 정책에 따라 한국 일반여권 소지자는 관광, 비즈니스, 친지·친구 방문, 교류 방문, 경유 목적으로 1회 30일까지 입국할 수 있습니다(%s부터). 현재 시행 기한은 %s입니다." % (e(since), e(end)),
            [("30일", "1회 입국당"), (end, "정책 기한"), ("횟수 제한 없음", "입국 횟수"), ("모든 개방 항구", "항공·육로·해로")], e)
        prose = """<section class="prose">
<h2>30일 계산법</h2>
<p>입국한 다음 날 0시부터 셉니다. 3월 1일 밤 11시에 상하이에 도착하면 3월 2일부터 3월 31일까지 30일. 그날까지 출국해야 합니다.</p>
<h2>입국심사 준비물</h2>
<ul>
<li><strong>일반여권</strong>. 체류 기간 내내 유효해야 합니다. 긴급여권 등은 대상이 아닙니다. 항공사가 더 엄격하게 잔여 기간을 확인할 수 있으니 미리 문의하세요.</li>
<li><strong>목적에 맞는 서류</strong>. 귀국 항공권과 호텔 예약, 비즈니스라면 초청장을 지참하도록 권장됩니다.</li>
<li><strong>입국카드</strong>. 2025년 11월부터 착륙 전에 온라인으로 작성할 수 있습니다.</li>
<li>대사관에 미리 신고할 필요는 없고, 개방된 공항·육로·항구 어디로든 입국할 수 있습니다.</li>
</ul>
<h2>무비자로 할 수 없는 것</h2>
<ul>
<li><strong>취업·유학·취재</strong>는 미리 해당 비자를 받아야 합니다.</li>
<li><strong>30일 넘게 머물려면</strong> 출발 전에 비자를 받거나, 정당한 사유가 있으면 현지 공안국 출입국관리 부서에서 연장을 신청합니다.</li>
<li><strong>여러 번 이용 가능</strong>. 현재 횟수나 연간 총 체류일 제한은 없습니다(목적이 맞아야 함).</li>
</ul>
<h2>입국심사·호텔에서 보여줄 카드</h2>
<p>큰 공항 심사관은 영어가 통하지만 지방 창구나 호텔 프런트에서는 안 통할 때도 있어요. 탭하면 크게 보입니다.</p>
%s
<p>경유로 잠깐 들르는 경우라면 <a href="/ko/visa/240-hour-transit.html">240시간 무비자 경유</a>라는 별도 제도도 있습니다.</p>
</section>""" % cards
        faqs = [("한국인은 중국에 30일 넘게 무비자로 있을 수 있나요?", "한 번 입국에 30일까지입니다. 출국 후 재입국은 가능하고(현재 횟수 제한 없음), 정당한 사유가 있으면 현지에서 연장 신청도 할 수 있습니다. 장기 체류 예정이면 비자를 받으세요."),
                ("한국인 중국 무비자는 언제까지인가요?", "현재 기한은 %s입니다. 2024년 시행 이후 여러 차례 연장됐지만, 기한이 가까워지면 다시 확인하세요." % end),
                ("무비자로 중국에서 일하거나 유학할 수 있나요?", "안 됩니다. 관광, 비즈니스, 친지·친구 방문, 교류 방문, 경유만 해당됩니다."),
                ("아이도 비자가 필요 없나요?", "네. 본인 여권으로 여행하는 아이에게도 같은 규칙이 적용됩니다.")]
    faq_html, faq_ld = faq_block(lang, faqs)
    checked_line = {"ja": "%s、中国の公式発表で確認" % checked, "ko": "%s 중국 공식 발표로 확인" % checked}[lang]
    head = '<header class="v-head"><h1>%s</h1><p class="checked">%s</p></header>' % (e(title), e(checked_line))
    body = head + verdict + prose + faq_html + cta(lang) + sources(lang, ["nia_unilateral", "embassy_faq", "arrival_card"])
    return title, desc, body, [faq_ld], short


# =====================================================================================  HUB
HUB_T = {
    "en": dict(
        title="Do I need a visa for China? Check your passport (2026)",
        desc="Check if your passport can enter China visa-free: 50 countries get 30 days, 27 have mutual exemption, 57 can use 240-hour transit. Official lists, checked {d}.",
        h1="Do I need a visa for China?", lede="Pick your passport. The answer comes from China's official lists, checked {d}.",
        label="Your passport", ph="Choose a country…", more="Full rules for this passport →",
        s_uni="30 days visa-free", s_mut="mutual exemption", s_tr="240-hour transit", s_end="30-day list ends",
        ways="Four ways in", ways_body="""<ul>
<li><strong>30-day visa-free list</strong> ({n_uni} countries). China's own, one-sided policy. Tourism, business, family, exchange visits and transit, 30 days per entry. Runs until {end} (Russia until {rus}).</li>
<li><strong>Mutual visa exemption</strong> ({n_mut} countries). Agreements between governments, with no end date. Usually 30 days per stay.</li>
<li><strong>240-hour visa-free transit</strong> ({n_tr} countries). Up to 10 days if you fly on to a third country or region, in {prov} provinces.</li>
<li><strong>Everyone else</strong> needs a visa, apart from 24-hour airside transit and some group-tour schemes.</li>
</ul>""",
        t_uni="30 days visa-free: {n} countries", t_mut="Mutual visa exemption: {n} countries", t_tr="Visa needed, but 240-hour transit works: {n} countries",
        t_visa="Visa required", visa_p="Not listed above? You need a visa. Common passports:",
        th_c="Passport", th_since="Since", th_end="Ends", th_tr="240h transit", th_stay="Stay", yes="Yes", no="No", noend="No end date",
        unclear="Ecuador and Tonga also have mutual agreements, but we could not confirm their current terms for ordinary passports. Ask the Chinese embassy.",
        other="Other visa-free schemes", other_body="""<ul>
<li><strong>Hainan:</strong> 61 nationalities can visit Hainan island only, visa-free for 30 days.</li>
<li><strong>Cruise groups:</strong> foreign tour groups arriving by cruise ship at 13 port cities can stay up to 15 days, as long as they leave on the same ship.</li>
<li><strong>ASEAN tour groups:</strong> up to 6 days in Guilin or Xishuangbanna.</li>
<li><strong>Tour groups from Hong Kong or Macau:</strong> any nationality, up to 144 hours in the Pearl River Delta cities and Shantou.</li>
<li><strong>24-hour transit:</strong> any nationality, staying in the airport or port area.</li>
</ul>""",
        say="Cards for the border", tr_link="240-hour transit, explained →",
        v=dict(uni="No visa needed for up to 30 days.", mut="No visa needed: {stay}.", tr="Visa needed, unless you're in transit (up to 240 hours).", visa="Yes, you need a visa.",
               uni_d="On China's 30-day visa-free list until {end}.", mut_d="Mutual visa exemption agreement, no end date.", tr_d="Not on the 30-day list, but eligible for 240-hour transit to a third country.", visa_d="Not on any visa-free or transit list."),
        faqs=[("Which countries can enter China without a visa in 2026?", "50 countries are on China's 30-day visa-free list, including the UK, Canada, Australia, Japan, South Korea and most of Europe. 27 more have mutual exemption agreements, such as Singapore, Thailand and Malaysia."),
              ("Do Americans need a visa for China?", "Yes, for a normal visit. US passports are not on the 30-day list, but they can use 240-hour visa-free transit when flying on to a third country."),
              ("When does China's visa-free policy end?", "For 48 of the 50 countries, currently on 31 December 2026. Russia's runs to 31 December 2027 and Brunei's has no end date. China has extended the list several times since 2023.")],
    ),
    "ja": dict(
        title="中国ビザは必要？パスポート別チェッカー（2026年最新）",
        desc="あなたのパスポートで中国にビザなしで入国できるか確認。30日ビザ免除50か国、相互免除27か国、240時間トランジット57か国。{d}に公式リストで確認。",
        h1="中国に行くのにビザは必要？", lede="パスポートの国を選ぶだけ。中国の公式リストをもとに、{d}に確認した内容です。",
        label="パスポートの国", ph="国を選択…", more="このパスポートの詳しいルール →",
        s_uni="30日ビザ免除", s_mut="相互ビザ免除", s_tr="240時間トランジット", s_end="30日免除の期限",
        ways="入国の4つのパターン", ways_body="""<ul>
<li><strong>30日ビザ免除</strong>（{n_uni}か国）。中国側の一方的な政策。観光・商用・親族訪問・交流・トランジットで1回30日。期限は{end}（ロシアは{rus}）。</li>
<li><strong>相互ビザ免除協定</strong>（{n_mut}か国）。政府間の協定で期限なし。多くは1回30日。</li>
<li><strong>240時間トランジットビザ免除</strong>（{n_tr}か国）。第三国・地域へ乗り継ぐなら、{prov}の省・市で最大10日。</li>
<li><strong>それ以外</strong>はビザが必要（24時間以内の空港内トランジットや一部の団体旅行を除く）。</li>
</ul>""",
        t_uni="30日ビザ免除：{n}か国", t_mut="相互ビザ免除：{n}か国", t_tr="ビザ必要、ただし240時間トランジット可：{n}か国",
        t_visa="ビザが必要", visa_p="上にない国はビザが必要です。主な国：",
        th_c="パスポート", th_since="開始", th_end="期限", th_tr="240時間", th_stay="滞在", yes="可", no="不可", noend="期限なし",
        unclear="エクアドルとトンガも相互免除協定がありますが、一般旅券の現在の条件を公式に確認できませんでした。中国大使館にお問い合わせください。",
        other="その他のビザ免除制度", other_body="""<ul>
<li><strong>海南島</strong>：61か国の国籍者は、海南島内に限り30日ビザなし。</li>
<li><strong>クルーズ団体</strong>：13の港湾都市にクルーズ船で着く外国人団体は、同じ船で出国するなら最大15日。</li>
<li><strong>ASEAN団体</strong>：桂林または西双版納に最大6日。</li>
<li><strong>香港・マカオ発の団体</strong>：国籍を問わず、珠江デルタの都市と汕頭に最大144時間。</li>
<li><strong>24時間トランジット</strong>：国籍を問わず、空港・港の区域内に限る。</li>
</ul>""",
        say="入国審査で見せるカード", tr_link="240時間トランジットの解説 →",
        v=dict(uni="30日以内ならビザ不要。", mut="ビザ不要：{stay}。", tr="ビザ必要（240時間トランジットなら免除）。", visa="ビザが必要です。",
               uni_d="中国の30日ビザ免除リスト対象（期限{end}）。", mut_d="相互ビザ免除協定（期限なし）。", tr_d="30日免除の対象外。第三国へ乗り継ぐ240時間トランジットは可。", visa_d="ビザ免除・トランジットのどのリストにもありません。"),
        faqs=[("2026年に中国へビザなしで行ける国は？", "30日ビザ免除は日本、韓国、イギリス、カナダ、オーストラリア、欧州の大半など50か国。ほかにシンガポール、タイ、マレーシアなど27か国が相互免除協定の対象です。"),
              ("アメリカ人は中国ビザが必要？", "通常の訪問では必要です。ただし第三国へ乗り継ぐ場合は240時間トランジットビザ免除を使えます。"),
              ("中国のビザ免除はいつまで？", "50か国のうち48か国は現在2026年12月31日まで。ロシアは2027年12月31日まで、ブルネイは期限なし。2023年以降、何度も延長されています。")],
    ),
    "ko": dict(
        title="중국 비자 필요할까? 여권별 무비자 확인 (2026년 최신)",
        desc="내 여권으로 중국 무비자 입국이 되는지 확인하세요. 30일 무비자 50개국, 상호 면제 27개국, 240시간 경유 57개국. {d} 공식 목록으로 확인.",
        h1="중국 가는데 비자 필요할까?", lede="여권 국가만 고르면 됩니다. 중국 공식 목록을 바탕으로 {d}에 확인한 내용입니다.",
        label="여권 국가", ph="국가 선택…", more="이 여권의 자세한 규칙 →",
        s_uni="30일 무비자", s_mut="상호 비자 면제", s_tr="240시간 경유", s_end="30일 무비자 기한",
        ways="입국 방법 4가지", ways_body="""<ul>
<li><strong>30일 무비자</strong>({n_uni}개국). 중국의 일방적 정책. 관광·비즈니스·친지 방문·교류·경유로 1회 30일. 기한은 {end}(러시아는 {rus}).</li>
<li><strong>상호 비자 면제 협정</strong>({n_mut}개국). 정부 간 협정으로 기한 없음. 대부분 1회 30일.</li>
<li><strong>240시간 무비자 경유</strong>({n_tr}개국). 제3국·지역으로 가는 경우 {prov}개 성·시에서 최대 10일.</li>
<li><strong>그 외</strong>는 비자 필요(24시간 이내 공항 내 경유, 일부 단체 관광 제외).</li>
</ul>""",
        t_uni="30일 무비자: {n}개국", t_mut="상호 비자 면제: {n}개국", t_tr="비자 필요, 단 240시간 경유 가능: {n}개국",
        t_visa="비자 필요", visa_p="위에 없는 국가는 비자가 필요합니다. 주요 국가:",
        th_c="여권", th_since="시작", th_end="기한", th_tr="240시간", th_stay="체류", yes="가능", no="불가", noend="기한 없음",
        unclear="에콰도르와 통가도 상호 면제 협정이 있지만, 일반여권의 현재 조건을 공식적으로 확인하지 못했습니다. 중국대사관에 문의하세요.",
        other="그 밖의 무비자 제도", other_body="""<ul>
<li><strong>하이난</strong>: 61개국 국적자는 하이난섬 안에서만 30일 무비자.</li>
<li><strong>크루즈 단체</strong>: 13개 항구 도시에 크루즈로 도착한 외국인 단체는 같은 배로 출국하면 최대 15일.</li>
<li><strong>아세안 단체</strong>: 구이린 또는 시솽반나에 최대 6일.</li>
<li><strong>홍콩·마카오 출발 단체</strong>: 국적 무관, 주강 삼각주 도시와 산터우에 최대 144시간.</li>
<li><strong>24시간 경유</strong>: 국적 무관, 공항·항구 구역 안에서만.</li>
</ul>""",
        say="입국심사에서 보여줄 카드", tr_link="240시간 경유 자세히 →",
        v=dict(uni="30일 이내면 비자 필요 없음.", mut="비자 필요 없음: {stay}.", tr="비자 필요 (240시간 경유는 면제).", visa="비자가 필요합니다.",
               uni_d="중국 30일 무비자 대상 (기한 {end}).", mut_d="상호 비자 면제 협정 (기한 없음).", tr_d="30일 무비자 대상은 아니지만, 제3국으로 가는 240시간 경유는 가능.", visa_d="무비자·경유 목록 어디에도 없습니다."),
        faqs=[("2026년 중국 무비자 입국 가능한 나라는?", "30일 무비자는 한국, 일본, 영국, 캐나다, 호주, 유럽 대부분 등 50개국. 그 밖에 싱가포르, 태국, 말레이시아 등 27개국이 상호 면제 협정 대상입니다."),
              ("미국인은 중국 비자가 필요한가요?", "일반 방문에는 필요합니다. 다만 제3국으로 가는 경우 240시간 무비자 경유를 이용할 수 있습니다."),
              ("중국 무비자는 언제까지인가요?", "50개국 중 48개국은 현재 2026년 12월 31일까지. 러시아는 2027년 12월 31일까지, 브루나이는 기한이 없습니다. 2023년 이후 여러 차례 연장됐습니다.")],
    ),
}


def hub(lang, D, BY, country_url, fmt_date, say_cards, faq_block, cta, sources, e):
    T = HUB_T[lang]
    d = fmt_date(D.CHECKED, lang)
    nm = (lambda c: c["en"]) if lang == "en" else (lambda c: c[lang])
    uni = [c for c in D.COUNTRIES if c["scheme"] == "unilateral"]
    mut = [c for c in D.COUNTRIES if c["scheme"] == "mutual"]
    tr = [c for c in D.COUNTRIES if c["scheme"] == "transit"]
    visa = [c for c in D.COUNTRIES if c["scheme"] == "visa"]
    end, rus = fmt_date(D.UNILATERAL_END, lang), fmt_date(D.RUSSIA_END, lang)
    link = lambda c: '<a href="%s">%s</a>' % (country_url(lang, c["slug"]), e(nm(c)))
    yn = lambda b: '<span class="pill %s">%s</span>' % ("free" if b else "visa", T["yes"] if b else T["no"])

    data = [[c["slug"], nm(c), c["scheme"], STAY[lang].get(c["stay"] or "", ""),
             (T["noend"] if c["end"] == "none" else fmt_date(end_of(c, D), lang)) if c["scheme"] == "unilateral" else "",
             country_url(lang, c["slug"])] for c in sorted_by(D.COUNTRIES, lang)]
    opts = "".join('<option value="%s">%s</option>' % (s, e(n)) for s, n, *_ in data)

    parts = ['<header class="v-head"><h1>%s</h1><p class="lede">%s</p></header>' % (e(T["h1"]), e(T["lede"].format(d=d)))]
    parts.append('<section class="checker"><label for="passport">%s</label><div class="checker-row"><select id="passport"><option value="">%s</option>%s</select></div>'
                 '<div class="checker-out" id="checkerOut" aria-live="polite"></div></section>' % (e(T["label"]), e(T["ph"]), opts))
    parts.append('<section class="verdict" style="border-left-color:var(--ink)"><div class="facts" style="border-top:0;margin-top:0">'
                 '<div class="fact"><b>%d</b><span>%s</span></div><div class="fact"><b>%d</b><span>%s</span></div>'
                 '<div class="fact"><b>%d</b><span>%s</span></div><div class="fact"><b>%s</b><span>%s</span></div></div></section>'
                 % (len(uni), e(T["s_uni"]), len(mut), e(T["s_mut"]), sum(1 for c in D.COUNTRIES if c["transit"]), e(T["s_tr"]), e(end), e(T["s_end"])))

    rows_uni = "".join('<tr><td>%s</td><td class="n">%s</td><td class="n">%s</td><td>%s</td></tr>' % (
        link(c), fmt_date(c["since"], lang) if c["since"] else "—",
        T["noend"] if c["end"] == "none" else fmt_date(end_of(c, D), lang), yn(c["transit"])) for c in sorted_by(uni, lang))
    rows_mut = "".join('<tr><td>%s</td><td>%s</td><td class="n">%s</td></tr>' % (
        link(c), e(STAY[lang][c["stay"]]), fmt_date(c["since"], lang) if c["since"] else "—") for c in sorted_by(mut, lang))
    rows_tr = "".join('<tr><td>%s</td><td>%s</td></tr>' % (link(c), yn(True)) for c in sorted_by(tr, lang))
    visa_chips = "".join(link(c) for c in sorted_by(visa, lang))

    parts.append('<section class="prose"><h2>%s</h2>%s<p><a href="%s">%s</a></p>' % (
        e(T["ways"]), T["ways_body"].format(n_uni=len(uni), n_mut=len(mut), n_tr=sum(1 for c in D.COUNTRIES if c["transit"]),
                                            end=end, rus=rus, prov=D.TRANSIT_PROVINCES),
        {"en": "/visa/240-hour-transit.html", "ja": "/ja/visa/240-hour-transit.html", "ko": "/ko/visa/240-hour-transit.html"}[lang], e(T["tr_link"])))
    parts.append('<h2>%s</h2><div class="ctable-wrap"><table class="ctable"><thead><tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table></div>'
                 % (e(T["t_uni"].format(n=len(uni))), e(T["th_c"]), e(T["th_since"]), e(T["th_end"]), e(T["th_tr"]), rows_uni))
    parts.append('<h2>%s</h2><div class="ctable-wrap"><table class="ctable"><thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table></div><p class="note">%s</p>'
                 % (e(T["t_mut"].format(n=len(mut))), e(T["th_c"]), e(T["th_stay"]), e(T["th_since"]), rows_mut, e(T["unclear"])))
    parts.append('<h2>%s</h2><div class="ctable-wrap"><table class="ctable"><thead><tr><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table></div>'
                 % (e(T["t_tr"].format(n=len(tr))), e(T["th_c"]), e(T["th_tr"]), rows_tr))
    parts.append('<h2>%s</h2><p>%s</p><div class="chips-links">%s</div>' % (e(T["t_visa"]), e(T["visa_p"]), visa_chips))
    parts.append('<h2>%s</h2>%s<h2>%s</h2>%s</section>' % (e(T["other"]), T["other_body"], e(T["say"]), say_cards(lang, ["visafree", "transit", "hotel", "return"])))

    faq_html, faq_ld = faq_block(lang, T["faqs"])
    parts.append(faq_html)
    parts.append(cta(lang))
    parts.append(sources(lang, ["nia_unilateral", "embassy_faq", "mfa_mutual", "nia_mutual", "nia_transit", "nia_regional"]))

    js_strings = {k: T["v"][k] for k in T["v"]}
    js_strings.update(more=T["more"], stamp=STAMP, cls=VCLASS)
    parts.append("""<script>
(function () {
  var DATA = %s, S = %s, sel = document.getElementById("passport"), out = document.getElementById("checkerOut");
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); }
  function show(slug) {
    var r = DATA.filter(function (x) { return x[0] === slug; })[0];
    if (!r) { out.innerHTML = ""; return; }
    var key = {unilateral: "uni", mutual: "mut", transit: "tr", visa: "visa"}[r[2]];
    var ans = S[key].replace("{stay}", r[3]), det = S[key + "_d"].replace("{end}", r[4]);
    out.innerHTML = '<div class="verdict ' + S.cls[r[2]] + '"><span class="verdict-stamp" aria-hidden="true">' + S.stamp[r[2]] + '</span>' +
      '<p class="verdict-kicker">' + esc(r[1]) + '</p><p class="verdict-answer">' + esc(ans) + '</p><p class="verdict-detail">' + esc(det) + '</p>' +
      '<a class="more" href="' + r[5] + '">' + esc(S.more) + '</a></div>';
    try { history.replaceState(null, "", "#" + slug); } catch (e) {}
  }
  sel.addEventListener("change", function () { show(sel.value); });
  var h = location.hash.slice(1);
  if (h && DATA.some(function (x) { return x[0] === h; })) { sel.value = h; show(h); }
})();
</script>""" % (json.dumps(data, ensure_ascii=False), json.dumps(js_strings, ensure_ascii=False)))
    return T["title"], T["desc"].format(d=d), "\n".join(parts), [faq_ld]


# =====================================================================================  TRANSIT
TR_T = {
    "en": dict(
        title="China 240-hour visa-free transit: rules, 57 countries, 24 provinces (2026)",
        desc="How China's 240-hour (10-day) visa-free transit works: the third-country rule, routes that qualify, all 57 eligible passports, ports and permitted provinces. Checked {d}.",
        h1="China's 240-hour visa-free transit, explained",
        lede="Ten days in China without a visa, if you're on your way somewhere else. Here is exactly what counts.",
        rules_h="The rules", rules="""<ol>
<li><strong>Passport:</strong> an ordinary passport from one of the {n} eligible countries, valid for at least 3 more months.</li>
<li><strong>Third country:</strong> you arrive from one country or region and leave to a different one. Round trips (A → China → A) do not qualify.</li>
<li><strong>Onward ticket:</strong> confirmed date and seat, leaving within 240 hours.</li>
<li><strong>Ports:</strong> enter and leave through any of the {ports} designated ports (they do not have to be the same one).</li>
<li><strong>Where you can go:</strong> the permitted areas of {prov} provinces and municipalities. Travel between them is allowed.</li>
<li><strong>The clock</strong> starts at 00:00 on the day after you arrive. Extensions are only possible for illness or force majeure.</li>
<li><strong>Purpose:</strong> tourism, business, visits. Not work, study or journalism.</li>
</ol>""",
        routes_h="Routes that work, and routes that don't", r_th=("Route", "Visa-free?"),
        routes=[("Los Angeles → Shanghai → Tokyo", True, ""), ("Seoul → Beijing → London", True, ""),
                ("Singapore → Chengdu → Sydney", True, "Singapore passports are also visa-free for 30 days anyway"),
                ("New York → Shanghai → New York", False, "same country both ways"),
                ("London → Beijing, stay 11 days → Seoul", False, "over 240 hours")],
        yes="Yes", no="No",
        hk="Many travellers use a flight to Hong Kong or Macau as the onward leg. The official rule says \"third country or region\"; confirm with your airline before you book, since it checks eligibility at check-in.",
        who_h="Eligible passports ({n})", who_p="Passports marked with a 30-day badge do not need transit at all for trips up to 30 days.",
        ports_h="Every port you can use ({ports})", ports_p="Enter at one, leave from another: they do not have to match. Five ports on the Guangdong side opened on 5 November 2025 and are marked new.", ports_new="new", badge="30 days", areas_h="Where you can go ({prov} provinces)", areas_p="Some provinces are open only in listed cities.",
        say="Show this at the border",
        faqs=[("Is 240-hour transit the same as visa-free entry?", "No. Transit needs an onward ticket to a third country or region and limits you to certain provinces. The 30-day visa-free policy has neither condition, but covers fewer passports."),
              ("Do Americans qualify for 240-hour transit?", "Yes. US passports are on the list of 57 countries. Americans are not on the 30-day visa-free list, so transit is their main visa-free option."),
              ("Can I enter in Beijing and leave from Shanghai?", "Yes. You can enter and leave through different designated ports, and travel between permitted provinces."),
              ("When does the 240 hours start?", "At 00:00 on the day after you arrive.")],
    ),
    "ja": dict(
        title="中国240時間トランジットビザ免除：ルール・対象57か国・24省（2026年）",
        desc="中国の240時間（10日間）トランジットビザ免除の仕組み。第三国ルール、使えるルート・使えないルート、対象57か国、入国できる港と滞在できる省。{d}確認。",
        h1="中国の240時間トランジットビザ免除",
        lede="第三国へ向かう途中なら、ビザなしで中国に最大10日。どこまでがOKか、正確にまとめました。",
        rules_h="ルール", rules="""<ol>
<li><strong>パスポート：</strong>対象{n}か国の一般旅券。残存期間3か月以上。</li>
<li><strong>第三国：</strong>来た国・地域と、次に向かう国・地域が異なること。往復（A→中国→A）は対象外。</li>
<li><strong>次の航空券：</strong>日付と座席が確定し、240時間以内に出国するもの。</li>
<li><strong>港：</strong>指定された{ports}の港から出入国（同じ港でなくてもよい）。</li>
<li><strong>行ける範囲：</strong>{prov}の省・直轄市などの指定区域。区域間の移動も可。</li>
<li><strong>時間</strong>は入国翌日の0時から。延長は病気や不可抗力の場合のみ。</li>
<li><strong>目的：</strong>観光、商用、訪問。就労・留学・取材は不可。</li>
</ol>""",
        routes_h="使えるルート・使えないルート", r_th=("ルート", "ビザ免除？"),
        routes=[("ロサンゼルス → 上海 → 東京", True, ""), ("ソウル → 北京 → ロンドン", True, ""),
                ("東京 → 上海 → 東京", False, "往復は対象外（日本のパスポートなら30日ビザ免除で入国可）"),
                ("ロンドン → 北京に11日滞在 → ソウル", False, "240時間超過")],
        yes="可", no="不可",
        hk="次の行き先として香港・マカオ行きの便を使う旅行者も多くいます。公式の表現は「第三国または地域」なので、予約前に航空会社に確認してください（搭乗手続きで資格を確認されます）。",
        who_h="対象パスポート（{n}か国）", who_p="「30日」の印がある国は、30日以内の旅行ならトランジット制度を使う必要がありません。",
        ports_h="使える港・空港の全リスト（{ports}）", ports_p="入国と出国で別の港でも構いません。広東省側の5か所は2025年11月5日に追加されたもので、newと表示しています。", ports_new="new", badge="30日", areas_h="行ける範囲（{prov}省・市）", areas_p="一部の省は記載の都市のみ。",
        say="入国審査で見せるカード",
        faqs=[("日本人は240時間トランジットを使う必要がありますか？", "30日以内の旅行なら不要です。日本のパスポートは30日ビザ免除の対象なので、往復航空券でも入国できます。"),
              ("北京で入国して上海から出国できますか？", "できます。指定された港であれば出入国の港が違っても構いません。"),
              ("240時間はいつから数えますか？", "入国した日の翌日0時からです。")],
    ),
    "ko": dict(
        title="중국 240시간 무비자 경유: 규칙, 대상 57개국, 24개 성 (2026년)",
        desc="중국 240시간(10일) 무비자 경유 제도 정리. 제3국 규칙, 되는 경로와 안 되는 경로, 대상 57개국, 입국 항구와 체류 가능 지역. {d} 확인.",
        h1="중국 240시간 무비자 경유 제도",
        lede="다른 나라로 가는 길이라면 비자 없이 중국에서 최대 10일. 어디까지 되는지 정확하게 정리했습니다.",
        rules_h="규칙", rules="""<ol>
<li><strong>여권:</strong> 대상 {n}개국 일반여권, 잔여 유효기간 3개월 이상.</li>
<li><strong>제3국:</strong> 출발한 국가·지역과 다음 목적지 국가·지역이 달라야 합니다. 왕복(A→중국→A)은 불가.</li>
<li><strong>다음 항공권:</strong> 날짜와 좌석이 확정되고 240시간 이내 출국.</li>
<li><strong>항구:</strong> 지정된 {ports}개 항구로 출입국(같은 항구가 아니어도 됨).</li>
<li><strong>이동 범위:</strong> {prov}개 성·직할시 등의 지정 지역. 지역 간 이동 가능.</li>
<li><strong>시간</strong>은 입국 다음 날 0시부터. 연장은 질병·불가항력일 때만.</li>
<li><strong>목적:</strong> 관광, 비즈니스, 방문. 취업·유학·취재는 불가.</li>
</ol>""",
        routes_h="되는 경로, 안 되는 경로", r_th=("경로", "무비자?"),
        routes=[("로스앤젤레스 → 상하이 → 도쿄", True, ""), ("서울 → 베이징 → 런던", True, ""),
                ("서울 → 상하이 → 서울", False, "왕복은 불가 (한국 여권은 30일 무비자로 입국 가능)"),
                ("런던 → 베이징 11일 체류 → 서울", False, "240시간 초과")],
        yes="가능", no="불가",
        hk="다음 목적지로 홍콩·마카오행 항공편을 이용하는 여행자도 많습니다. 공식 표현은 \"제3국 또는 지역\"이므로 예약 전에 항공사에 확인하세요(체크인 때 자격을 확인합니다).",
        who_h="대상 여권 ({n}개국)", who_p="\"30일\" 표시가 있는 국가는 30일 이내 여행이면 경유 제도를 쓸 필요가 없습니다.",
        ports_h="이용 가능한 전체 항구·공항 ({ports})", ports_p="입국과 출국 항구가 달라도 됩니다. 광둥성 쪽 5곳은 2025년 11월 5일에 추가되었으며 new로 표시했습니다.", ports_new="new", badge="30일", areas_h="이동 가능 지역 ({prov}개 성·시)", areas_p="일부 성은 표시된 도시만 해당.",
        say="입국심사에서 보여줄 카드",
        faqs=[("한국인도 240시간 경유를 써야 하나요?", "30일 이내 여행이면 필요 없습니다. 한국 여권은 30일 무비자 대상이라 왕복 항공권으로도 입국할 수 있습니다."),
              ("베이징으로 입국해서 상하이로 출국할 수 있나요?", "네. 지정된 항구라면 입국과 출국 항구가 달라도 됩니다."),
              ("240시간은 언제부터 계산하나요?", "입국한 다음 날 0시부터입니다.")],
    ),
}


def transit(lang, D, BY, country_url, fmt_date, say_cards, faq_block, cta, sources, e):
    T = TR_T[lang]
    d = fmt_date(D.CHECKED, lang)
    elig = sorted_by([c for c in D.COUNTRIES if c["transit"]], lang)
    nm = (lambda c: c["en"]) if lang == "en" else (lambda c: c[lang])
    fmtv = dict(n=len(elig), ports=D.TRANSIT_PORTS, prov=D.TRANSIT_PROVINCES)
    parts = ['<header class="v-head"><h1>%s</h1><p class="lede">%s</p><p class="checked">%s</p></header>' % (
        e(T["h1"]), e(T["lede"]), e({"en": "Checked %s", "ja": "%s 確認", "ko": "%s 확인"}[lang] % d))]
    parts.append(verdict_html("is-transit", "过", "240h", {"en": "Up to 10 days, no visa, on your way elsewhere.", "ja": "乗り継ぎなら、ビザなしで最大10日。", "ko": "경유라면 비자 없이 최대 10일."}[lang], "",
                              [("240 h", {"en": "max stay", "ja": "最長滞在", "ko": "최대 체류"}[lang]),
                               (str(len(elig)), {"en": "countries", "ja": "対象国", "ko": "대상국"}[lang]),
                               (str(D.TRANSIT_PORTS), {"en": "ports", "ja": "港", "ko": "항구"}[lang]),
                               (str(D.TRANSIT_PROVINCES), {"en": "provinces", "ja": "省・市", "ko": "성·시"}[lang])], e))
    rows = "".join('<tr><td>%s</td><td><span class="pill %s">%s</span>%s</td></tr>' % (
        e(r), "free" if ok else "visa", e(T["yes"] if ok else T["no"]), (" " + e(note)) if note else "") for r, ok, note in T["routes"])
    chips = "".join('<a href="%s">%s%s</a>' % (country_url(lang, c["slug"]), e(nm(c)),
                    ' · <span class="pill free">%s</span>' % e(T["badge"]) if c["scheme"] in ("unilateral", "mutual") else "") for c in elig)
    areas = "".join('<li>%s</li>' % e(zh if lang == "ja" else en) for en, zh in D.TRANSIT_AREAS)
    port_rows = "".join(
        '<tr><td>%s</td><td>%s</td></tr>' % (e(area), "".join(
            '<span class="port%s">%s%s</span>' % (
                " is-new" if pt in D.NEW_PORTS else "", e(pt),
                ' <em>%s</em>' % e(T["ports_new"]) if pt in D.NEW_PORTS else "") for pt in pts))
        for area, pts in D.TRANSIT_PORTS_BY_AREA)
    parts.append('<section class="prose"><h2>%s</h2>%s<h2>%s</h2><div class="ctable-wrap"><table class="ctable"><thead><tr><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table></div>'
                 '<p class="note">%s</p><h2>%s</h2><p>%s</p><div class="chips-links">%s</div><h2>%s</h2><p>%s</p><ul style="columns:2">%s</ul><h2>%s</h2>%s</section>' % (
        e(T["rules_h"]), T["rules"].format(**fmtv), e(T["routes_h"]), e(T["r_th"][0]), e(T["r_th"][1]), rows, e(T["hk"]),
        e(T["who_h"].format(**fmtv)), e(T["who_p"]), chips, e(T["areas_h"].format(**fmtv)), e(T["areas_p"]), areas,
        e(T["say"]), say_cards(lang, ["transit", "hotel"])))
    parts.append('<section class="prose"><h2 id="ports">%s</h2><p>%s</p>'
                 '<div class="ctable-wrap"><table class="ctable ports"><tbody>%s</tbody></table></div></section>' % (
                     e(T["ports_h"].format(**fmtv)), e(T["ports_p"]), port_rows))
    faq_html, faq_ld = faq_block(lang, T["faqs"])
    parts.append(faq_html)
    parts.append(cta(lang))
    parts.append(sources(lang, ["nia_transit", "transit_faq", "transit_areas", "transit_ports_2025"]))
    return T["title"], T["desc"].format(d=d), "\n".join(parts), [faq_ld]
