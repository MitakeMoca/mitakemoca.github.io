(() => {
  const root = document.documentElement;
  const theme = document.querySelector('[data-theme-toggle]');
  const syncTheme = () => {
    if (theme) {
      const dark = root.dataset.theme === 'dark';
      theme.setAttribute('aria-pressed', String(dark));
      theme.textContent = dark ? '☀' : '◐';
    }
  };
  syncTheme();
  theme?.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('theme', root.dataset.theme); } catch {}
    syncTheme();
  });
  const menu = document.querySelector('[data-menu-toggle]');
  const nav = document.querySelector('#navigation');
  menu?.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    nav?.classList.toggle('open', open);
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      nav?.classList.remove('open');
      menu?.setAttribute('aria-expanded', 'false');
    }
  });
  const more = document.querySelector('[data-more-updates]');
  more?.addEventListener('click', () => {
    const expanded = more.getAttribute('aria-expanded') !== 'true';
    document.querySelectorAll('[data-older-update]').forEach(el => el.hidden = !expanded);
    more.setAttribute('aria-expanded', String(expanded));
    more.textContent = expanded ? more.dataset.less : more.dataset.more;
  });
  document.querySelectorAll('[data-filter]').forEach(button => {
    button.addEventListener('click', () => {
      document.querySelectorAll('[data-filter]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
      document.querySelectorAll('[data-course]').forEach(row => {
        row.hidden = button.dataset.filter === 'lead' && row.dataset.lead !== 'true';
      });
    });
  });
  // Older updates remain available without JavaScript.
  document.querySelectorAll('[data-older-update]').forEach(el => el.hidden = true);
  if (more) more.hidden = false;
  document.querySelectorAll('.js-only').forEach(el => el.hidden = false);
})();
