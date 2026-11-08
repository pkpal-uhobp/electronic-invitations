// Existing PR6 mobile navigation and current-year footer.
const yearElement = document.getElementById('current-year');
if (yearElement) yearElement.textContent = new Date().getFullYear();
const toggle = document.getElementById('nav-toggle');
const navigation = document.getElementById('site-nav');
if (toggle && navigation) {
  toggle.addEventListener('click', () => {
    const expanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!expanded));
    toggle.setAttribute('aria-label', expanded ? 'Открыть меню' : 'Закрыть меню');
    navigation.classList.toggle('is-open', !expanded);
  });
}
