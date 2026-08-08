// Lightweight interactions: mobile nav, scroll reveal, footer year, contact form handling,
// plus enhanced "send message" celebration: confetti, button morph, hero pulse, overlay.
document.addEventListener('DOMContentLoaded', function () {
  // Nav toggle for mobile
  const navToggle = document.getElementById('nav-toggle');
  const nav = document.getElementById('nav');
  if (navToggle && nav) {
    navToggle.addEventListener('click', () => {
      nav.style.display = nav.style.display === 'flex' ? 'none' : 'flex';
    });
  }

  // Footer year
  const yearEl = document.getElementById('footer-year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // IntersectionObserver for reveal animations
  const revealEls = document.querySelectorAll('.reveal-up');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible');
          io.unobserve(e.target);
        }
      });
    }, {threshold: 0.15});
    revealEls.forEach(el => io.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('is-visible'));
  }

  // Floating subtle animation: small random delay
  document.querySelectorAll('.floating').forEach((el, i) => {
    el.style.animationDelay = (i * 0.3) + 's';
  });

  // --- Confetti setup ---
  const confettiCanvas = document.getElementById('confetti-canvas');
  const confettiCtx = confettiCanvas && confettiCanvas.getContext ? confettiCanvas.getContext('2d') : null;
  let confettiParticles = [];
  let confettiAnimating = false;

  function resizeCanvas() {
    if (!confettiCanvas) return;
    confettiCanvas.width = window.innerWidth;
    confettiCanvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resizeCanvas);
  resizeCanvas();

  function random(min, max) { return Math.random() * (max - min) + min; }
  function createConfettiBurst(x, y, count = 40) {
    const colors = ['#6EE7B7', '#7C5CFF', '#FFD166', '#FF6B6B', '#FF9F1C'];
    for (let i = 0; i < count; i++) {
      confettiParticles.push({
        x: x + random(-20, 20),
        y: y + random(-20, 20),
        vx: random(-6, 6),
        vy: random(-10, -2),
        size: random(6, 12),
        rot: random(0, Math.PI*2),
        vr: random(-0.15, 0.15),
        color: colors[Math.floor(Math.random() * colors.length)],
        life: 0,
        ttl: random(60, 120)
      });
    }
  }

  function stepConfetti() {
    if (!confettiCtx) return;
    confettiCtx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
    for (let i = confettiParticles.length - 1; i >= 0; i--) {
      const p = confettiParticles[i];
      p.vy += 0.25; // gravity
      p.vx *= 0.995; p.vy *= 0.998;
      p.x += p.vx;
      p.y += p.vy;
      p.rot += p.vr;
      p.life++;
      // draw rectangle rotated
      confettiCtx.save();
      confettiCtx.translate(p.x, p.y);
      confettiCtx.rotate(p.rot);
      confettiCtx.fillStyle = p.color;
      confettiCtx.fillRect(-p.size/2, -p.size/2, p.size, p.size * 0.6);
      confettiCtx.restore();
      if (p.life > p.ttl || p.y > confettiCanvas.height + 50) {
        confettiParticles.splice(i, 1);
      }
    }
    if (confettiParticles.length === 0) {
      confettiAnimating = false;
      confettiCanvas.style.opacity = 0;
    } else {
      requestAnimationFrame(stepConfetti);
    }
  }

  function launchConfetti() {
    if (!confettiCanvas) return;
    confettiCanvas.style.opacity = 1;
    const w = confettiCanvas.width;
    const h = confettiCanvas.height;
    // multiple bursts across top area for fuller effect
    createConfettiBurst(w * 0.3, h * 0.2, 30);
    createConfettiBurst(w * 0.5, h * 0.18, 40);
    createConfettiBurst(w * 0.7, h * 0.22, 30);
    if (!confettiAnimating) {
      confettiAnimating = true;
      requestAnimationFrame(stepConfetti);
    }
  }

  // --- Success animations: button morph, hero pulse, overlay ---
  const form = document.getElementById('contact-form');
  const status = document.getElementById('form-status');
  const submitBtn = document.getElementById('submit-btn');
  const hero = document.getElementById('hero');
  const successOverlay = document.getElementById('success-overlay');
  const successClose = document.getElementById('success-close');

  function setButtonSending() {
    submitBtn.classList.add('sending');
    submitBtn.disabled = true;
  }
  function setButtonSuccess() {
    submitBtn.classList.remove('sending');
    submitBtn.classList.add('success');
    submitBtn.disabled = false;
    // revert button after a while
    setTimeout(() => {
      submitBtn.classList.remove('success');
    }, 2200);
  }

  function showSuccessOverlay() {
    if (!successOverlay) return;
    successOverlay.classList.add('show');
    successOverlay.setAttribute('aria-hidden', 'false');
    // close on button
    successClose?.addEventListener('click', () => {
      successOverlay.classList.remove('show');
      successOverlay.setAttribute('aria-hidden', 'true');
    }, { once: true });
  }

  function heroPulse() {
    if (!hero) return;
    hero.classList.remove('pulse');
    // reflow then add
    void hero.offsetWidth;
    hero.classList.add('pulse');
    setTimeout(() => hero.classList.remove('pulse'), 900);
  }

  // Contact form handling (Formspree-friendly)
  if (form) {
    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      status.textContent = 'Sending...';
      setButtonSending();
      const action = form.getAttribute('action');
      if (!action || action.includes('YOUR_FORM_ID')) {
        status.textContent = 'Please configure your Formspree endpoint in index.html';
        submitBtn.classList.remove('sending');
        submitBtn.disabled = false;
        return;
      }
      const formData = new FormData(form);
      try {
        const res = await fetch(action, {
          method: 'POST',
          body: formData,
          headers: {'Accept': 'application/json'}
        });
        const json = await res.json();
        if (res.ok) {
          // success celebration
          status.textContent = 'Sent — thank you!';
          setButtonSuccess();
          heroPulse();
          // spawn sparkle elements briefly
          spawnSparkles();
          launchConfetti();
          showSuccessOverlay();
          form.reset();
        } else {
          status.textContent = json.error || 'Failed to send — please email directly.';
          submitBtn.classList.remove('sending');
          submitBtn.disabled = false;
        }
      } catch (err) {
        status.textContent = 'Network error: could not send message.';
        submitBtn.classList.remove('sending');
        submitBtn.disabled = false;
      }
    });
  }

  // small sparkle particles near hero for extra visual effect
  function spawnSparkles() {
    const heroEl = document.querySelector('.hero-inner');
    if (!heroEl) return;
    const count = 10;
    for (let i = 0; i < count; i++) {
      const s = document.createElement('div');
      s.className = 'sparkle';
      s.style.left = (random(10, 80)) + '%';
      s.style.top = (random(10, 70)) + '%';
      document.body.appendChild(s);
      // show and remove
      requestAnimationFrame(() => s.classList.add('show'));
      setTimeout(() => {
        s.classList.remove('show');
        setTimeout(() => s.remove(), 400);
      }, 700 + Math.random()*600);
    }
  }

  // Close overlay on ESC
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && successOverlay && successOverlay.classList.contains('show')) {
      successOverlay.classList.remove('show');
      successOverlay.setAttribute('aria-hidden', 'true');
    }
  });

  // safety: stop confetti on navigation or page hide
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && confettiParticles.length) {
      confettiParticles = [];
      if (confettiCtx) confettiCtx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
      confettiCanvas.style.opacity = 0;
    }
  });
});
