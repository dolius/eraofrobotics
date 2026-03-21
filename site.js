document.addEventListener('DOMContentLoaded', () => {
  const btn = document.querySelector('.nav-toggle');
  const menu = document.querySelector('.site-nav');
  if (!btn || !menu) return;
  btn.addEventListener('click', () => {
    const open = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!open));
    menu.classList.toggle('open', !open);
    document.body.classList.toggle('menu-open', !open);
  });
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    btn.setAttribute('aria-expanded', 'false');
    menu.classList.remove('open');
    document.body.classList.remove('menu-open');
  }));
});
