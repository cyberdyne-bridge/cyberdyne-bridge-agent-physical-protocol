/* LM 风的动效：少、慢、克制。 */
(() => {
  const 减动 = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const 头 = document.querySelector('.site-header');
  const 滚动 = () => 头 && 头.classList.toggle('lm-scrolled', scrollY > 8);
  滚动(); addEventListener('scroll', 滚动, { passive: true });

  // 顶部 1px 滚动进度（蓝）
  const 条 = document.createElement('div');
  条.className = 'lm-progress';
  document.body.appendChild(条);
  const 画条 = () => {
    const 高 = document.documentElement.scrollHeight - innerHeight;
    条.style.transform = `scaleX(${高 > 0 ? Math.min(1, scrollY / 高) : 0})`;
  };
  画条(); addEventListener('scroll', 画条, { passive: true });
  addEventListener('resize', 画条);

  const 选 = '.section-head, .kicker, .card, .principles li, .arch-image, .status-grid, .cta h2, .cta-actions';
  const 元素 = [...document.querySelectorAll(选)];
  元素.forEach(el => {
    el.classList.add('lm-reveal');
    const 同组 = [...el.parentElement.children].filter(x => x.classList.contains('lm-reveal'));
    const i = Math.max(0, 同组.indexOf(el));
    el.style.setProperty('--d', Math.min(i, 4) * 70 + 'ms');
  });
  if (减动 || !('IntersectionObserver' in window)) {
    元素.forEach(el => el.classList.add('in'));
    return;
  }
  const 扫 = document.querySelector('.arch-frame');
  if (扫) {
    const sio = new IntersectionObserver(es => {
      es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('scan'); sio.unobserve(e.target); } });
    }, { threshold: 0.25 });
    sio.observe(扫);
  }

  const io = new IntersectionObserver(es => {
    es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
  元素.forEach(el => io.observe(el));
  window.LM_MOTION = { count: 元素.length };
})();
