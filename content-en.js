window.CONTENT = window.CONTENT || {};
window.CONTENT.en = {
  cityNames: { beijing: "Beijing", shanghai: "Shanghai", xian: "Xi'an", chengdu: "Chengdu", suzhou: "Suzhou", everywhere: "Everywhere" },
  cards: [
    {
      id: "douzhi", city: "beijing", zh: "豆汁", title: "How to drink douzhi", price: "3–5 RMB a bowl",
      hook: "Fermented mung-bean water. Smells like a sour sock, tastes like Beijing. Locals drink it at 6:30 a.m. and watch your face.",
      steps: [
        "Order a small bowl (小碗), one jiaoquan (焦圈, a crisp fried ring) and a plate of pickled shreds. They come as a set.",
        "Do not smell it first. Take a small sip while it is hot. Hot douzhi is far milder than warm douzhi.",
        "Bite jiaoquan, sip douzhi, eat a pinch of pickles. Repeat. The three balance each other.",
        "Sip #1 is a shock, sip #3 is fine, bowl #2 is when you start to like it. Most people stop at #1."
      ],
      where: "Old Ciqikou Douzhi (老磁器口豆汁店), north gate of the Temple of Heaven. Huguosi Snacks (护国寺小吃) for a gentler version.",
      mistake: "Ordering a big bowl on your first try, or drinking it cold.",
      say: { zh: "一碗豆汁，一个焦圈，谢谢。", py: "yì wǎn dòu zhī, yí ge jiāo quān, xiè xie", en: "One bowl of douzhi, one jiaoquan, thanks." }
    },
    {
      id: "xlb", city: "shanghai", zh: "小笼包", title: "How to eat a soup dumpling", price: "20–35 RMB / 12 pcs",
      hook: "There is hot soup inside. The shop will not warn you. The rhyme locals learn as kids: lift lightly, move slowly, open a window, drink the soup.",
      steps: [
        "Put ginger shreds in the small dish, pour black vinegar over them. That is your dip.",
        "Lift one dumpling by the top pleat with chopsticks onto your spoon. Slowly. If the skin tears, the soup is gone.",
        "Bite a small hole in the side. Blow once. Sip the soup out of the hole.",
        "Now dip the rest in vinegar with a shred of ginger and eat it in one or two bites."
      ],
      where: "Jia Jia Tang Bao (佳家汤包), Huanghe Road, get there before 8:30. Nanxiang (南翔馒头店) at Yu Garden if you want the famous queue.",
      mistake: "Dipping the whole dumpling first and biting it in half. That is how you burn your lip and stain your shirt.",
      say: { zh: "一笼鲜肉小笼，一碗蛋皮汤。", py: "yì lóng xiān ròu xiǎo lóng, yì wǎn dàn pí tāng", en: "One steamer of pork soup dumplings, one egg-skin soup." }
    },
    {
      id: "bike", city: "everywhere", zh: "共享单车", title: "How to ride a shared bike", price: "≈1.5 RMB / 15 min",
      hook: "Yellow is Meituan, blue is HelloBike, teal is Qingju. All three unlock from inside Alipay, no separate app needed.",
      steps: [
        "Open Alipay, tap Scan (扫一扫), scan the QR plate on the handlebar. First time only: it asks for passport verification, about two minutes.",
        "Tap the blue confirm button. The rear lock clicks open. Adjust the seat before you set off, the lever is under the saddle.",
        "Ride in the bike lane on the right side of the road. Cars turn right through red lights, so look right at every crossing.",
        "Park inside a white-painted bike zone or a P icon on the app map. Push the rear lock lever down by hand. Your phone buzzes and shows the fare."
      ],
      where: "Every city on this trip. Best rides: Beijing's Second Ring hutongs, Shanghai's Former French Concession, Xi'an's city wall (rental bikes on top of the wall are separate).",
      mistake: "Parking outside the zone. The trip cannot end, the meter keeps running, and you get a 2–5 RMB penalty.",
      say: { zh: "这附近哪里可以停共享单车？", py: "zhè fù jìn nǎ lǐ kě yǐ tíng gòng xiǎng dān chē", en: "Where can I park a shared bike near here?" }
    },
    {
      id: "pay", city: "everywhere", zh: "扫码支付", title: "How to pay by QR code", price: "0 fee under 200 RMB",
      hook: "Nobody carries cash. Your Visa, JCB or Mastercard inside Alipay works at street stalls. PayPay, Kakao Pay and Naver Pay work at many shops too.",
      steps: [
        "Before flying: install Alipay, add your card, verify your passport. Do the same in WeChat Pay as a backup.",
        "Small shop shows a printed QR: tap Scan, scan it, type the amount they say, confirm. Show them the green tick.",
        "Big shop or convenience store: tap Pay (付钱), show your barcode, they scan it. Done in one second.",
        "Fees: nothing under 200 RMB per transaction, 3 percent above. So split large bills, or use your card directly at hotels."
      ],
      where: "Everywhere. Even the douzhi shop and the old man selling jianbing take QR. Keep about 300 RMB in cash for the rare exception.",
      mistake: "Trusting hotel Wi-Fi to verify your card. Do the setup at home, on your own network, a week before.",
      say: { zh: "可以用支付宝吗？", py: "kě yǐ yòng zhī fù bǎo ma", en: "Can I pay with Alipay?" }
    },
    {
      id: "metro", city: "everywhere", zh: "地铁", title: "How to ride the metro", price: "3–7 RMB a ride",
      hook: "Cheap, clean, exact. But there is an airport-style X-ray at every station door, and the staff may ask you to sip your water bottle.",
      steps: [
        "Bag on the belt, walk through the arch. If you carry a drink, sip it when they point at it. That proves it is water.",
        "In Alipay, tap Transport (出行), choose the city, and a ride QR appears. Hold it to the reader at the gate. Same code on the way out.",
        "No phone signal underground? Buy a single ticket at the machine with cash or by tapping your Alipay code on the screen.",
        "Stand right on escalators in Beijing. In Shanghai, no eating or drinking in the carriage, fines are real."
      ],
      where: "Beijing Line 1 for Tiananmen, Line 2 around the old city. Shanghai Line 2 links both airports through People's Square and the Bund.",
      mistake: "Arriving at 23:15. Most lines stop around 23:00 and taxis outside stations are the expensive kind.",
      say: { zh: "请问，去这里坐几号线？", py: "qǐng wèn, qù zhè lǐ zuò jǐ hào xiàn", en: "Which line goes here? (then show the address)" }
    },
    {
      id: "hotpot", city: "chengdu", zh: "火锅油碟", title: "How to build your hotpot dip", price: "100–150 RMB pp",
      hook: "Sichuan hotpot does not come with sauce. You mix it yourself from a bar, and the locals' bowl is nothing like what tourists make.",
      steps: [
        "Take a bowl, fill it one third with sesame oil (香油). This is the oil dish (油碟). It cools the chili, it does not add heat.",
        "Add a spoon of minced garlic, a pinch of coriander, a few drops of oyster sauce. Stop there. No peanut sauce, that is a northern thing.",
        "Order the broth as half-and-half (鸳鸯锅) and say mild (微辣). Mild still bites. Extra-mild does not exist.",
        "Tripe (毛肚) goes in for 15 seconds, swish it: seven up, eight down. Duck intestine 10 seconds. Potato slices 3 minutes."
      ],
      where: "Any branch of Xiaolongkan (小龙坎) or Shu Da Xia (蜀大侠) is fine. Skewer hotpot (串串) shops near Jinli are cheaper and more fun.",
      mistake: "Drinking the red broth from the ladle. It is 40 percent chili oil. It is not soup.",
      say: { zh: "鸳鸯锅，微辣。一份毛肚，一份土豆。", py: "yuān yāng guō, wēi là. yí fèn máo dǔ, yí fèn tǔ dòu", en: "Half-and-half pot, mild. One tripe, one potato." }
    },
    {
      id: "water", city: "everywhere", zh: "热水", title: "Why everyone hands you hot water", price: "0 RMB, always",
      hook: "Ask for water and you get boiling water. Ice is rare, and cold drinks are seen as bad for you. There is a free hot-water tap in every train, airport and mall.",
      steps: [
        "At a restaurant, water arrives hot in a small glass. If you want room temperature, say 常温 (cháng wēn). Cold: 冰的 (bīng de), often unavailable.",
        "Bring a thermos or buy one at any supermarket for 30 RMB. Refill at the hot-water dispensers (开水) on every high-speed train and station.",
        "Tea in a glass with loose leaves: wait, sip from the edge, leaves sink. Topping up with hot water is free and expected.",
        "Bottled water is 2 RMB at any shop. Tap water is not for drinking anywhere in China."
      ],
      where: "Every train carriage has a dispenser at the end. Every airport gate. Most hotel corridors.",
      mistake: "Asking for ice in a small local restaurant. They may not have any, and they will find it odd.",
      say: { zh: "一杯常温水，谢谢。", py: "yì bēi cháng wēn shuǐ, xiè xie", en: "A glass of room-temperature water, please." }
    },
    {
      id: "toilet", city: "everywhere", zh: "卫生间", title: "The toilet rules nobody writes down", price: "Free",
      hook: "Public toilets are everywhere and free. Half have no paper. Some are squat. You need a plan, not luck.",
      steps: [
        "Carry a pack of tissues, always. Buy at any convenience store: 纸巾 (zhǐ jīn), 2 RMB.",
        "Best toilets, in order: shopping malls, metro stations, hotel lobbies, Starbucks. Worst: parks and old hutong blocks.",
        "Squat toilet: face the hood, feet on the ridges, keep your phone in a zipped pocket. It is simpler than it looks.",
        "In older buildings, paper goes in the bin next to the toilet, not in the bowl. Look for a sign or a full bin."
      ],
      where: "Look for 卫生间, 洗手间 or 厕所. In malls, follow the WC sign, usually near the escalators on each floor.",
      mistake: "Leaving the hotel without tissues. That is the whole mistake.",
      say: { zh: "请问卫生间在哪里？", py: "qǐng wèn wèi shēng jiān zài nǎ lǐ", en: "Excuse me, where is the toilet?" }
    },
    /* ---- locked: teasers only ---- */
    {
      id: "roujiamo", city: "xian", zh: "肉夹馍", title: "How to order roujiamo and liangpi", price: "12–18 RMB", locked: true,
      hook: "Xi'an's meat sandwich has a quality tier the menu does not translate, and the cold noodles next to it are the real breakfast.",
      teaser: "Which of the two words on the board to say, the street that beats the Muslim Quarter, and how to get it without cilantro."
    },
    {
      id: "hsr", city: "everywhere", zh: "高铁", title: "How to take the high-speed train", price: "553–660 RMB BJ→SH", locked: true,
      hook: "Your passport is your ticket. There is a passport reader at the gate. The gate closes five minutes before departure and nobody waits.",
      teaser: "12306 vs Trip.com, which side of the train to sit on, luggage that fits, and the 20-minute security trap at Beijing South."
    },
    {
      id: "didi", city: "everywhere", zh: "滴滴", title: "How to hail a Didi without speaking", price: "15–40 RMB in town", locked: true,
      hook: "China's Uber lives inside Alipay as a mini-program in English. The driver will call you anyway. Here is what to do about that.",
      teaser: "Setting a pickup point the driver can find, matching the plate, the one sentence to send back when they call, and the phrase for stop here."
    },
    {
      id: "duck", city: "beijing", zh: "烤鸭", title: "How to roll Peking duck", price: "200–300 RMB whole", locked: true,
      hook: "The first piece of skin is meant to be dipped in sugar. Most tourists never find out.",
      teaser: "Half-duck ordering for two, the pancake fold, sugar first, and the restaurant with no 90-minute queue."
    },
    {
      id: "jianbing", city: "beijing", zh: "煎饼果子", title: "How to order a jianbing at 7 a.m.", price: "6–10 RMB", locked: true,
      hook: "The breakfast crepe from a bicycle cart. Four choices to make in five seconds while the lady is already pouring the batter.",
      teaser: "Egg, crisp, sauce, cilantro: the words for each, the order she expects, and how to say no spice."
    },
    {
      id: "gaiwan", city: "chengdu", zh: "盖碗茶", title: "How to hold a gaiwan", price: "15–30 RMB, free refills", locked: true,
      hook: "The lidded teacup in a Chengdu teahouse. Hold it wrong and it spills; hold it right and you can sit there for four hours.",
      teaser: "Lid, cup, saucer: which fingers go where, how to signal a refill without a word, and the teahouse in People's Park with ear-cleaners."
    }
  ],

  days: [
    { city: "beijing", zh: "北京", label: "Arrive", items: ["Airport express or Daxing line into the city, first QR payment at the 7-Eleven by the exit.", "Check in near Gulou. Walk Shichahai lake at dusk, rent a bike on the way back.", "Dinner: dumplings on a side hutong, not the main tourist lane."],
      lock: "Which airport line for your terminal, eSIM to activate before landing, hotels that actually register foreigners." },
    { city: "beijing", zh: "北京", label: "Old city", items: ["6:30 douzhi at the Temple of Heaven north gate, then tai chi in the park.", "Forbidden City from the south gate, out the north, up Jingshan for the view.", "Evening: Qianmen back streets, shared bike home."],
      lock: "Booking the Forbidden City on WeChat with a passport seven days out, and what to do when it is sold out." },
    { city: "beijing", zh: "北京", label: "Great Wall", items: ["Mutianyu section: less crowded, toboggan down.", "Leave at 7:00, back by 15:00.", "Dinner: Peking duck, half a bird for two."],
      lock: "Bus 916 vs Didi cost math, cable car vs chairlift, and the duck place that does not need a queue." },
    { city: "shanghai", zh: "上海", label: "Train day", items: ["G-train from Beijing South, 4.5 hours, second class is fine.", "Arrive Hongqiao, metro Line 2 straight into town.", "The Bund at night, seen from the Pudong side."],
      lock: "Seat side for the view, luggage that fits the rack, and the 20-minute security trap at Beijing South." },
    { city: "shanghai", zh: "上海", label: "Dumplings and bikes", items: ["Soup dumplings at Jia Jia before 8:30.", "Yu Garden edges, then skip the garden itself if the queue is long.", "Bike through the Former French Concession, Wukang Road at 16:00 light."],
      lock: "Bike parking zones on Wukang Road, ordering by picture, and dumpling shop hours that change on holidays." },
    { city: "suzhou", zh: "苏州", label: "Day trip", items: ["25-minute train to Suzhou, book the day before.", "Humble Administrator's Garden early, Pingjiang Road canal after.", "Back in Shanghai for a rooftop drink."],
      lock: "Garden reservations with a passport, which canal boat, and the noodle shop that opens at 6:30." },
    { city: "shanghai", zh: "上海", label: "Depart", items: ["Maglev to Pudong airport in 8 minutes, or Line 2 for Hongqiao.", "Tax refund desk if you spent over 200 RMB in one shop.", "Last hot water refill at the gate."],
      lock: "Tax-refund desk locations, the paperwork the shop must give you, and the 90-minute buffer rule." }
  ],

  tiers: [
    { name: "Free", price: "0", cur: "", sub: "this page", items: ["8 detail cards", "7-day skeleton", "14 point-and-say phrases", "FAQ"], cta: "free" },
    { name: "Full guide", price: "2", cur: "USD", alt: "¥300 · ₩2,800", sub: "one-time, less than a bowl of douzhi", hero: true, tag: "Everything", items: ["7 days, hour by hour", "Chinese address for every stop, paste into Didi", "60 point-and-say cards", "Rain plans for each day", "Offline PDF + this site unlocked", "Free updates through 2026"], cta: "buy", link: "pack" }
  ],

  faq: [
    { q: "Do I need a visa?", a: "As of 2026, Japanese and Korean passports enter visa-free for up to 30 days under a trial policy that has been extended several times. Most European passports also get 30 days. Others can use the 240-hour transit exemption when flying onward to a third country. Check your embassy's site the week before you fly; this changes." },
    { q: "Will my phone work? Google, LINE, KakaoTalk?", a: "On local networks they are blocked. Buy an international roaming eSIM before you leave (Ubigi, Airalo, or your carrier's roaming). Traffic routes through your home country and everything works without a VPN. Hotel Wi-Fi is a local network, so switch back to mobile data when you need Google Maps." },
    { q: "Cash or apps?", a: "Alipay with your home card covers 95 percent of the trip. Set it up at home. Carry about 300 RMB in small notes for the rest. Bank of China ATMs accept foreign cards." },
    { q: "How much English is there?", a: "Hotels and airports, yes. Restaurants, taxis and shops, mostly no. That is why every card here ends with a phrase to show. Download the Chinese pack for your translate app's camera before you fly." },
    { q: "Is it safe? Do I tip?", a: "Very safe, including late at night. No tipping anywhere, not restaurants, not taxis, not hotels. Keep your passport on you: trains, museums and some parks check it at the gate." }
  ]
};
