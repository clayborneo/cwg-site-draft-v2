/**
 * Caring with Grace — contact form backend.
 * Cloudflare Worker owned by CWG; forwards submissions to email via Postmark.
 * (Postmark chosen over Resend: its DNS verification works with Wix DNS.)
 *
 * Secrets (set with `wrangler secret put NAME`):
 *   POSTMARK_SERVER_TOKEN - Server API token from postmarkapp.com
 *   TURNSTILE_SECRET      - (optional) Cloudflare Turnstile secret for spam
 * Vars (wrangler.toml):
 *   TO_EMAIL         - where submissions go
 *   FROM_EMAIL       - a Postmark-verified sender signature
 *   ALLOWED_ORIGINS  - comma-separated origins allowed to POST
 */

const FIELD_LIMIT = 4000;

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const allowed = (env.ALLOWED_ORIGINS || "").split(",").map(s => s.trim());
    const corsOrigin = allowed.includes(origin) ? origin : allowed[0] || "*";
    const cors = {
      "Access-Control-Allow-Origin": corsOrigin,
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") return new Response(null, { headers: cors });
    if (request.method !== "POST") return json({ ok: false, error: "POST only" }, 405, cors);

    let data;
    try { data = await request.json(); } catch { return json({ ok: false, error: "Bad JSON" }, 400, cors); }

    // Honeypot: real users never fill this
    if (data.website) return json({ ok: true }, 200, cors);

    const name = clean(data.name), email = clean(data.email);
    const message = clean(data.message);
    if (!name || !email || !message) return json({ ok: false, error: "Missing required fields" }, 400, cors);
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return json({ ok: false, error: "Invalid email" }, 400, cors);

    // Optional Turnstile verification
    if (env.TURNSTILE_SECRET) {
      const ok = await verifyTurnstile(env.TURNSTILE_SECRET, data.turnstileToken, request);
      if (!ok) return json({ ok: false, error: "Verification failed" }, 403, cors);
    }

    const lines = [
      `Name: ${name}`,
      `Email: ${email}`,
      data.phone ? `Phone: ${clean(data.phone)}` : null,
      data.topic ? `Topic: ${clean(data.topic)}` : null,
      data.referral ? `Heard about us: ${clean(data.referral)}` : null,
      data.page ? `Submitted from: ${clean(data.page)}` : null,
      "",
      "Message:",
      message,
    ].filter(l => l !== null);

    const resp = await fetch("https://api.postmarkapp.com/email", {
      method: "POST",
      headers: {
        "X-Postmark-Server-Token": env.POSTMARK_SERVER_TOKEN,
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        From: `CWG Website <${env.FROM_EMAIL}>`,
        To: env.TO_EMAIL,
        ReplyTo: email,
        Subject: `Website inquiry from ${name}`,
        TextBody: lines.join("\n"),
        MessageStream: "outbound",
      }),
    });

    if (!resp.ok) {
      console.error("Postmark error", resp.status, await resp.text());
      return json({ ok: false, error: "Delivery failed" }, 502, cors);
    }
    return json({ ok: true }, 200, cors);
  },
};

function clean(v) { return typeof v === "string" ? v.trim().slice(0, FIELD_LIMIT) : ""; }
function json(obj, status, headers) {
  return new Response(JSON.stringify(obj), { status, headers: { "Content-Type": "application/json", ...headers } });
}
async function verifyTurnstile(secret, token, request) {
  if (!token) return false;
  const resp = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ secret, response: token, remoteip: request.headers.get("CF-Connecting-IP") }),
  });
  const out = await resp.json();
  return !!out.success;
}
