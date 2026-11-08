/* 主题：默认跟随系统，手动切换后记住选择。必须在 head 里同步执行，避免闪白。 */
(function () {
  var KEY = 'cpnc-theme';
  var root = document.documentElement;

  function systemTheme() {
    try {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    } catch (e) { return 'light'; }
  }

  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  root.setAttribute('data-theme', saved || systemTheme());

  function paint(btn) {
    var dark = root.getAttribute('data-theme') === 'dark';
    var label = dark ? '切换到日间模式' : '切换到夜间模式';
    btn.setAttribute('aria-pressed', dark ? 'true' : 'false');
    btn.setAttribute('aria-label', label);
    btn.setAttribute('title', label);
  }

  function mount() {
    var btn = document.querySelector('.theme-toggle');
    if (!btn) return;
    paint(btn);
    btn.addEventListener('click', function () {
      root.setAttribute('data-theme',
        root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
      try { localStorage.setItem(KEY, root.getAttribute('data-theme')); } catch (e) {}
      paint(btn);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
