/* 五常语言：EN 默认，中文整页，FR/RU/ES 先翻译"框架"，正文暂留英文。 */
(() => {
  const 字典 = {
    ar: {
      "Overview": "نظرة عامة", "Architecture": "المعمارية", "Protocol": "البروتوكول",
      "Security": "الأمان", "MCP status": "حالة MCP", "Protocol map": "خريطة البروتوكول",
      "CBAP OS": "CBAP OS", "Agents": "الوكلاء",
      "AGENT ↔ PHYSICAL WORLD / CBAP v1": "الوكيل ↔ العالم المادي / CBAP v1",
      "UNOFFICIAL OPEN-SOURCE PROTOCOL": "بروتوكول مفتوح المصدر غير رسمي",
      "An open protocol bridge for physical agents": "جسر بروتوكول مفتوح للوكلاء الماديين",
      "A protocol where an agent acquires a device, executes an action, and verifies the result through server-authoritative facts. The main repository is CBAP; each agent adapter lives in its own subrepo.":
        "بروتوكول يحصل فيه الوكيل على جهاز، وينفّذ إجراءً، ويتحقق من النتيجة عبر حقائق موثوقة من الخادم. المستودع الرئيسي هو CBAP؛ وكل محوّل وكيل يعيش في مستودعه الفرعي.",
      "Open repository ↗": "فتح المستودع ↗", "Releases": "الإصدارات", "README": "README",
      "See architecture ↓": "عرض المعمارية ↓",
      "active agent subrepos": "مستودعات وكلاء نشطة", "source release": "إصدار المصدر",
      "CBAP conformance": "توافق CBAP", "control-plane p50 (local UDS)": "p50 لطائرة التحكم (UDS محلي)",
      "completion criterion": "معيار الإنجاز",
      "Not \"LLM directly driving Minecraft\".": "ليس «LLM يقود Minecraft مباشرة».",
      "Agents above. Facts below.": "الوكلاء في الأعلى. الحقائق في الأسفل.",
      "The protocol does not trust \"it said it worked\".": "البروتوكول لا يثق بـ«قال إنه نجح».",
      "Close the trust boundary before letting AI run.": "أغلق حدود الثقة قبل تشغيل الذكاء الاصطناعي.",
      "Upstream is not fixed. CBAP only mitigates locally.": "المنبع لم يُصلح. CBAP يخفف محليًا فقط.",
      "CBAP is not the whole agent stack.": "CBAP ليس كامل حزمة الوكلاء.",
      "Put the protocol into a bootable system.": "ضع البروتوكول في نظام قابل للإقلاع.",
      "Same protocol. Different bodies.": "نفس البروتوكول. أجساد مختلفة.",
      "Protocol, subrepos, and acceptance records live in the repo.": "البروتوكول والمستودعات الفرعية وسجلات القبول في المستودع.",
      "This site is a front door only: no mirrored docs, no local service, no runtime data.": "هذا الموقع واجهة فقط: لا نسخ وثائق، لا خدمة محلية، لا بيانات تشغيل.",
      "Open GitHub ↗": "فتح GitHub ↗", "Read README": "قراءة README",
      "Read spec": "قراءة المواصفة", "10-minute path": "مسار 10 دقائق",
      "UNOFFICIAL OPEN-SOURCE PROTOCOL · AS IS · AI-ASSISTED": "بروتوكول مفتوح المصدر غير رسمي · كما هو · بمساعدة الذكاء الاصطناعي",
      "Legal": "قانوني", "Third-party notices": "إشعارات الأطراف الثالثة", "License": "الرخصة",
      "_note": "الأقسام التفصيلية بالإنجليزية حاليًا."
    },
    fr: {
      "An open protocol bridge for physical agents": "Un pont de protocole ouvert pour les agents physiques",
      "active agent subrepos": "sous-dépôts d'agents actifs",
      "source release": "version source",
      "CBAP conformance": "conformité CBAP",
      "control-plane p50 (local UDS)": "p50 plan de contrôle (UDS local)",
      "completion criterion": "critère d'achèvement",
      "See architecture ↓": "Voir l'architecture ↓",

      "Overview": "Aperçu", "Architecture": "Architecture", "Protocol": "Protocole",
      "Security": "Sécurité", "MCP status": "État MCP", "Protocol map": "Carte du protocole",
      "CBAP OS": "CBAP OS", "Agents": "Agents",
      "AGENT ↔ PHYSICAL WORLD / CBAP v1": "AGENT ↔ MONDE PHYSIQUE / CBAP v1",
      "UNOFFICIAL OPEN-SOURCE PROTOCOL": "PROTOCOLE OPEN SOURCE NON OFFICIEL",
      "A protocol where an agent acquires a device, executes an action, and verifies the result through server-authoritative facts. The main repository is CBAP; each agent adapter lives in its own subrepo.":
        "Un protocole où un agent acquiert un appareil, exécute une action et vérifie le résultat via des faits faisant autorité côté serveur. Le dépôt principal est CBAP ; chaque adaptateur d'agent vit dans son propre sous-dépôt.",
      "Open repository ↗": "Ouvrir le dépôt ↗", "Releases": "Versions", "README": "README",
      "See architecture ↓": "Voir l'architecture ↓",
      "Not \"LLM directly driving Minecraft\".": "Pas « un LLM qui pilote Minecraft ».",
      "Agents above. Facts below.": "Les agents au-dessus.<br>Les faits en dessous.",
      "The protocol does not trust \"it said it worked\".": "Le protocole ne croit pas « ça a marché ».",
      "Close the trust boundary before letting AI run.": "Fermer la frontière de confiance<br>avant de laisser courir l'IA.",
      "Upstream is not fixed. CBAP only mitigates locally.": "L'amont n'est pas corrigé.<br>CBAP atténue localement.",
      "CBAP is not the whole agent stack.": "CBAP n'est pas toute<br>la pile agent.",
      "Put the protocol into a bootable system.": "Mettre le protocole dans<br>un système amorçable.",
      "Same protocol. Different bodies.": "Même protocole.<br>Des corps différents.",
      "Protocol, subrepos, and acceptance records live in the repo.": "Protocole, sous-dépôts et preuves d'acceptation sont dans le dépôt.",
      "This site is a front door only: no mirrored docs, no local service, no runtime data.": "Ce site n'est qu'une porte d'entrée : pas de docs miroir, pas de service local, pas de données d'exécution.",
      "Open GitHub ↗": "Ouvrir GitHub ↗", "Read README": "Lire le README",
      "Read spec": "Lire la spécification", "10-minute path": "Parcours 10 minutes",
      "UNOFFICIAL OPEN-SOURCE PROTOCOL · AS IS · AI-ASSISTED": "PROTOCOLE OPEN SOURCE NON OFFICIEL · EN L'ÉTAT · ASSISTÉ PAR IA",
      "Legal": "Mentions légales", "Third-party notices": "Déclarations tierces", "License": "Licence",
      "_note": "Les sections détaillées sont encore en anglais."
    },
    ru: {
      "An open protocol bridge for physical agents": "Открытый протокольный мост для физических агентов",
      "active agent subrepos": "активных подрепозиториев агентов",
      "source release": "исходный релиз",
      "CBAP conformance": "соответствие CBAP",
      "control-plane p50 (local UDS)": "p50 плоскости управления (локальный UDS)",
      "completion criterion": "критерий завершения",
      "See architecture ↓": "Смотреть архитектуру ↓",

      "Overview": "Обзор", "Architecture": "Архитектура", "Protocol": "Протокол",
      "Security": "Безопасность", "MCP status": "Статус MCP", "Protocol map": "Карта протокола",
      "CBAP OS": "CBAP OS", "Agents": "Агенты",
      "AGENT ↔ PHYSICAL WORLD / CBAP v1": "АГЕНТ ↔ ФИЗИЧЕСКИЙ МИР / CBAP v1",
      "UNOFFICIAL OPEN-SOURCE PROTOCOL": "НЕОФИЦИАЛЬНЫЙ ОТКРЫТЫЙ ПРОТОКОЛ",
      "A protocol where an agent acquires a device, executes an action, and verifies the result through server-authoritative facts. The main repository is CBAP; each agent adapter lives in its own subrepo.":
        "Протокол, в котором агент получает устройство, выполняет действие и проверяет результат по фактам на сервере. Основной репозиторий — CBAP; каждый адаптер агента живёт в своём подрепозитории.",
      "Open repository ↗": "Открыть репозиторий ↗", "Releases": "Релизы", "README": "README",
      "See architecture ↓": "Смотреть архитектуру ↓",
      "Not \"LLM directly driving Minecraft\".": "Не «LLM напрямую управляет Minecraft».",
      "Agents above. Facts below.": "Агенты сверху.<br>Факты снизу.",
      "The protocol does not trust \"it said it worked\".": "Протокол не верит «оно сработало».",
      "Close the trust boundary before letting AI run.": "Сначала граница доверия,<br>потом ИИ.",
      "Upstream is not fixed. CBAP only mitigates locally.": "Верхний проект не исправлен.<br>CBAP смягчает локально.",
      "CBAP is not the whole agent stack.": "CBAP — не весь<br>стек агента.",
      "Put the protocol into a bootable system.": "Протокол в<br>загружаемую систему.",
      "Same protocol. Different bodies.": "Тот же протокол.<br>Другие тела.",
      "Protocol, subrepos, and acceptance records live in the repo.": "Протокол, подрепозитории и акты приёмки — в репозитории.",
      "This site is a front door only: no mirrored docs, no local service, no runtime data.": "Сайт — только вход: без зеркал документации, локальных сервисов и данных выполнения.",
      "Open GitHub ↗": "Открыть GitHub ↗", "Read README": "Читать README",
      "Read spec": "Читать спецификацию", "10-minute path": "Путь за 10 минут",
      "UNOFFICIAL OPEN-SOURCE PROTOCOL · AS IS · AI-ASSISTED": "НЕОФИЦИАЛЬНЫЙ ОТКРЫТЫЙ ПРОТОКОЛ · КАК ЕСТЬ · ПРИ УЧАСТИИ ИИ",
      "Legal": "Правовая информация", "Third-party notices": "Уведомления третьих сторон", "License": "Лицензия",
      "_note": "Подробные разделы пока на английском."
    },
    es: {
      "An open protocol bridge for physical agents": "Un puente de protocolo abierto para agentes físicos",
      "active agent subrepos": "subrepos de agentes activos",
      "source release": "versión fuente",
      "CBAP conformance": "conformidad CBAP",
      "control-plane p50 (local UDS)": "p50 del plano de control (UDS local)",
      "completion criterion": "criterio de finalización",
      "See architecture ↓": "Ver la arquitectura ↓",

      "Overview": "Resumen", "Architecture": "Arquitectura", "Protocol": "Protocolo",
      "Security": "Seguridad", "MCP status": "Estado MCP", "Protocol map": "Mapa del protocolo",
      "CBAP OS": "CBAP OS", "Agents": "Agentes",
      "AGENT ↔ PHYSICAL WORLD / CBAP v1": "AGENTE ↔ MUNDO FÍSICO / CBAP v1",
      "UNOFFICIAL OPEN-SOURCE PROTOCOL": "PROTOCOLO OPEN SOURCE NO OFICIAL",
      "A protocol where an agent acquires a device, executes an action, and verifies the result through server-authoritative facts. The main repository is CBAP; each agent adapter lives in its own subrepo.":
        "Un protocolo donde un agente adquiere un dispositivo, ejecuta una acción y verifica el resultado mediante hechos autoritativos del servidor. El repositorio principal es CBAP; cada adaptador de agente vive en su propio subrepo.",
      "Open repository ↗": "Abrir repositorio ↗", "Releases": "Versiones", "README": "README",
      "See architecture ↓": "Ver la arquitectura ↓",
      "Not \"LLM directly driving Minecraft\".": "No es «un LLM conduciendo Minecraft».",
      "Agents above. Facts below.": "Agentes arriba.<br>Hechos abajo.",
      "The protocol does not trust \"it said it worked\".": "El protocolo no cree en «funcionó».",
      "Close the trust boundary before letting AI run.": "Cierra la frontera de confianza<br>antes de dejar correr la IA.",
      "Upstream is not fixed. CBAP only mitigates locally.": "Aguas arriba no está arreglado.<br>CBAP mitiga en local.",
      "CBAP is not the whole agent stack.": "CBAP no es todo<br>el stack de agentes.",
      "Put the protocol into a bootable system.": "Mete el protocolo en<br>un sistema arrancable.",
      "Same protocol. Different bodies.": "Mismo protocolo.<br>Cuerpos distintos.",
      "Protocol, subrepos, and acceptance records live in the repo.": "Protocolo, subrepos y registros de aceptación están en el repo.",
      "This site is a front door only: no mirrored docs, no local service, no runtime data.": "Este sitio es solo una puerta: sin documentación espejo, sin servicio local, sin datos de ejecución.",
      "Open GitHub ↗": "Abrir GitHub ↗", "Read README": "Leer README",
      "Read spec": "Leer la especificación", "10-minute path": "Ruta de 10 minutos",
      "UNOFFICIAL OPEN-SOURCE PROTOCOL · AS IS · AI-ASSISTED": "PROTOCOLO OPEN SOURCE NO OFICIAL · TAL CUAL · ASISTIDO POR IA",
      "Legal": "Legal", "Third-party notices": "Avisos de terceros", "License": "Licencia",
      "_note": "Las secciones detalladas siguen en inglés."
    }
  };

  const 参 = new URLSearchParams(location.search);
  const 是中文页 = (document.documentElement.lang || '').toLowerCase().startsWith('zh');
  const 当前 = 参.get('lang') || (是中文页 ? 'zh' : (localStorage.getItem('lm_lang') || 'en'));
  const 选择器 = '.site-nav a, .hero .eyebrow, .hero .unofficial-tag, .hero .hero-cn, .hero .lede, .hero-actions .btn, .hero-actions .text-link, .stats dd, ' +
    '.section .kicker, .section h2, .section-lede, .cta .kicker, .cta h2, .cta p, .cta-actions .btn, ' +
    '.site-footer .footer-meta span, .site-footer a';

  const 规整 = s => (s || '').replace(/\s+/g, ' ').trim();

  if (!是中文页 && 当前 !== 'en' && 字典[当前]) {
    const 表 = 字典[当前];
    document.documentElement.lang = 当前;
    document.documentElement.dir = 当前 === 'ar' ? 'rtl' : 'ltr';
    document.querySelectorAll(选择器).forEach(el => {
      if (el.classList.contains('lang-select')) return;
      const 原文 = 规整(el.innerText || el.textContent);
      const 译 = 表[原文];
      if (!译) return;
      if (译.includes('<')) el.innerHTML = 译; else el.textContent = 译;
    });
    const 注 = document.createElement('div');
    注.className = 'i18n-note';
    注.textContent = 表._note;
    const 头 = document.querySelector('.site-header');
    if (头) 头.insertAdjacentElement('afterend', 注);
  }

  document.querySelectorAll('.lang-select').forEach(sel => {
    sel.value = 当前;
    sel.addEventListener('change', () => {
      const v = sel.value;
      localStorage.setItem('lm_lang', v);
      if (v === 'zh') location.href = 'zh.html' + location.hash;
      else if (v === 'en') location.href = 'index.html' + location.hash;
      else location.href = 'index.html?lang=' + v + location.hash;
    });
  });
})();
