# Off-Wix migration plan (ISS-009 / ISS-033)

Status: planned, not started. Revised 2026-09-21.

Wix does not allow nameserver changes on a domain registered with Wix, so the
earlier "move DNS to Cloudflare" phase is gone. The site launches by editing
two kinds of record inside Wix DNS (apex A, `www` CNAME). Email records are
never touched. The old Wix site stays published as a rollback target.

The one thing that must not break: Google Workspace MX records (company email).

## Phase 0 — Prep (zero risk)
- [ ] Screenshot / export every DNS record in Wix's DNS manager (MX and
      priorities, SPF TXT, `_dmarc` CNAME, verification TXTs, A, CNAME).
      This is the rollback sheet.
- [ ] CWG-owned accounts: GitHub organization, Cloudflare (Worker + Turnstile
      only, not DNS), Postmark. Two admins each.
- [ ] Transfer this repo into the organization and rename it.

## Phase 1 — Contact form (can ship on the draft site)
- [ ] Postmark: verify the caringwithgrace.com DOMAIN (DKIM TXT + custom
      Return-Path CNAME, both added in Wix DNS). Leave the apex SPF alone.
- [ ] Cloudflare Turnstile widget; hostnames = draft host + production hosts.
- [ ] From workers/contact-form/: `wrangler login`,
      `wrangler secret put POSTMARK_SERVER_TOKEN`,
      `wrangler secret put TURNSTILE_SECRET`, `wrangler deploy`.
      ALLOWED_ORIGINS must include the organization's github.io origin.
- [ ] Set CONTACT_FORM_ENDPOINT and TURNSTILE_SITE_KEY in assets/js/main.js,
      bump the `?v=` on main.js, push.
- [ ] Test with TO_EMAIL pointed at the implementer. In Gmail "Show original":
      DKIM, SPF and DMARC all PASS; Reply-To is the visitor.
- [ ] Flip TO_EMAIL to the intake inbox; confirm inbox delivery with no filter.

## Phase 2 — Site cutover (needs team go-ahead; the public launch)
- [ ] Repo launch checklist:
      - remove draft banner from all pages
      - delete `noindex` metas; set robots.txt to Allow
      - canonicals, og:url, sitemap.xml, and the JSON-LD `url` on index.html
        -> https://www.caringwithgrace.com/
      - delete brand-review.html, brand-home.html, assets/js/palette.js
      - add redirect stubs for old Wix paths (about-us, caringoncall, blog,
        and the old resources sub-pages)
      - retire the 20-years banner if past 2026
- [ ] GitHub Pages settings: custom domain `www.caringwithgrace.com`.
- [ ] Wix DNS: `www` CNAME -> `<organization>.github.io`; apex A ->
      185.199.108.153 / .109.153 / .110.153 / .111.153 (replacing Wix's).
      Change nothing else.
- [ ] Wait for GitHub's certificate (minutes, up to an hour), then tick
      Enforce HTTPS. GitHub handles apex -> www.
- [ ] Verify: every page on both hostnames, a real 404, the form from the
      production origin, GA Realtime, external email in and out.
- Rollback: restore the Wix A records and `www` CNAME from the Phase 0 sheet.

## Phase 3 — After launch
- [ ] Search Console: verify domain, submit sitemap.
- [ ] Worker ALLOWED_ORIGINS and Turnstile hostnames: drop the draft origin.
- [ ] Wix: turn off auto-renew on the SITE plan only. The domain subscription
      is the registration and stays.

## Not planned: leaving Wix DNS
Requires transferring the registration to another registrar (locked for 60 days
after the September 2026 registrar move) and re-creating every record there
first. Only worth doing if something forces it.
