/* Paid content: what the unlock code reveals.
   Keep this file OUT of the public deploy if you want the paywall to be real —
   serve it only after purchase, or move the real text into the PDF and leave this as a sample.
   Shape: PAID[lang][cardId] = { steps, where, mistake, say }; PAID[lang]["dayN"] = [lines] */
window.PAID = {
  en: {
    duck: {
      steps: [
        "Two people: order half a duck (半只). Whole (一只) only for four. It comes carved, with pancakes, scallion, cucumber, sweet bean sauce and a dish of sugar.",
        "First piece of skin only: dip in sugar, eat it plain. That is the chef's test piece. Then start rolling.",
        "Pancake flat on your palm. Sauce with the back of the scallion, 2 pieces duck, 2 scallion, 1 cucumber. Fold the bottom up, then the sides. Never the top.",
        "Ask for the bones as soup (鸭架汤) at the end. It is included and most tourists leave without it."
      ],
      where: "Siji Minfu (四季民福), Dengshikou branch, book on their WeChat or go at 16:45. Jingzun (京尊) near Sanlitun has no queue and the same quality.",
      mistake: "Quanjude on Qianmen at 18:30. Ninety minutes of queue for a tour-group duck.",
      say: { zh: "半只烤鸭，鸭架做汤。", py: "bàn zhī kǎo yā, yā jià zuò tāng", en: "Half a roast duck, bones as soup." }
    },
    day1: ["PEK Terminal 3: Airport Express to Dongzhimen, 25 RMB, then Line 2 one stop to Gulou. PKX: Daxing Airport Express to Caoqiao, 35 RMB, then Line 10.", "eSIM: activate on the plane before landing; hotel Wi-Fi cannot verify anything.", "Hutong hotels that register foreigners: search the booking site filter 'accepts foreign guests' and message to confirm the night before."]
  },
  ja: {
    duck: {
      steps: [
        "2人なら半羽（半只）。1羽（一只）は4人用。切り分けた鴨、薄餅、ネギ、キュウリ、甜麺醤、砂糖の小皿が来る。",
        "最初の皮一切れだけ：砂糖につけてそのまま食べる。料理長の試食用の一切れ。それから巻き始める。",
        "薄餅を手のひらに。ネギの背でタレを塗り、鴨2切れ、ネギ2本、キュウリ1本。下を折り上げ、両側を折る。上は折らない。",
        "最後に骨をスープに（鸭架汤）。料金に含まれていて、ほとんどの観光客は頼まずに帰る。"
      ],
      where: "四季民福 灯市口店、WeChatで予約か16時45分に行く。三里屯近くの京尊は行列なしで同じ品質。",
      mistake: "18時30分の前門・全聚徳。団体客向けの鴨に90分並ぶ。",
      say: { zh: "半只烤鸭，鸭架做汤。", py: "bàn zhī kǎo yā, yā jià zuò tāng", en: "北京ダック半羽、骨はスープに。" }
    },
    day1: ["首都空港T3：空港快速で東直門まで25元、2号線で1駅の鼓楼へ。大興空港：大興空港快速で草橋まで35元、10号線へ。", "eSIM：着陸前に機内で有効化。ホテルWi-Fiでは何も認証できない。", "外国人を登録できる胡同ホテル：予約サイトで「外国人受け入れ可」を絞り込み、前夜にメッセージで確認。"]
  },
  ko: {
    duck: {
      steps: [
        "둘이면 반 마리(半只). 한 마리(一只)는 넷용. 썰린 오리, 밀전병, 파채, 오이, 톈몐장, 설탕 접시가 온다.",
        "첫 껍질 한 조각만: 설탕에 찍어 그대로 먹는다. 주방장의 시식 조각. 그다음 싸기 시작.",
        "전병을 손바닥에 편다. 파 뒷면으로 소스를 바르고 오리 2조각, 파 2개, 오이 1개. 아래를 접어 올리고 양옆을 접는다. 위는 절대 안 접는다.",
        "마지막에 뼈를 탕으로(鸭架汤). 포함된 것인데 관광객 대부분이 안 시키고 간다."
      ],
      where: "쓰지민푸(四季民福) 덩스커우점, 위챗 예약 또는 16시 45분 도착. 싼리툰 근처 징쭌(京尊)은 줄 없이 같은 품질.",
      mistake: "18시 30분 첸먼 취안쥐더. 단체 관광객용 오리에 90분 줄.",
      say: { zh: "半只烤鸭，鸭架做汤。", py: "bàn zhī kǎo yā, yā jià zuò tāng", en: "오리 반 마리, 뼈는 탕으로." }
    },
    day1: ["서우두공항 T3: 공항고속으로 둥즈먼까지 25위안, 2호선 한 정거장 구러우. 다싱공항: 다싱공항선으로 차오차오까지 35위안, 10호선 환승.", "eSIM: 착륙 전 기내에서 활성화. 호텔 와이파이로는 아무것도 인증 안 된다.", "외국인 등록 가능한 후통 호텔: 예약 사이트에서 '외국인 투숙 가능' 필터, 전날 밤 메시지로 확인."]
  }
};
