# Policy facts for the visa pages. Every rule here traces to a source in SOURCES.
# Checked against official pages on CHECKED. Things we could not verify officially are left out on purpose
# (Ecuador's and Tonga's mutual-exemption terms; an official example of HK/Macau as the transit "third region").

CHECKED = "2026-09-17"
UNILATERAL_END = "2026-12-31"      # 48 of the 50 countries
RUSSIA_END = "2027-12-31"
TRANSIT_PORTS = 65
TRANSIT_PROVINCES = 24

# scheme: "unilateral" (30 days, has an end date) | "mutual" (agreement, no end date) | "transit" (240h only) | "visa"
# stay (mutual only): "30" | "30_90in180" | "90in180" | "30_90peryear" | "60" | "3m"
# t: eligible for 240-hour transit.  asean: ASEAN tour-group schemes apply.
# region: eu | am | oc | as | me | af
C = lambda slug, en, dem, ja, ko, scheme, region, t=False, since=None, stay=None, end=None, asean=False: dict(
    slug=slug, en=en, dem=dem, ja=ja, ko=ko, scheme=scheme, region=region, transit=t, since=since, stay=stay, end=end, asean=asean)

COUNTRIES = [
    # ---- 30-day unilateral visa-free (NIA list of 17 Feb 2026; end dates per embassy FAQ of 25 May 2026)
    C("france", "France", "French citizens", "フランス", "프랑스", "unilateral", "eu", True, "2023-12-01"),
    C("germany", "Germany", "German citizens", "ドイツ", "독일", "unilateral", "eu", True, "2023-12-01"),
    C("italy", "Italy", "Italian citizens", "イタリア", "이탈리아", "unilateral", "eu", True, "2023-12-01"),
    C("netherlands", "Netherlands", "Dutch citizens", "オランダ", "네덜란드", "unilateral", "eu", True, "2023-12-01"),
    C("spain", "Spain", "Spanish citizens", "スペイン", "스페인", "unilateral", "eu", True, "2023-12-01"),
    C("switzerland", "Switzerland", "Swiss citizens", "スイス", "스위스", "unilateral", "eu", True, "2024-03-14"),
    C("ireland", "Ireland", "Irish citizens", "アイルランド", "아일랜드", "unilateral", "eu", True, "2024-03-14"),
    C("hungary", "Hungary", "Hungarian citizens", "ハンガリー", "헝가리", "unilateral", "eu", True, "2024-03-14"),
    C("austria", "Austria", "Austrian citizens", "オーストリア", "오스트리아", "unilateral", "eu", True, "2024-03-14"),
    C("belgium", "Belgium", "Belgian citizens", "ベルギー", "벨기에", "unilateral", "eu", True, "2024-03-14"),
    C("luxembourg", "Luxembourg", "Luxembourg citizens", "ルクセンブルク", "룩셈부르크", "unilateral", "eu", True, "2024-03-14"),
    C("new-zealand", "New Zealand", "New Zealanders", "ニュージーランド", "뉴질랜드", "unilateral", "oc", True, "2024-07-01"),
    C("australia", "Australia", "Australians", "オーストラリア", "호주", "unilateral", "oc", True, "2024-07-01"),
    C("poland", "Poland", "Polish citizens", "ポーランド", "폴란드", "unilateral", "eu", True, "2024-07-01"),
    C("portugal", "Portugal", "Portuguese citizens", "ポルトガル", "포르투갈", "unilateral", "eu", True, "2024-10-15"),
    C("greece", "Greece", "Greek citizens", "ギリシャ", "그리스", "unilateral", "eu", True, "2024-10-15"),
    C("cyprus", "Cyprus", "Cypriot citizens", "キプロス", "키프로스", "unilateral", "eu", True, "2024-10-15"),
    C("slovenia", "Slovenia", "Slovenian citizens", "スロベニア", "슬로베니아", "unilateral", "eu", True, "2024-10-15"),
    C("slovakia", "Slovakia", "Slovak citizens", "スロバキア", "슬로바키아", "unilateral", "eu", True, "2024-11-08"),
    C("norway", "Norway", "Norwegian citizens", "ノルウェー", "노르웨이", "unilateral", "eu", True, "2024-11-08"),
    C("finland", "Finland", "Finnish citizens", "フィンランド", "핀란드", "unilateral", "eu", True, "2024-11-08"),
    C("denmark", "Denmark", "Danish citizens", "デンマーク", "덴마크", "unilateral", "eu", True, "2024-11-08"),
    C("iceland", "Iceland", "Icelandic citizens", "アイスランド", "아이슬란드", "unilateral", "eu", True, "2024-11-08"),
    C("andorra", "Andorra", "Andorran citizens", "アンドラ", "안도라", "unilateral", "eu", False, "2024-11-08"),
    C("monaco", "Monaco", "Monaco citizens", "モナコ", "모나코", "unilateral", "eu", True, "2024-11-08"),
    C("liechtenstein", "Liechtenstein", "Liechtenstein citizens", "リヒテンシュタイン", "리히텐슈타인", "unilateral", "eu", False, "2024-11-08"),
    C("south-korea", "South Korea", "South Koreans", "韓国", "한국", "unilateral", "as", True, "2024-11-08"),
    C("bulgaria", "Bulgaria", "Bulgarian citizens", "ブルガリア", "불가리아", "unilateral", "eu", True, "2024-11-30"),
    C("romania", "Romania", "Romanian citizens", "ルーマニア", "루마니아", "unilateral", "eu", True, "2024-11-30"),
    C("croatia", "Croatia", "Croatian citizens", "クロアチア", "크로아티아", "unilateral", "eu", True, "2024-11-30"),
    C("montenegro", "Montenegro", "Montenegrin citizens", "モンテネグロ", "몬테네그로", "unilateral", "eu", True, "2024-11-30"),
    C("north-macedonia", "North Macedonia", "North Macedonian citizens", "北マケドニア", "북마케도니아", "unilateral", "eu", True, "2024-11-30"),
    C("malta", "Malta", "Maltese citizens", "マルタ", "몰타", "unilateral", "eu", True, "2024-11-30"),
    C("estonia", "Estonia", "Estonian citizens", "エストニア", "에스토니아", "unilateral", "eu", True, "2024-11-30"),
    C("latvia", "Latvia", "Latvian citizens", "ラトビア", "라트비아", "unilateral", "eu", True, "2024-11-30"),
    C("japan", "Japan", "Japanese citizens", "日本", "일본", "unilateral", "as", True, "2024-11-30"),
    C("brazil", "Brazil", "Brazilians", "ブラジル", "브라질", "unilateral", "am", True, "2025-06-01"),
    C("argentina", "Argentina", "Argentinians", "アルゼンチン", "아르헨티나", "unilateral", "am", True, "2025-06-01"),
    C("chile", "Chile", "Chileans", "チリ", "칠레", "unilateral", "am", True, "2025-06-01"),
    C("peru", "Peru", "Peruvians", "ペルー", "페루", "unilateral", "am", False, "2025-06-01"),
    C("uruguay", "Uruguay", "Uruguayans", "ウルグアイ", "우루과이", "unilateral", "am", False, "2025-06-01"),
    C("saudi-arabia", "Saudi Arabia", "Saudi citizens", "サウジアラビア", "사우디아라비아", "unilateral", "me", False, "2025-06-09"),
    C("oman", "Oman", "Omani citizens", "オマーン", "오만", "unilateral", "me", False, "2025-06-09"),
    C("kuwait", "Kuwait", "Kuwaiti citizens", "クウェート", "쿠웨이트", "unilateral", "me", False, "2025-06-09"),
    C("bahrain", "Bahrain", "Bahraini citizens", "バーレーン", "바레인", "unilateral", "me", False, "2025-06-09"),
    C("russia", "Russia", "Russian citizens", "ロシア", "러시아", "unilateral", "eu", True, "2025-09-15", end="2027-12-31"),
    C("sweden", "Sweden", "Swedish citizens", "スウェーデン", "스웨덴", "unilateral", "eu", True, "2025-11-10"),
    C("united-kingdom", "United Kingdom", "British citizens", "イギリス", "영국", "unilateral", "eu", True, "2026-02-17"),
    C("canada", "Canada", "Canadians", "カナダ", "캐나다", "unilateral", "am", True, "2026-02-17"),
    C("brunei", "Brunei", "Bruneians", "ブルネイ", "브루나이", "unilateral", "as", True, None, end="none", asean=True),

    # ---- mutual visa exemption, ordinary passports (MFA table updated 29 May 2026; stay limits per NIA table 14 Apr 2025)
    C("san-marino", "San Marino", "San Marino citizens", "サンマリノ", "산마리노", "mutual", "eu", False, "1985-07-22", "3m"),
    C("seychelles", "Seychelles", "Seychellois citizens", "セーシェル", "세이셸", "mutual", "af", False, "2013-06-26", "30"),
    C("mauritius", "Mauritius", "Mauritian citizens", "モーリシャス", "모리셔스", "mutual", "af", False, "2013-10-31", "60"),
    C("bahamas", "Bahamas", "Bahamians", "バハマ", "바하마", "mutual", "am", False, "2014-02-12", "30"),
    C("fiji", "Fiji", "Fijians", "フィジー", "피지", "mutual", "oc", False, "2015-03-14", "30"),
    C("grenada", "Grenada", "Grenadians", "グレナダ", "그레나다", "mutual", "am", False, "2015-06-10", "30"),
    C("serbia", "Serbia", "Serbian citizens", "セルビア", "세르비아", "mutual", "eu", True, "2017-01-15", "30"),
    C("barbados", "Barbados", "Barbadians", "バルバドス", "바베이도스", "mutual", "am", False, "2017-06-01", "30"),
    C("united-arab-emirates", "United Arab Emirates", "UAE citizens", "アラブ首長国連邦", "아랍에미리트", "mutual", "me", True, "2018-01-16", "30"),
    C("bosnia-and-herzegovina", "Bosnia and Herzegovina", "Bosnian citizens", "ボスニア・ヘルツェゴビナ", "보스니아 헤르체고비나", "mutual", "eu", True, "2018-05-29", "90in180"),
    C("belarus", "Belarus", "Belarusian citizens", "ベラルーシ", "벨라루스", "mutual", "eu", True, "2018-08-10", "30_90peryear"),
    C("qatar", "Qatar", "Qatari citizens", "カタール", "카타르", "mutual", "me", True, "2018-12-21", "30"),
    C("armenia", "Armenia", "Armenian citizens", "アルメニア", "아르메니아", "mutual", "as", False, "2020-01-19", "90in180"),
    C("suriname", "Suriname", "Surinamese citizens", "スリナム", "수리남", "mutual", "am", False, None, "30"),
    C("maldives", "Maldives", "Maldivians", "モルディブ", "몰디브", "mutual", "as", False, "2022-05-20", "30"),
    C("dominica", "Dominica", "Dominica citizens", "ドミニカ国", "도미니카 연방", "mutual", "am", False, "2022-09-19", "30"),
    C("albania", "Albania", "Albanian citizens", "アルバニア", "알바니아", "mutual", "eu", True, "2023-03-18", "90in180"),
    C("kazakhstan", "Kazakhstan", "Kazakh citizens", "カザフスタン", "카자흐스탄", "mutual", "as", False, "2023-11-10", "30_90in180"),
    C("singapore", "Singapore", "Singaporeans", "シンガポール", "싱가포르", "mutual", "as", True, "2024-02-09", "30", asean=True),
    C("thailand", "Thailand", "Thai citizens", "タイ", "태국", "mutual", "as", False, "2024-03-01", "30_90in180", asean=True),
    C("antigua-and-barbuda", "Antigua and Barbuda", "Antigua and Barbuda citizens", "アンティグア・バーブーダ", "앤티가 바부다", "mutual", "am", False, "2024-05-11", "30_90in180"),
    C("georgia", "Georgia", "Georgian citizens", "ジョージア", "조지아", "mutual", "as", False, "2024-05-28", "30_90in180"),
    C("solomon-islands", "Solomon Islands", "Solomon Islanders", "ソロモン諸島", "솔로몬 제도", "mutual", "oc", False, "2024-12-28", "30_90in180"),
    C("samoa", "Samoa", "Samoans", "サモア", "사모아", "mutual", "oc", False, "2025-04-02", "30_90in180"),
    C("uzbekistan", "Uzbekistan", "Uzbek citizens", "ウズベキスタン", "우즈베키스탄", "mutual", "as", False, "2025-06-01", "30_90in180"),
    C("azerbaijan", "Azerbaijan", "Azerbaijani citizens", "アゼルバイジャン", "아제르바이잔", "mutual", "as", False, "2025-07-16", "30_90in180"),
    C("malaysia", "Malaysia", "Malaysians", "マレーシア", "말레이시아", "mutual", "as", False, "2025-07-17", "30_90in180", asean=True),

    # ---- 240-hour transit only (NIA list of 20 Aug 2026)
    C("united-states", "United States", "Americans", "アメリカ", "미국", "transit", "am", True),
    C("mexico", "Mexico", "Mexicans", "メキシコ", "멕시코", "transit", "am", True),
    C("czech-republic", "Czech Republic", "Czech citizens", "チェコ", "체코", "transit", "eu", True),
    C("lithuania", "Lithuania", "Lithuanian citizens", "リトアニア", "리투아니아", "transit", "eu", True),
    C("ukraine", "Ukraine", "Ukrainian citizens", "ウクライナ", "우크라이나", "transit", "eu", True),
    C("indonesia", "Indonesia", "Indonesians", "インドネシア", "인도네시아", "transit", "as", True, "2025-06-12", asean=True),
    C("vietnam", "Vietnam", "Vietnamese citizens", "ベトナム", "베트남", "transit", "as", True, "2026-08-20", asean=True),
    C("kyrgyzstan", "Kyrgyzstan", "Kyrgyz citizens", "キルギス", "키르기스스탄", "transit", "as", True, "2026-08-20"),

    # ---- visa required (not on any list above); large travel markets only
    C("india", "India", "Indians", "インド", "인도", "visa", "as"),
    C("philippines", "Philippines", "Filipinos", "フィリピン", "필리핀", "visa", "as", asean=True),
    C("cambodia", "Cambodia", "Cambodians", "カンボジア", "캄보디아", "visa", "as", asean=True),
    C("myanmar", "Myanmar", "Myanmar citizens", "ミャンマー", "미얀마", "visa", "as", asean=True),
    C("laos", "Laos", "Lao citizens", "ラオス", "라오스", "visa", "as", asean=True),
    C("pakistan", "Pakistan", "Pakistanis", "パキスタン", "파키스탄", "visa", "as"),
    C("bangladesh", "Bangladesh", "Bangladeshis", "バングラデシュ", "방글라데시", "visa", "as"),
    C("nepal", "Nepal", "Nepalis", "ネパール", "네팔", "visa", "as"),
    C("sri-lanka", "Sri Lanka", "Sri Lankans", "スリランカ", "스리랑카", "visa", "as"),
    C("mongolia", "Mongolia", "Mongolians", "モンゴル", "몽골", "visa", "as"),
    C("turkey", "Turkey", "Turkish citizens", "トルコ", "튀르키예", "visa", "me"),
    C("israel", "Israel", "Israelis", "イスラエル", "이스라엘", "visa", "me"),
    C("egypt", "Egypt", "Egyptians", "エジプト", "이집트", "visa", "af"),
    C("nigeria", "Nigeria", "Nigerians", "ナイジェリア", "나이지리아", "visa", "af"),
    C("south-africa", "South Africa", "South Africans", "南アフリカ", "남아프리카공화국", "visa", "af"),
    C("kenya", "Kenya", "Kenyans", "ケニア", "케냐", "visa", "af"),
    C("colombia", "Colombia", "Colombians", "コロンビア", "콜롬비아", "visa", "am"),
]

PHRASES = {
    "tourist": {"zh": "我来旅游，待十天。", "py": "wǒ lái lǚyóu, dāi shí tiān.",
                "en": "I'm here as a tourist, for ten days.", "ja": "観光で来ました。10日間滞在します。", "ko": "관광하러 왔어요. 열흘 있을 거예요."},
    "visafree": {"zh": "我是免签入境。", "py": "wǒ shì miǎnqiān rùjìng.",
                 "en": "I'm entering visa-free.", "ja": "ビザ免除で入国します。", "ko": "무비자로 입국합니다."},
    "transit": {"zh": "我是240小时过境免签。这是我去第三国的机票。", "py": "wǒ shì èr-bǎi sì-shí xiǎoshí guòjìng miǎnqiān. zhè shì wǒ qù dì-sān guó de jīpiào.",
                "en": "I'm on 240-hour visa-free transit. This is my ticket to a third country.", "ja": "240時間トランジットビザ免除です。これは第三国行きの航空券です。", "ko": "240시간 무비자 경유입니다. 제3국으로 가는 항공권이에요."},
    "hotel": {"zh": "这是我的酒店预订。", "py": "zhè shì wǒ de jiǔdiàn yùdìng.",
              "en": "This is my hotel booking.", "ja": "これはホテルの予約です。", "ko": "제 호텔 예약이에요."},
    "return": {"zh": "这是我的回程机票。", "py": "zhè shì wǒ de huíchéng jīpiào.",
               "en": "This is my return ticket.", "ja": "これは帰りの航空券です。", "ko": "제 귀국 항공권이에요."},
}

SOURCES = {
    "nia_unilateral": {"title": "National Immigration Administration: visa-free policy for 50 countries (17 Feb 2026)",
                       "url": "https://en.nia.gov.cn/n147418/n147463/c183390/content.html"},
    "embassy_faq": {"title": "Chinese Embassy in Sweden: visa-free FAQ, end dates (updated 25 May 2026)",
                    "url": "https://se.china-embassy.gov.cn/lstz/202511/t20251110_11750027.htm"},
    "mfa_uk_ca": {"title": "Ministry of Foreign Affairs: UK and Canada added (15 Feb 2026)",
                  "url": "https://cs.mfa.gov.cn/gyls/lsgz/fwxx/202602/t20260215_11860470.shtml"},
    "mfa_russia": {"title": "Ministry of Foreign Affairs: Russia trial extended to 31 Dec 2027 (20 May 2026)",
                   "url": "https://www.mfa.gov.cn/wjbzwfwpt/kzx/tzgg/202605/t20260520_11914502.html"},
    "mfa_mutual": {"title": "Ministry of Foreign Affairs: mutual visa exemption agreements",
                   "url": "https://cs.mfa.gov.cn/wgrlh/lhqz/lhqzjjs/202510/t20251023_11739051.shtml"},
    "nia_mutual": {"title": "National Immigration Administration: mutual exemption stay limits (14 Apr 2025)",
                   "url": "https://en.nia.gov.cn/n147418/n147463/c181470/content.html"},
    "nia_transit": {"title": "National Immigration Administration: 240-hour visa-free transit, 57 countries (20 Aug 2026)",
                    "url": "https://en.nia.gov.cn/n147418/n147463/c183412/content.html"},
    "transit_faq": {"title": "Chinese Consulate in Montreal: transit FAQ, passport validity and time count (30 May 2025)",
                    "url": "https://montreal.china-consulate.gov.cn/zjfw/lszj/fhqz/cjwd2/202505/t20250530_11637915.htm"},
    "transit_areas": {"title": "Chinese Embassy in Canada: 240-hour transit ports and permitted areas",
                      "url": "https://ca.china-embassy.gov.cn/lsyw/lszj/mqzc00/gjmq00/202501/t20250110_11530399.htm"},
    "nia_regional": {"title": "National Immigration Administration: regional visa-free schemes (20 Aug 2026)",
                     "url": "https://www.nia.gov.cn/n741440/n741577/c1699641/content.html"},
    "asean_xsbn": {"title": "State Council: ASEAN tour groups visa-free in Xishuangbanna (Feb 2025)",
                   "url": "https://www.gov.cn/zhengce/zhengceku/202502/content_7003054.htm"},
    "arrival_card": {"title": "Chinese Consulate in Barcelona: online arrival card and 2026 measures",
                     "url": "https://barcelona.china-consulate.gov.cn/gdxw/202603/t20260330_11883678.htm"},
}

# Permitted areas for 240-hour transit (Chinese Embassy in Canada; ports rose from 60 to 65 on 5 Nov 2025, provinces unchanged).
TRANSIT_AREAS = [
    ("Beijing", "北京"), ("Tianjin", "天津"), ("Hebei", "河北"), ("Shanxi (Taiyuan, Datong)", "山西（太原、大同）"),
    ("Liaoning", "辽宁"), ("Heilongjiang (Harbin)", "黑龙江（哈尔滨）"), ("Shanghai", "上海"), ("Jiangsu", "江苏"),
    ("Zhejiang", "浙江"), ("Anhui", "安徽"), ("Fujian", "福建"), ("Jiangxi (Nanchang, Jingdezhen)", "江西（南昌、景德镇）"),
    ("Shandong", "山东"), ("Henan", "河南"), ("Hubei", "湖北"), ("Hunan", "湖南"), ("Guangdong", "广东"),
    ("Guangxi (12 cities)", "广西（12个城市）"), ("Hainan", "海南"), ("Chongqing", "重庆"),
    ("Sichuan (Chengdu, Leshan and 9 more cities)", "四川（成都、乐山等11市）"), ("Guizhou", "贵州"),
    ("Yunnan (Kunming, Dali, Lijiang, Xishuangbanna and 5 more)", "云南（昆明、大理、丽江、西双版纳等9地）"), ("Shaanxi", "陕西"),
]
