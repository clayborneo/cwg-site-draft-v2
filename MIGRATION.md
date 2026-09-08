# Off-Wix migration plan (ISS-009 / ISS-033)

Status: planned, not started. Wix subscription paid through 2026, so there
is no deadline pressure; the old site remains a rollback target throughout.

## Phase 0 — Prep (~30 min, zero risk)
- [ ] Screenshot / export every DNS record in Wix's DNS manager.
      Critical: Google Workspace MX records (company email), SPF TXT,
      site-verification TXTs, A/CNAME records pointing at Wix.
- [ ] Create CWG Cloudflare account (business-owned email).
- [ ] Cloudflare "Add site" -> caringwithgrace.com -> verify its imported
      records against the screenshots; add anything missed.
- Nothing changes publicly in this phase.

## Phase 1 — Move DNS to Cloudflare (~15 min + propagation)
- [ ] In Wix domain settings, set nameservers to the two Cloudflare NS.
- [ ] Wait for propagation (minutes-hours). Site stays on Wix, email
      unaffected, because the records are identical.
- Rollback: restore Wix nameservers.
- After this phase the contact-form email setup (Phase 3) is unblocked.

## Phase 2 — Site cutover (~1 hour; needs team go-ahead; the public launch)
- [ ] Repo launch checklist:
      - remove draft banner from all pages
      - delete `noindex` metas; set robots.txt to Allow
      - canonicals + sitemap.xml -> https://www.caringwithgrace.com/
      - add CNAME file (www.caringwithgrace.com) + set custom domain in
        GitHub Pages settings; enforce HTTPS
      - retire the 20-years banner if past 2026
- [ ] Cloudflare: point apex + www from Wix to GitHub Pages
      (A 185.199.108.153 / .109. / .110. / .111.; CNAME www -> clayborneo.github.io).
- [ ] Apex->www redirect rule; verify every page, GA Realtime, favicon.
- Rollback: repoint the two records at Wix.

## Phase 3 — Contact form + hardening (~45 min; needs only Phase 1)
- [ ] Postmark account; verify caringwithgrace.com domain (DKIM TXT +
      Return-Path CNAME, 2 min in Cloudflare DNS).
- [ ] `wrangler login` / `wrangler secret put POSTMARK_SERVER_TOKEN` /
      `wrangler deploy` from workers/contact-form/.
- [ ] Paste Worker URL into CONTACT_FORM_ENDPOINT in assets/js/main.js.
- [ ] Test end-to-end with TO_EMAIL pointed at Clay, then flip to Melissa.
- [ ] Optional: Turnstile spam protection; forms.caringwithgrace.com route.

Total: ~2-3 hours of hands-on work across a few days. The one thing that
must not break: Google Workspace MX records (company email).
