/**
 * Caring with Grace — contact form backend.
 * Cloudflare Worker owned by CWG; forwards submissions to email via Postmark.
 * (Postmark chosen over Resend: its DNS verification works with Wix DNS.)
 *
 * Secrets (set with `wrangler secret put NAME`):
 *   POSTMARK_SERVER_TOKEN - Server API token from postmarkapp.com
 *   TURNSTILE_SECRET      - Cloudflare Turnstile secret (spam protection)
 * Vars (wrangler.toml):
 *   TO_EMAIL          - where submissions go
 *   FROM_EMAIL        - an address on the Postmark-verified domain
 *   ALLOWED_ORIGINS   - comma-separated origins allowed to POST
 *   REQUIRE_TURNSTILE - "true" in production: refuse to send if the Turnstile
 *                       secret is missing, instead of silently running open
 */

const MAX_BODY_BYTES = 16 * 1024;
const LIMITS = { name: 200, email: 254, phone: 40, topic: 120, referral: 120, page: 200, message: 4000 };
const UPSTREAM_TIMEOUT_MS = 8000;

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const allowed = (env.ALLOWED_ORIGINS || "").split(",").map(s => s.trim()).filter(Boolean);
    const originOk = allowed.includes(origin);
    const cors = {
      "Access-Control-Allow-Origin": originOk ? origin : allowed[0] || "null",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      Vary: "Origin",
    };

    if (request.method === "OPTIONS") return new Response(null, { headers: cors });
    if (request.method !== "POST") return json({ ok: false, error: "POST only" }, 405, cors);
    // CORS headers only stop a browser reading the reply; this stops the send.
    if (!originOk) return json({ ok: false, error: "Origin not allowed" }, 403, cors);
    if (!(request.headers.get("Content-Type") || "").toLowerCase().startsWith("application/json")) {
      return json({ ok: false, error: "JSON only" }, 415, cors);
    }

    let raw;
    try { raw = await request.text(); } catch { return json({ ok: false, error: "Bad request" }, 400, cors); }
    if (new TextEncoder().encode(raw).length > MAX_BODY_BYTES) return json({ ok: false, error: "Too large" }, 413, cors);

    let data;
    try { data = JSON.parse(raw); } catch { return json({ ok: false, error: "Bad JSON" }, 400, cors); }
    if (!data || typeof data !== "object" || Array.isArray(data)) return json({ ok: false, error: "Bad JSON" }, 400, cors);

    // Honeypot: real users never fill this
    if (data.website) return json({ ok: true }, 200, cors);

    const f = {};
    for (const [key, max] of Object.entries(LIMITS)) {
      const v = typeof data[key] === "string" ? data[key].trim() : "";
      if (v.length > max) return json({ ok: false, error: `${key} is too long` }, 400, cors);
      f[key] = v;
    }
    if (!f.name || !f.email || !f.message) return json({ ok: false, error: "Missing required fields" }, 400, cors);
    if (!/^[^@\s,;<>"]+@[^@\s,;<>"]+\.[^@\s,;<>"]+$/.test(f.email)) return json({ ok: false, error: "Invalid email" }, 400, cors);
    // name and email end up in mail headers (Subject, Reply-To)
    if (/[\u0000-\u001f\u007f]/.test(f.name + f.email + f.phone)) return json({ ok: false, error: "Invalid characters" }, 400, cors);

    if (env.TURNSTILE_SECRET) {
      const hosts = allowed.map(o => { try { return new URL(o).hostname; } catch { return ""; } });
      const ok = await verifyTurnstile(env.TURNSTILE_SECRET, data.turnstileToken, request, hosts);
      if (!ok) return json({ ok: false, error: "Verification failed" }, 403, cors);
    } else if (String(env.REQUIRE_TURNSTILE).toLowerCase() === "true") {
      console.error("REQUIRE_TURNSTILE is on but TURNSTILE_SECRET is not set");
      return json({ ok: false, error: "Form is not configured" }, 503, cors);
    }

    const lines = [
      `Name: ${f.name}`,
      `Email: ${f.email}`,
      f.phone ? `Phone: ${f.phone}` : null,
      f.topic ? `Topic: ${f.topic}` : null,
      f.referral ? `Heard about us: ${f.referral}` : null,
      f.page ? `Submitted from: ${f.page}` : null,
      "",
      "Message:",
      f.message,
    ].filter(l => l !== null);

    let resp;
    try {
      resp = await fetch("https://api.postmarkapp.com/email", {
        method: "POST",
        headers: {
          "X-Postmark-Server-Token": env.POSTMARK_SERVER_TOKEN,
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          From: `CWG Website <${env.FROM_EMAIL}>`,
          To: env.TO_EMAIL,
          ReplyTo: f.email,
          Subject: `Website inquiry from ${f.name}`,
          TextBody: lines.join("\n"),
          MessageStream: "outbound",
        }),
        signal: AbortSignal.timeout(UPSTREAM_TIMEOUT_MS),
      });
    } catch (err) {
      console.error("Postmark unreachable", err && err.name);
      return json({ ok: false, error: "Delivery failed" }, 502, cors);
    }

    // Log the provider's status and code only, never the visitor's message.
    const out = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      console.error("Postmark error", resp.status, out.ErrorCode);
      return json({ ok: false, error: "Delivery failed" }, 502, cors);
    }
    console.log("Postmark accepted", out.MessageID);
    return json({ ok: true }, 200, cors);
  },
};

function json(obj, status, headers) {
  return new Response(JSON.stringify(obj), { status, headers: { "Content-Type": "application/json", ...headers } });
}
async function verifyTurnstile(secret, token, request, hosts) {
  if (!token || typeof token !== "string" || token.length > 2048) return false;
  try {
    const resp = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ secret, response: token, remoteip: request.headers.get("CF-Connecting-IP") }),
      signal: AbortSignal.timeout(UPSTREAM_TIMEOUT_MS),
    });
    const out = await resp.json();
    return !!out.success && hosts.includes(out.hostname);
  } catch {
    return false;
  }
}
