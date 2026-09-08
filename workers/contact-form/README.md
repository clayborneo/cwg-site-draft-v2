# CWG contact form backend

A Cloudflare Worker owned by Caring with Grace. Receives form POSTs from the
website and emails them to Melissa via Postmark. No third-party form service.
(Postmark, not Resend: Resend requires a subdomain MX record that Wix DNS
cannot create. Postmark's records are Wix-compatible.)

## One-time setup (about 15 minutes)

1. Create a free Cloudflare account (cloudflare.com) if CWG doesn't have one.
2. Create a free Postmark account (postmarkapp.com). Two verification options:
   - Quickest, zero DNS: Sender Signatures -> add the FROM address (see
     wrangler.toml) or melissa@caringwithgrace.com; click the confirmation
     link Postmark emails to that inbox.
   - Better deliverability: also verify the caringwithgrace.com domain
     (DKIM TXT + Return-Path CNAME; both work in Wix's DNS manager).
   Then copy the Server API token (Servers -> API Tokens).
3. From this folder:

       npm install -g wrangler
       wrangler login
       wrangler secret put POSTMARK_SERVER_TOKEN   # paste the token
       wrangler deploy

4. Wrangler prints the Worker URL, e.g.
   https://cwg-contact-form.<account>.workers.dev
   Paste that URL into CONTACT_FORM_ENDPOINT at the top of
   assets/js/main.js and push.

Until the endpoint is set, the site forms fall back to opening the
visitor's email app with a pre-filled message (works, just less smooth).

## Optional hardening

- Spam: create a (free) Cloudflare Turnstile widget, add its site key to the
  form pages, and `wrangler secret put TURNSTILE_SECRET`. The Worker starts
  verifying automatically once the secret exists.
- Custom URL: once the domain moves to Cloudflare DNS, route the Worker at
  forms.caringwithgrace.com instead of workers.dev.

## Privacy note

The form intentionally asks visitors not to include medical details;
specifics are gathered by phone during intake. Submissions are not stored
anywhere except the delivery email to Melissa's inbox.
