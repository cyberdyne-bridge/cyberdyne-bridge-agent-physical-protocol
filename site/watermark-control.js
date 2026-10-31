(() => {
  const KEY = 'cpnc_wm_opacity';
  const panel = document.getElementById('wm-panel');
  const range = document.getElementById('wm-range');
  const out = document.getElementById('wm-value');
  if (!panel || !range || !out) return;

  const apply = (value) => {
    const v = Math.max(0, Math.min(20, Number(value) || 0));
    document.documentElement.style.setProperty('--wm-opacity', (v / 100).toFixed(2));
    out.textContent = v + '%';
  };

  const saved = localStorage.getItem(KEY);
  const initial = saved === null ? 12 : Number(saved);
  range.value = String(initial);
  apply(initial);

  if (new URLSearchParams(location.search).has('wm')) panel.hidden = false;

  range.addEventListener('input', () => {
    const v = Number(range.value);
    apply(v);
    try { localStorage.setItem(KEY, String(v)); } catch (e) {}
  });

  document.getElementById('wm-close').addEventListener('click', () => {
    panel.hidden = true;
  });
})();
