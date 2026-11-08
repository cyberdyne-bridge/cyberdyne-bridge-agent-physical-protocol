/* 首帧前执行：语言方向 + 入场动画类。
   内联版本已抽到外部文件，以便使用不含 unsafe-inline 的 CSP。 */
(function () {
  try {
    var q = new URLSearchParams(location.search).get('lang');
    if (q === 'ar') {
      document.documentElement.dir = 'rtl';
      document.documentElement.lang = 'ar';
    }
    if (!sessionStorage.getItem('lm_seen') &&
        !matchMedia('(prefers-reduced-motion: reduce)').matches) {
      var m = new URLSearchParams(location.search).get('enter') === 'b' ? 'lm-lock' : 'lm-boot';
      document.documentElement.classList.add(m);
    }
  } catch (e) {}
})();
