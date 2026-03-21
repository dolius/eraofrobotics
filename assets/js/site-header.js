(function () {
  if (!document.body || document.querySelector('.site-header')) return;

  var links = [
    { href: '/index.html', label: 'Home' },
    { href: '/robotics-shift-guide.html', label: 'Explainer' },
    { href: '/tools.html', label: 'Tools' },
    { href: '/briefs.html', label: 'Reports' },
    { href: '/reference-asset-page.html', label: 'Resources' }
  ];

  var currentPath = (window.location.pathname || '').toLowerCase();

  function isActive(href) {
    var normalized = href.toLowerCase();
    if (normalized === '/index.html' && (currentPath === '/' || currentPath === '/index.html')) return true;
    return currentPath === normalized;
  }

  var navLinks = links
    .map(function (item) {
      var activeClass = isActive(item.href) ? ' class="active"' : '';
      return '<a' + activeClass + ' href="' + item.href + '">' + item.label + '</a>';
    })
    .join('');

  var header = document.createElement('header');
  header.className = 'site-header';
  header.innerHTML =
    '<div class="site-header-inner">' +
      '<a class="site-brand" href="/index.html">Era of Robotics</a>' +
      '<button class="mobile-menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>' +
      '<nav id="site-nav" class="site-nav">' + navLinks + '</nav>' +
    '</div>';

  document.body.prepend(header);
  document.body.classList.add('has-site-header');

  var button = header.querySelector('.mobile-menu-btn');
  var nav = header.querySelector('#site-nav');

  function closeMenu() {
    nav.classList.remove('open');
    button.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('nav-open');
  }

  button.addEventListener('click', function () {
    var isOpen = nav.classList.toggle('open');
    button.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    document.body.classList.toggle('nav-open', isOpen);
  });

  nav.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', closeMenu);
  });

  window.addEventListener('resize', function () {
    if (window.innerWidth > 980) closeMenu();
  });

  window.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') closeMenu();
  });
})();
