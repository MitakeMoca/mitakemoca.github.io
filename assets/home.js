(() => {
  const root = document.documentElement;
  const theme = document.querySelector('[data-theme-toggle]');
  const menu = document.querySelector('[data-menu-toggle]');
  const nav = document.querySelector('#navigation');
  const syncTheme = () => {
    const dark = root.dataset.theme === 'dark';
    theme?.setAttribute('aria-pressed', String(dark));
    if (theme) theme.textContent = dark ? '☀' : '◐';
  };
  syncTheme();
  theme?.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('theme', root.dataset.theme); } catch {}
    syncTheme();
  });
  const closeMenu = () => {
    menu?.setAttribute('aria-expanded', 'false');
    nav?.classList.remove('open');
  };
  menu?.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    nav?.classList.toggle('open', open);
  });
  nav?.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') closeMenu();
  });
  document.querySelectorAll('[data-theme-toggle],[data-menu-toggle]').forEach(button => button.hidden = false);
  const anchors = [...document.querySelectorAll('#navigation a')];
  const sections = anchors.map(a => document.getElementById(a.hash.slice(1))).filter(Boolean);
  const updateCurrent = () => {
    let current = sections[0];
    for (const section of sections) if (section.getBoundingClientRect().top <= 125) current = section;
    anchors.forEach(a => {
      if (current && a.hash === '#' + current.id) a.setAttribute('aria-current', 'location');
      else a.removeAttribute('aria-current');
    });
  };
  let scheduled = false;
  addEventListener('scroll', () => {
    if (!scheduled) requestAnimationFrame(() => { updateCurrent(); scheduled = false; });
    scheduled = true;
  }, { passive: true });
  updateCurrent();
})();
