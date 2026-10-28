/* 进站动效：一次"上电"，然后像机库门一样抬起。 */
(() => {
  const html = document.documentElement;
  const 锁 = html.classList.contains('lm-lock');
  if (!html.classList.contains('lm-boot') && !锁) return;
  const 幕 = document.querySelector(锁 ? '.lm-lock-overlay' : '.lm-boot-overlay');
  if (!幕) { html.classList.remove('lm-boot', 'lm-lock'); return; }

  const 参 = new URLSearchParams(location.search);
  if (参.get('static') !== null) {
    html.classList.add('lm-static');
    return;                       // 静态样张：停在"READY"那一帧
  }
  const 冻结 = 参.get('freeze');
  if (冻结 !== null) {
    const t = Math.max(0, parseFloat(冻结) || 0) * 1000;
    requestAnimationFrame(() => {
      document.getAnimations().forEach(a => { try { a.currentTime = t; a.pause(); } catch (e) {} });
    });
    return;                       // 冻结模式不自动收尾，方便截图
  }

  let 收过 = false;
  const 收 = () => {
    if (收过) return;
    收过 = true;
    html.classList.remove('lm-boot', 'lm-lock');
    try { sessionStorage.setItem('lm_seen', '1'); } catch (e) {}
  };
  幕.addEventListener('animationend', e => {
    if (e.animationName === 'lm-boot-out' || e.animationName === 'lm-lock-out') 收();
  });

  const 跳 = () => {
    if (收过) return;
    幕.style.animation = (锁 ? 'lm-lock-out' : 'lm-boot-out') + ' .26s cubic-bezier(.4,0,.2,1) forwards';
    setTimeout(收, 280);
  };
  addEventListener('click', 跳, { once: true });
  addEventListener('keydown', 跳, { once: true });
  addEventListener('wheel', 跳, { once: true, passive: true });
  setTimeout(收, 2800);           // 兜底：动画事件丢了也不能卡住
})();
