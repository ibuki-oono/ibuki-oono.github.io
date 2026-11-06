(() => {
  'use strict';

  // External article photos degrade gracefully if the source is unavailable.
  document.querySelectorAll('.project-image img').forEach(img => {
    const fallback = () => {
      img.hidden = true;
      img.parentElement.classList.add('image-unavailable');
    };
    img.addEventListener('error', fallback, { once: true });
    if (img.complete && img.naturalWidth === 0) fallback();
  });

  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  const reveals = document.querySelectorAll('.reveal');
  const progress = document.querySelector('.scroll-progress');
  const photo = document.querySelector('[data-parallax]');
  const photoImage = photo?.querySelector('img');
  let observer;
  let framePending = false;

  function updateScroll() {
    const height = document.documentElement.scrollHeight - window.innerHeight;
    const fraction = height > 0 ? window.scrollY / height : 0;
    if (progress) progress.style.transform = `scaleX(${Math.max(0, Math.min(1, fraction))})`;
    if (photoImage) {
      if (preference.matches) {
        photoImage.style.removeProperty('transform');
      } else {
        const bounds = photo.getBoundingClientRect();
        if (bounds.bottom > 0 && bounds.top < window.innerHeight) {
          const offset = (window.innerHeight / 2 - bounds.top - bounds.height / 2) * 0.05;
          const travel = Math.min(12, bounds.height * 0.015);
          photoImage.style.transform = `translate3d(0, ${Math.max(-travel, Math.min(travel, offset))}px, 0) scale(1.02)`;
        }
      }
    }
    framePending = false;
  }

  function requestUpdate() {
    if (!framePending) {
      framePending = true;
      window.requestAnimationFrame(updateScroll);
    }
  }

  function configureMotion() {
    observer?.disconnect();
    document.documentElement.classList.toggle('motion-enabled', !preference.matches);
    if (preference.matches || !('IntersectionObserver' in window)) {
      reveals.forEach(element => element.classList.add('is-visible'));
    } else {
      observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.08 });
      reveals.forEach(element => observer.observe(element));
    }
    updateScroll();
  }

  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate, { passive: true });
  window.addEventListener('pageshow', requestUpdate);
  preference.addEventListener('change', configureMotion);
  configureMotion();
})();
