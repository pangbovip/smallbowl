/* Small Bowl China — page logic
   Config you will edit: PAY_LINKS, UNLOCK_CODES, MAIL_ENDPOINT */
(function () {
  "use strict";

  // 1. Payment links. Replace with your Stripe Payment Link / Gumroad / Lemon Squeezy URLs.
  var PAY_LINKS = {
    pack: "https://buy.stripe.com/REPLACE_ME_pack"   // US$2 one-time
  };
  // 2. Unlock codes you send after purchase. Client-side only: good enough to gate a guide, not a bank.
  //    For real license checks use Gumroad's license API or Lemon Squeezy license keys (see README).
  var UNLOCK_CODES = ["SMALLBOWL-DEMO", "XIAOWAN2026"];
  // 3. Newsletter endpoint (Buttondown / Mailchimp / Formspree). Empty = store locally, no network.
  var MAIL_ENDPOINT = "";

  var LANGS = ["en", "ja", "ko"];
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  var state = {
    lang: pickLang(),
    unlocked: safeGet("sb_unlocked") === "1",
    filter: "all"
  };

  function pickLang() {
    var saved = safeGet("sb_lang");
    if (LANGS.indexOf(saved) >= 0) return saved;
    var nav = (navigator.language || "en").toLowerCase();
    if (nav.indexOf("ja") === 0) return "ja";
    if (nav.indexOf("ko") === 0) return "ko";
    return "en";
  }
  function safeGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function safeSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function t(key) { var d = window.I18N[state.lang] || window.I18N.en; return d[key] != null ? d[key] : (window.I18N.en[key] || key); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  /* ---------- render ---------- */
  function renderAll() {
    document.documentElement.lang = state.lang;
    $$("[data-i18n]").forEach(function (el) { el.textContent = t(el.getAttribute("data-i18n")); });
    $$("[data-i18n-placeholder]").forEach(function (el) { el.placeholder = t(el.getAttribute("data-i18n-placeholder")); });
    $$(".lang button").forEach(function (b) { b.classList.toggle("is-on", b.getAttribute("data-lang") === state.lang); });
    renderBoard(); renderDays(); renderTiers(); renderFaq();
  }

  function sayCardHTML(say, extraClass) {
    return '<button type="button" class="say-card ' + (extraClass || "") + '" data-say="' + esc(say.zh) + '" data-say-pinyin="' + esc(say.py) + '">' +
      '<span class="say-zh">' + esc(say.zh) + '</span>' +
      '<span class="say-pinyin">' + esc(say.py) + '</span>' +
      '<span class="say-meaning">' + esc(say.en) + '</span>' +
      '<span class="say-hint">' + esc(t("hero.demoHint")) + '</span></button>';
  }

  function renderBoard() {
    var c = window.CONTENT[state.lang];
    var html = c.cards.map(function (card) {
      var locked = card.locked && !state.unlocked;
      var city = c.cityNames[card.city] || card.city;
      var body;
      if (card.locked) {
        // Locked cards ship teaser only; the full body lives in the paid guide (content-paid-*.js after unlock).
        var paid = window.PAID && window.PAID[state.lang] && window.PAID[state.lang][card.id];
        if (state.unlocked && paid) card = Object.assign({}, card, paid);
      }
      if (locked || !card.steps) {
        body = '<div class="card-body"><p class="hook">' + esc(card.hook) + '</p>' +
          '<ol class="steps"><li>' + esc(card.teaser || "") + '</li><li>&nbsp;</li><li>&nbsp;</li></ol></div>' +
          '<div class="card-foot"><div class="say-card"><span class="say-zh">……</span><span class="say-pinyin">&nbsp;</span></div></div>' +
          '<div class="lock">' + esc(card.zh) + '<small>' + esc(t("card.locked")) + '</small></div>' +
          '<a class="btn btn-seal btn-small lock-btn" href="#pricing">' + esc(t("card.unlock")) + '</a>';
      } else {
        body = '<div class="card-body"><p class="hook">' + esc(card.hook) + '</p>' +
          '<ol class="steps">' + card.steps.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + '</ol>' +
          '<dl class="kv"><dt>' + esc(t("card.where")) + '</dt><dd>' + esc(card.where) + '</dd>' +
          '<dt>' + esc(t("card.mistake")) + '</dt><dd class="mistake">' + esc(card.mistake) + '</dd></dl></div>' +
          '<div class="card-foot">' + sayCardHTML(card.say) + '</div>';
      }
      return '<article class="card' + (locked ? " is-locked" : "") + '" data-city="' + esc(card.city) + '" id="card-' + esc(card.id) + '">' +
        '<div class="card-head"><div class="card-name"><span class="card-zh">' + esc(card.zh) + '</span>' +
        '<h3 class="card-title">' + esc(card.title) + '</h3><span class="card-city">' + esc(city) + '</span></div>' +
        '<span class="price">' + esc(card.price) + '</span></div>' + body + '</article>';
    }).join("");
    $("#board").innerHTML = html;
    applyFilter();
  }

  function applyFilter() {
    $$(".chip").forEach(function (b) { b.classList.toggle("is-on", b.getAttribute("data-filter") === state.filter); });
    $$(".card").forEach(function (card) {
      var show = state.filter === "all" || card.getAttribute("data-city") === state.filter;
      card.hidden = !show;
    });
  }

  function renderDays() {
    var c = window.CONTENT[state.lang];
    $("#daysGrid").innerHTML = c.days.map(function (d, i) {
      var paid = window.PAID && window.PAID[state.lang] && window.PAID[state.lang]["day" + (i + 1)];
      var lockBlock = state.unlocked && paid
        ? '<div class="day-lock is-open"><b>' + esc(t("day.locked")) + '</b>' + paid.map(function (s) { return "<span>" + esc(s) + "</span>"; }).join("") + '</div>'
        : '<div class="day-lock"><b>' + esc(t("day.locked")) + '</b><span>' + esc(d.lock) + '</span></div>';
      return '<div class="day"><span class="day-num">' + esc(t("day.n")) + " " + (i + 1) + '</span>' +
        '<div class="day-city">' + esc(d.zh) + '<span>' + esc(c.cityNames[d.city] || d.city) + " · " + esc(d.label) + '</span></div>' +
        '<ul class="day-list">' + d.items.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + '</ul>' + lockBlock + '</div>';
    }).join("");
  }

  function renderTiers() {
    var c = window.CONTENT[state.lang];
    $("#tiers").innerHTML = c.tiers.map(function (tier) {
      var cta = tier.cta === "free"
        ? '<span class="btn btn-ghost" aria-disabled="true">' + esc(t("tier.free")) + '</span>'
        : '<a class="btn ' + (tier.hero ? "btn-seal" : "btn-primary") + '" href="' + esc(PAY_LINKS[tier.link] || "#") + '" target="_blank" rel="noopener">' + esc(t("tier.buy")) + " · " + esc(tier.name) + '</a>';
      var price = tier.cur
        ? '<strong>' + esc(tier.cur === "USD" ? "$" + tier.price : tier.cur === "JPY" ? "¥" + tier.price : "₩" + tier.price) + '</strong><span>' + esc((tier.alt ? tier.alt + " · " : "") + tier.sub) + '</span>'
        : '<strong>0</strong><span>' + esc(tier.sub) + '</span>';
      return '<div class="tier' + (tier.hero ? " is-hero" : "") + '" data-tag="' + esc(tier.tag || "") + '">' +
        '<h3>' + esc(tier.name) + '</h3><div class="tier-price">' + price + '</div>' +
        '<ul>' + tier.items.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + '</ul>' + cta + '</div>';
    }).join("");
  }

  function renderFaq() {
    var c = window.CONTENT[state.lang];
    $("#faqList").innerHTML = c.faq.map(function (f, i) {
      return '<details' + (i === 0 ? " open" : "") + '><summary>' + esc(f.q) + '</summary><div class="faq-body">' + esc(f.a) + '</div></details>';
    }).join("");
  }

  /* ---------- point-and-say overlay ---------- */
  var overlay = $("#sayOverlay");
  function openSay(zh, py) {
    $("#sayZh").textContent = zh; $("#sayPinyin").textContent = py;
    overlay.hidden = false; $("#sayClose").focus();
    document.body.style.overflow = "hidden";
  }
  function closeSay() { overlay.hidden = true; document.body.style.overflow = ""; }
  document.addEventListener("click", function (e) {
    var card = e.target.closest && e.target.closest(".say-card[data-say]");
    if (card && !card.closest(".is-locked")) { openSay(card.getAttribute("data-say"), card.getAttribute("data-say-pinyin")); return; }
    if (e.target === overlay || e.target.closest && e.target.closest("#sayClose")) closeSay();
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !overlay.hidden) closeSay(); });

  /* ---------- controls ---------- */
  $$(".lang button").forEach(function (b) {
    b.addEventListener("click", function () { state.lang = b.getAttribute("data-lang"); safeSet("sb_lang", state.lang); renderAll(); });
  });
  $(".filters").addEventListener("click", function (e) {
    var chip = e.target.closest(".chip"); if (!chip) return;
    state.filter = chip.getAttribute("data-filter"); applyFilter();
  });
  $("#codeBtn").addEventListener("click", tryUnlock);
  $("#codeInput").addEventListener("keydown", function (e) { if (e.key === "Enter") tryUnlock(); });
  function tryUnlock() {
    var code = $("#codeInput").value.trim().toUpperCase();
    var msg = $("#codeMsg");
    if (UNLOCK_CODES.indexOf(code) >= 0) {
      state.unlocked = true; safeSet("sb_unlocked", "1");
      msg.textContent = t("pricing.codeOk"); msg.className = "unlock-msg ok"; renderAll();
    } else { msg.textContent = t("pricing.codeBad"); msg.className = "unlock-msg"; }
  }
  // ?code=XXXX in the URL (put it in the purchase email) unlocks without typing
  var m = /[?&]code=([^&]+)/.exec(location.search);
  if (m && UNLOCK_CODES.indexOf(decodeURIComponent(m[1]).toUpperCase()) >= 0) { state.unlocked = true; safeSet("sb_unlocked", "1"); }

  $("#mailForm").addEventListener("submit", function (e) {
    e.preventDefault();
    var email = $("#mailInput").value.trim(); var msg = $("#mailMsg");
    var done = function () { msg.textContent = t("foot.mailOk"); msg.className = "unlock-msg ok"; $("#mailInput").value = ""; };
    if (!MAIL_ENDPOINT) { safeSet("sb_mail", email); done(); return; }
    fetch(MAIL_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email: email, lang: state.lang }) })
      .then(done, function () { msg.textContent = "Could not save. Try again."; msg.className = "unlock-msg"; });
  });

  renderAll();
})();
