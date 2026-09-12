/* Small Bowl unlock-code verifier — Cloudflare Worker
   Routes:
     POST /issue  { captureId, orderId }  -> verifies the PayPal capture (COMPLETED, 2.00 USD), stores code, returns { code }
     GET  /check?code=SB-XXXX             -> { ok: true|false }
   Bindings: KV namespace CODES; secrets PAYPAL_CLIENT_ID, PAYPAL_SECRET; var PRICE_USD, ALLOWED_ORIGIN */

const PAYPAL_API = "https://api-m.paypal.com"; // live. Sandbox: https://api-m.sandbox.paypal.com

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const cors = corsHeaders(request, env);
    if (request.method === "OPTIONS") return new Response(null, { headers: cors });

    try {
      if (url.pathname === "/check" && request.method === "GET") {
        const code = (url.searchParams.get("code") || "").trim().toUpperCase();
        const hit = code && (await env.CODES.get(code));
        return json({ ok: !!hit }, cors);
      }

      if (url.pathname === "/issue" && request.method === "POST") {
        const { captureId } = await request.json();
        if (!captureId || !/^[A-Z0-9]{8,32}$/i.test(captureId)) return json({ error: "bad capture id" }, cors, 400);
        const code = "SB-" + String(captureId).toUpperCase();
        if (await env.CODES.get(code)) return json({ code }, cors);

        const token = await paypalToken(env);
        const r = await fetch(`${PAYPAL_API}/v2/payments/captures/${encodeURIComponent(captureId)}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (!r.ok) return json({ error: "capture not found" }, cors, 404);
        const cap = await r.json();
        const okStatus = cap.status === "COMPLETED";
        const okAmount = cap.amount && cap.amount.currency_code === "USD" && Number(cap.amount.value) >= Number(env.PRICE_USD || "2.00");
        if (!okStatus || !okAmount) return json({ error: "capture not valid", status: cap.status }, cors, 402);

        await env.CODES.put(code, JSON.stringify({ captureId, amount: cap.amount, at: new Date().toISOString() }));
        return json({ code }, cors);
      }

      return json({ error: "not found" }, cors, 404);
    } catch (e) {
      return json({ error: "server error" }, cors, 500);
    }
  }
};

async function paypalToken(env) {
  const basic = btoa(`${env.PAYPAL_CLIENT_ID}:${env.PAYPAL_SECRET}`);
  const r = await fetch(`${PAYPAL_API}/v1/oauth2/token`, {
    method: "POST",
    headers: { Authorization: `Basic ${basic}`, "Content-Type": "application/x-www-form-urlencoded" },
    body: "grant_type=client_credentials"
  });
  if (!r.ok) throw new Error("paypal auth failed");
  return (await r.json()).access_token;
}

function corsHeaders(request, env) {
  const origin = request.headers.get("Origin") || "";
  const allowed = (env.ALLOWED_ORIGIN || "https://chinavisit.org").split(",").map(s => s.trim());
  return {
    "Access-Control-Allow-Origin": allowed.includes(origin) ? origin : allowed[0],
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Cache-Control": "no-store"
  };
}

function json(body, headers, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { ...headers, "Content-Type": "application/json" } });
}
