# CWG contact form backend

A Cloudflare Worker owned by Caring with Grace. Receives form POSTs from the
website and emails them to info@caringwithgrace.com via Postmark. No third-party form service.
(Postmark, not Resend: Resend requires a subdomain MX record that Wix DNS
cannot create. Postmark's records are Wix-compatible.)

## One-time setup (about 15 minutes)

1. Create a free Cloudflare account (cloudflare.com) if CWG doesn't have one.
2. Create a free Postmark account (postmarkapp.com) and verify the
   caringwithgrace.com DOMAIN (DKIM TXT + custom Return-Path CNAME; both
   work in Wix's DNS manager). A sender signature alone is not enough: the
   mail says it is from the same domain it is delivered to, so it needs
   aligned DKIM to pass DMARC. Then copy the Server API token
   (Servers -> API Tokens).
3. Create a free Cloudflare Turnstile widget (hostnames: the draft host and
   the production hosts). Put its site key in TURNSTILE_SITE_KEY at the top
   of assets/js/main.js.
4. From this folder:

       npm install -g wrangler
       wrangler login
       wrangler secret put POSTMARK_SERVER_TOKEN   # paste the token
       wrangler secret put TURNSTILE_SECRET        # from the widget
       wrangler deploy

5. Wrangler prints the Worker URL, e.g.
   https://cwg-contact-form.<account>.workers.dev
   Paste that URL into CONTACT_FORM_ENDPOINT at the top of
   assets/js/main.js and push.

Until the endpoint is set, the site forms fall back to opening the
visitor's email app with a pre-filled message (works, just less smooth).

## Optional hardening

- Turnstile is required, not optional: with REQUIRE_TURNSTILE = "true" (the
  default in wrangler.toml) the Worker refuses to send if the secret is
  missing. Set it to "false" only for a first delivery test.
- The Worker only accepts POSTs from the origins in ALLOWED_ORIGINS. Update
  that list when the repo moves or the site launches.

## Privacy note

The form intentionally asks visitors not to include medical details;
specifics are gathered by phone during intake. Submissions are delivered to
the info@ inbox. Postmark also keeps message content in its activity log
(45 days by default, 7 days minimum) and does not sign HIPAA BAAs, so the
form must stay a simple contact request.
