/* Small Bowl China — page logic
   Config you will edit: PAYPAL_CLIENT_ID, PRICE_USD, VERIFY_ENDPOINT, UNLOCK_CODES, MAIL_ENDPOINT */
(function () {
  "use strict";

  // 1. PayPal. Same business account as wenguhall.com (client ID is public by design).
  var PAYPAL_CLIENT_ID = "AZAUdHJ_fPObN-WAMZWZNRT5F2DBm262FCzEXr95R71042sUsGrIqtQUp8oclUDGJJ4-KjBLeuA08Gvw";
  var PRICE_USD = "2.00";
  // 2. Optional Cloudflare Worker that verifies payments with PayPal and stores codes (see worker/).
  //    Empty = no backend: unlock happens on this device and the code is "SB-" + PayPal transaction ID.
  var VERIFY_ENDPOINT = "";
  // 3. Hand-issued codes (refunds, friends, press). Remove SMALLBOWL-DEMO before launch.
  var UNLOCK_CODES = ["SMALLBOWL-DEMO"];
  // 4. Newsletter endpoint (Buttondown / Mailchimp / Formspree). Empty = store locally, no network.
  var MAIL_ENDPOINT = "";

  var LANGS = ["en", "ja", "ko"];
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  var state = {
    lang: pickLang(),
    unlocked: safeGet("sb_unlocked") === "1",
    code: safeGet("sb_code") || "",
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
        var paid = paidData() && paidData().cards && paidData().cards[card.id];
        if (state.unlocked && paid) card = Object.assign({}, card, paid);
      }
      if (locked || !card.steps) {
        body = '<div class="card-body"><p class="hook">' + esc(card.hook) + '</p>' +
          '<ol class="steps"><li>' + esc(card.teaser || "") + '</li><li>&nbsp;</li><li>&nbsp;</li></ol></div>' +
          '<div class="card-foot"><div class="say-card"><span class="say-zh">……</span><span class="say-pinyin">&nbsp;</span></div></div>' +
          '<div class="lock">' + esc(card.zh) + '<small>' + esc(t("card.locked")) + '</small></div>' +
          '<button type="button" class="btn btn-seal btn-small lock-btn" data-buy>' + esc(t("card.unlock")) + '</button>';
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

  function paidData() { return window.PAID && (window.PAID[state.lang] || window.PAID.en); }

  function renderDays() {
    var c = window.CONTENT[state.lang];
    var p = paidData();
    $("#daysGrid").innerHTML = c.days.map(function (d, i) {
      var open = state.unlocked && p && p.days && p.days[i];
      var lockBlock = open
        ? '<div class="day-lock is-open"><b>' + esc(t("day.locked")) + '</b><a href="#plan-day-' + (i + 1) + '">' + esc(t("day.openLink")) + '</a></div>'
        : '<div class="day-lock"><b>' + esc(t("day.locked")) + '</b><span>' + esc(d.lock) + '</span></div>';
      return '<div class="day"><span class="day-num">' + esc(t("day.n")) + " " + (i + 1) + '</span>' +
        '<div class="day-city">' + esc(d.zh) + '<span>' + esc(c.cityNames[d.city] || d.city) + " · " + esc(d.label) + '</span></div>' +
        '<ul class="day-list">' + d.items.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + '</ul>' + lockBlock + '</div>';
    }).join("");
    renderFullPlan();
  }

  // Paid sections: hour-by-hour plan per day, and the general phrasebook. Only rendered when unlocked.
  function renderFullPlan() {
    var c = window.CONTENT[state.lang];
    var p = paidData();
    var planSec = $("#fullplan"), bookSec = $("#phrasebook");
    var show = state.unlocked && p && p.days;
    planSec.hidden = !show; bookSec.hidden = !show;
    if (!show) { $("#planList").innerHTML = ""; $("#bookList").innerHTML = ""; return; }
    $("#planList").innerHTML = p.days.map(function (day, i) {
      var d = c.days[i] || {};
      var rows = day.plan.map(function (s) {
        return '<tr><td class="plan-t">' + esc(s.t) + '</td>' +
          '<td class="plan-zh"><button type="button" class="say-inline" data-say="' + esc(s.zh) + '" data-say-pinyin="">' + esc(s.zh) + '</button></td>' +
          '<td class="plan-what">' + esc(s.what) + '</td></tr>';
      }).join("");
      var says = day.say.map(function (s) { return sayCardHTML(s, "say-card-mini"); }).join("");
      return '<section class="plan-day" id="plan-day-' + (i + 1) + '">' +
        '<header class="plan-head"><span class="day-num">' + esc(t("day.n")) + " " + (i + 1) + '</span>' +
        '<h3><span class="plan-city">' + esc(d.zh || "") + '</span> ' + esc((c.cityNames[d.city] || d.city || "") + " · " + (d.label || "")) + '</h3></header>' +
        '<div class="plan-table-wrap"><table class="plan-table"><thead><tr><th>' + esc(t("plan.time")) + '</th><th>' + esc(t("plan.show")) + '</th><th>' + esc(t("plan.what")) + '</th></tr></thead><tbody>' + rows + '</tbody></table></div>' +
        '<p class="plan-rain"><b>' + esc(t("plan.rain")) + '</b> ' + esc(day.rain) + '</p>' +
        '<p class="plan-say-label">' + esc(t("plan.say")) + '</p><div class="say-grid">' + says + '</div>' +
        '</section>';
    }).join("");
    $("#bookList").innerHTML = (p.phrasebook || []).map(function (s) { return sayCardHTML(s, "say-card-mini"); }).join("");
  }

  function renderTiers() {
    var c = window.CONTENT[state.lang];
    $("#tiers").innerHTML = c.tiers.map(function (tier) {
      var cta;
      if (tier.cta === "free") cta = '<span class="btn btn-ghost" aria-disabled="true">' + esc(t("tier.free")) + '</span>';
      else if (state.unlocked) cta = '<span class="btn btn-ghost" aria-disabled="true">' + esc(t("tier.owned")) + '</span>';
      else cta = '<button type="button" class="btn btn-seal" data-buy>' + esc(t("tier.buy")) + " · $" + PRICE_USD.replace(/\.00$/, "") + '</button>';
      var price = tier.cur
        ? '<strong>' + esc(tier.cur === "USD" ? "$" + tier.price : tier.cur === "JPY" ? "¥" + tier.price : "₩" + tier.price) + '</strong><span>' + esc((tier.alt ? tier.alt + " · " : "") + tier.sub) + '</span>'
        : '<strong>0</strong><span>' + esc(tier.sub) + '</span>';
      return '<div class="tier' + (tier.hero ? " is-hero" : "") + '" data-tag="' + esc(tier.tag || "") + '">' +
        '<h3>' + esc(tier.name) + '</h3><div class="tier-price">' + price + '</div>' +
        '<ul>' + tier.items.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + '</ul>' + cta + '</div>';
    }).join("");
    var row = $(".unlock-row");
    if (row) row.hidden = state.unlocked;
    var owned = $("#ownedRow");
    if (owned) { owned.hidden = !state.unlocked; $("#ownedCode").textContent = state.code; }
  }

  function renderFaq() {
    var c = window.CONTENT[state.lang];
    $("#faqList").innerHTML = c.faq.map(function (f, i) {
      return '<details' + (i === 0 ? " open" : "") + '><summary>' + esc(f.q) + '</summary><div class="faq-body">' + esc(f.a) + '</div></details>';
    }).join("");
  }

  /* ---------- unlock ---------- */
  function unlock(code) {
    state.unlocked = true; state.code = code || state.code;
    safeSet("sb_unlocked", "1"); if (state.code) safeSet("sb_code", state.code);
    renderAll();
  }
  // Returns a Promise<boolean>. With a worker, the code is checked server-side; without one,
  // hand-issued codes and the "SB-" + PayPal transaction ID shape are accepted on the client.
  function validateCode(code) {
    code = code.trim().toUpperCase();
    if (!code) return Promise.resolve(false);
    if (UNLOCK_CODES.indexOf(code) >= 0) return Promise.resolve(true);
    if (VERIFY_ENDPOINT) {
      return fetch(VERIFY_ENDPOINT + "/check?code=" + encodeURIComponent(code))
        .then(function (r) { return r.json(); }).then(function (j) { return !!j.ok; }, function () { return false; });
    }
    return Promise.resolve(/^SB-[A-Z0-9]{12,20}$/.test(code));
  }
  function tryUnlock() {
    var code = $("#codeInput").value.trim().toUpperCase();
    var msg = $("#codeMsg");
    msg.textContent = "…"; msg.className = "unlock-msg";
    validateCode(code).then(function (ok) {
      if (ok) { msg.textContent = ""; unlock(code); }
      else { msg.textContent = t("pricing.codeBad"); msg.className = "unlock-msg"; }
    });
  }
  $("#codeBtn").addEventListener("click", tryUnlock);
  $("#codeInput").addEventListener("keydown", function (e) { if (e.key === "Enter") tryUnlock(); });
  var m = /[?&]code=([^&]+)/.exec(location.search);
  if (m) { validateCode(decodeURIComponent(m[1])).then(function (ok) { if (ok) unlock(decodeURIComponent(m[1]).toUpperCase()); }); }

  /* ---------- PayPal checkout modal ---------- */
  var payOverlay = $("#payOverlay"), paypalLoaded = false, paypalRendered = false;
  function openPay() {
    payOverlay.hidden = false; document.body.style.overflow = "hidden";
    $("#payDone").hidden = true; $("#payErr").textContent = "";
    $("#payButtons").hidden = false;
    loadPayPal();
  }
  function closePay() { payOverlay.hidden = true; document.body.style.overflow = ""; }
  function loadPayPal() {
    if (paypalRendered) return;
    if (paypalLoaded) { renderButtons(); return; }
    paypalLoaded = true;
    $("#payLoading").hidden = false;
    var s = document.createElement("script");
    s.src = "https://www.paypal.com/sdk/js?client-id=" + PAYPAL_CLIENT_ID + "&currency=USD&intent=capture&disable-funding=paylater&locale=" + ({ en: "en_US", ja: "ja_JP", ko: "ko_KR" }[state.lang]);
    s.onload = renderButtons;
    s.onerror = function () { $("#payLoading").hidden = true; $("#payErr").textContent = t("pay.loadError"); paypalLoaded = false; };
    document.head.appendChild(s);
  }
  function renderButtons() {
    if (paypalRendered || !window.paypal) return;
    paypalRendered = true;
    $("#payLoading").hidden = true;
    window.paypal.Buttons({
      style: { layout: "vertical", color: "black", shape: "rect", height: 44, tagline: false },
      createOrder: function (data, actions) {
        return actions.order.create({
          purchase_units: [{ amount: { value: PRICE_USD, currency_code: "USD" }, description: "Small Bowl China: full 7-day guide (chinavisit.org)" }],
          application_context: { shipping_preference: "NO_SHIPPING", brand_name: "Small Bowl China" }
        });
      },
      onApprove: function (data, actions) {
        return actions.order.capture().then(function (details) {
          var cap = details && details.purchase_units && details.purchase_units[0].payments && details.purchase_units[0].payments.captures;
          var txn = (cap && cap[0] && cap[0].id) || data.orderID;
          return issueCode(txn, data.orderID).then(function (code) {
            unlock(code);
            $("#payButtons").hidden = true;
            $("#payCode").textContent = code;
            $("#payDone").hidden = false;
          });
        }).catch(function () { $("#payErr").textContent = t("pay.error"); });
      },
      onError: function () { $("#payErr").textContent = t("pay.error"); }
    }).render("#payButtons");
  }
  // The code is the PayPal transaction ID with an SB- prefix, so a buyer can always recover it
  // from their PayPal receipt email. With a worker, the worker verifies the capture and stores it.
  function issueCode(txnId, orderId) {
    var code = "SB-" + String(txnId).toUpperCase();
    if (!VERIFY_ENDPOINT) return Promise.resolve(code);
    return fetch(VERIFY_ENDPOINT + "/issue", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ captureId: txnId, orderId: orderId }) })
      .then(function (r) { return r.json(); }).then(function (j) { return j.code || code; }, function () { return code; });
  }
  document.addEventListener("click", function (e) {
    if (e.target.closest && e.target.closest("[data-buy]")) { e.preventDefault(); openPay(); return; }
    if (e.target === payOverlay || (e.target.closest && e.target.closest("#payClose"))) closePay();
  });
  $("#payCopy").addEventListener("click", function () {
    var code = $("#payCode").textContent;
    var done = function () { $("#payCopy").textContent = t("pay.copied"); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(code).then(done, done); else done();
  });

  /* ---------- point-and-say overlay ---------- */
  var overlay = $("#sayOverlay");
  function openSay(zh, py) {
    $("#sayZh").textContent = zh; $("#sayPinyin").textContent = py;
    overlay.hidden = false; $("#sayClose").focus();
    document.body.style.overflow = "hidden";
  }
  function closeSay() { overlay.hidden = true; document.body.style.overflow = ""; }
  document.addEventListener("click", function (e) {
    var card = e.target.closest && e.target.closest(".say-card[data-say], .say-inline[data-say]");
    if (card && !card.closest(".is-locked")) { openSay(card.getAttribute("data-say"), card.getAttribute("data-say-pinyin")); return; }
    if (e.target === overlay || e.target.closest && e.target.closest("#sayClose")) closeSay();
  });
  var printBtn = $("#printBtn");
  if (printBtn) printBtn.addEventListener("click", function () { window.print(); });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    if (!overlay.hidden) closeSay();
    if (!payOverlay.hidden) closePay();
  });

  /* ---------- controls ---------- */
  $$(".lang button").forEach(function (b) {
    b.addEventListener("click", function () { state.lang = b.getAttribute("data-lang"); safeSet("sb_lang", state.lang); renderAll(); });
  });
  $(".filters").addEventListener("click", function (e) {
    var chip = e.target.closest(".chip"); if (!chip) return;
    state.filter = chip.getAttribute("data-filter"); applyFilter();
  });

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
