document.addEventListener('DOMContentLoaded', () => {
  const backBtn = document.createElement('button');
  backBtn.className = 'back-to-top';
  backBtn.setAttribute('aria-label', 'Back to top');
  backBtn.innerHTML = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>';
  document.body.appendChild(backBtn);
  backBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  window.addEventListener('scroll', () => {
    backBtn.classList.toggle('visible', window.scrollY > 600);
  }, { passive: true });


  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => nav.classList.toggle('open'));
  }

  const path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.site-nav a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === path || (path === 'index.html' && href === 'index.html')) {
      a.classList.add('active');
      const drop = a.closest('.has-dropdown');
      if (drop) drop.querySelector('.nav-drop-btn').classList.add('active');
    }
  });

  // Our Services dropdown: click toggles (touch devices), hover handled in CSS
  document.querySelectorAll('.has-dropdown .nav-drop-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      btn.parentElement.classList.toggle('open');
    });
  });
  document.addEventListener('click', () => {
    document.querySelectorAll('.has-dropdown.open').forEach(li => li.classList.remove('open'));
  });

  const carousel = document.getElementById('hero-carousel');
  if (carousel) {
    const slides = carousel.querySelectorAll('.carousel-slide');
    const dots = carousel.querySelectorAll('.carousel-dot');
    const prevBtn = carousel.querySelector('.carousel-prev');
    const nextBtn = carousel.querySelector('.carousel-next');
    const progressBar = document.getElementById('carousel-progress-bar');
    let current = 0;
    let timer = null;
    let progressTimer = null;
    const INTERVAL = 7000;

    function go(index) {
      slides[current].classList.remove('active');
      dots[current].classList.remove('active');
      current = (index + slides.length) % slides.length;
      slides[current].classList.add('active');
      dots[current].classList.add('active');
      resetProgress();
    }
    function resetProgress() {
      if (!progressBar) return;
      progressBar.style.transition = 'none';
      progressBar.style.width = '0%';
      void progressBar.offsetWidth;
      progressBar.style.transition = `width ${INTERVAL}ms linear`;
      progressBar.style.width = '100%';
    }
    function startAuto() {
      stopAuto();
      timer = setInterval(() => go(current + 1), INTERVAL);
      resetProgress();
    }
    function stopAuto() {
      if (timer) clearInterval(timer);
      timer = null;
    }
    dots.forEach((d, i) => d.addEventListener('click', () => { go(i); startAuto(); }));
    if (prevBtn) prevBtn.addEventListener('click', () => { go(current - 1); startAuto(); });
    if (nextBtn) nextBtn.addEventListener('click', () => { go(current + 1); startAuto(); });
    carousel.addEventListener('mouseenter', stopAuto);
    carousel.addEventListener('mouseleave', startAuto);

    // Keyboard
    document.addEventListener('keydown', (e) => {
      if (document.activeElement && carousel.contains(document.activeElement)) {
        if (e.key === 'ArrowLeft')  { go(current - 1); startAuto(); }
        if (e.key === 'ArrowRight') { go(current + 1); startAuto(); }
      }
    });

    startAuto();
  }

  const modal = document.getElementById('bio-modal');
  if (modal) {
    const photo = modal.querySelector('.bio-modal-photo');
    const name = modal.querySelector('.bio-modal-name');
    const title = modal.querySelector('.bio-modal-title');
    const creds = modal.querySelector('.bio-modal-creds');
    const body = modal.querySelector('.bio-modal-body');
    const closeBtn = modal.querySelector('.bio-modal-close');

    function openBio(card) {
      const bio = card.querySelector('.bio-text');
      if (!bio) return;
      name.textContent = card.dataset.name || '';
      title.textContent = card.dataset.title || '';
      creds.textContent = card.dataset.creds || '';
      const photoUrl = card.dataset.photo;
      if (photoUrl) {
        photo.style.backgroundImage = `url('${photoUrl}')`;
        photo.innerHTML = '';
      } else {
        photo.style.backgroundImage = '';
        photo.innerHTML = '<svg viewBox="0 0 24 24" width="40" height="40" fill="currentColor"><path d="M12 12c2.7 0 5-2.3 5-5s-2.3-5-5-5-5 2.3-5 5 2.3 5 5 5zm0 2c-3.3 0-10 1.7-10 5v3h20v-3c0-3.3-6.7-5-10-5z"/></svg>';
      }
      body.innerHTML = bio.innerHTML;
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
    function closeBio() {
      modal.classList.remove('open');
      document.body.style.overflow = '';
    }
    document.querySelectorAll('.team-card[data-name]').forEach(card => {
      card.addEventListener('click', () => openBio(card));
      card.style.cursor = 'pointer';
      const url = card.dataset.photo;
      const photoEl = card.querySelector('.team-photo');
      if (url && photoEl) {
        const img = new Image();
        img.onload = () => {
          photoEl.style.backgroundImage = `url('${url}')`;
          photoEl.classList.remove('placeholder');
          photoEl.innerHTML = '';
        };
        img.src = url;
      }
    });
    closeBtn.addEventListener('click', closeBio);
    modal.addEventListener('click', (e) => { if (e.target === modal) closeBio(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && modal.classList.contains('open')) closeBio(); });
  }
});


// ---------------------------------------------------------------------------
// Analytics (GA4). Paste the Measurement ID (G-XXXXXXXXXX) from
// analytics.google.com > Admin > Data streams to activate on all pages.
const GA_MEASUREMENT_ID = 'G-KQRYWP9436';

if (GA_MEASUREMENT_ID) {
  const gs = document.createElement('script');
  gs.async = true;
  gs.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_MEASUREMENT_ID;
  document.head.appendChild(gs);
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('config', GA_MEASUREMENT_ID);
}

// ---------------------------------------------------------------------------
// Contact form
// Set to the deployed Cloudflare Worker URL (see workers/contact-form/README).
// While empty, forms fall back to opening the visitor's email app.
const CONTACT_FORM_ENDPOINT = '';
const CONTACT_FALLBACK_EMAIL = 'melissa@caringwithgrace.com';

document.querySelectorAll('.contact-form').forEach((form) => {
  form.removeAttribute('onsubmit');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;

    const val = (sel) => { const el = form.querySelector(sel); return el ? el.value.trim() : ''; };
    const first = val('input[id$="-fn"]'), last = val('input[id$="-ln"]');
    const payload = {
      name: (first + ' ' + last).trim(),
      email: val('input[type="email"]'),
      phone: val('input[type="tel"]'),
      topic: val('select[id$="-topic"]'),
      referral: val('select[id$="-ref"]'),
      message: val('textarea'),
      website: val('input[name="website"]'),   // honeypot
      page: location.pathname,
    };

    const btn = form.querySelector('button[type="submit"]');

    if (!CONTACT_FORM_ENDPOINT) {
      const body = ['Name: ' + payload.name, 'Phone: ' + payload.phone,
        'Topic: ' + payload.topic, 'Heard about us: ' + payload.referral,
        '', payload.message].join('\n');
      location.href = 'mailto:' + CONTACT_FALLBACK_EMAIL +
        '?subject=' + encodeURIComponent('Website inquiry from ' + payload.name) +
        '&body=' + encodeURIComponent(body);
      return;
    }

    btn.disabled = true;
    const btnText = btn.textContent;
    btn.textContent = 'Sending…';
    try {
      const resp = await fetch(CONTACT_FORM_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const out = await resp.json();
      if (!out.ok) throw new Error(out.error || 'failed');
      form.innerHTML = '<div class="form-success"><h3>Thank you!</h3>' +
        '<p>Your message is on its way. We respond within one business day, ' +
        'often much sooner. If this is urgent, please call ' +
        '<a href="tel:+12147759969">(214) 775-9969</a>.</p></div>';
    } catch (err) {
      btn.disabled = false;
      btn.textContent = btnText;
      let errEl = form.querySelector('.form-error');
      if (!errEl) {
        errEl = document.createElement('p');
        errEl.className = 'form-error';
        btn.parentNode.insertBefore(errEl, btn);
      }
      errEl.textContent = 'Something went wrong sending your message. Please try again, or call us at (214) 775-9969.';
    }
  });
});
